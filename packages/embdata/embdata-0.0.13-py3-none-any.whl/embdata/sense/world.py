from functools import wraps
from importlib.resources import files

import numpy as np
from aiocache import cached
from multidict import MultiDict
from pydantic import Field, PrivateAttr, model_serializer, model_validator
from typing_extensions import Any, Generic, ItemsView, Iterable, Iterator, List, Literal, Type, TypeAlias, TypeVar, overload

from embdata.coordinate import Coordinate, Pose6D
from embdata.geometry import Transform3D
from embdata.ndarray import NumpyArray
from embdata.sample import Sample
from embdata.sense.camera import Camera
from embdata.sense.depth import Depth, Plane
from embdata.sense.image import Image
from embdata.sense.state import State
from embdata.utils.geometry_utils import rotation_from_z
from embdata.utils.import_utils import smart_import
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from meshcat import Visualizer


class BBox2D(Coordinate):
    """Model for 2D Bounding Box."""

    x1: float
    y1: float
    x2: float
    y2: float

    @classmethod
    def from_list(cls, bbox_list: list[float]) -> "BBox2D":
        return cls(x1=bbox_list[0], y1=bbox_list[1], x2=bbox_list[2], y2=bbox_list[3])


class BBox3D(Coordinate):
    """Model for 3D Bounding Box."""

    x1: float
    y1: float
    z1: float
    x2: float
    y2: float
    z2: float

    @classmethod
    def from_list(cls, bbox_list: list[float]) -> "BBox3D":
        return cls(x1=bbox_list[0], y1=bbox_list[1], z1=bbox_list[2], x2=bbox_list[3], y2=bbox_list[4], z2=bbox_list[5])


class PixelCoords(Coordinate):
    """Model for Pixel Coordinates."""
    u: int
    v: int

    @classmethod
    def from_list(cls, coords_list: list[int]) -> "PixelCoords":
        return cls(u=coords_list[0], v=coords_list[1])

T= TypeVar("T", bound=Sample)
class MultiSample(Sample, Generic[T]):
    """Model for a collection of values. Iterating over the collection will yield all values unlike Sample.

    Methods:
        add: Add a new value to the collection.
        getone: Get the first value for a key.s
        getall: Get all values for a key.
    """
    _store: MultiDict[str, T] = PrivateAttr(default_factory=MultiDict)
    _object_type: Type[Sample] = PrivateAttr(default_factory=lambda: Sample) # Actually a class variable of the instance's class weirdly enough.

    def __class_getitem__(cls, item: Any) -> TypeAlias:
        cls._object_type = item
        return super().__class_getitem__(item)

    @wraps(MultiDict.add)
    def append(self, value: T) -> Self:
        self._store.add(value.name if hasattr(value, "name") else value.__class__.__name__, value)
        return self
    @wraps(MultiDict.add)
    def add(self, key: str, value: T) -> Self:
        self._store.add(key, value)
        return self

    @wraps(MultiDict.getone)
    def getone(self, key: str) -> T:
        return self._store.getone(key)

    @wraps(MultiDict.popone)
    def popone(self, key: str) -> T:
        return self._store.popone(key)

    @wraps(MultiDict.getall)
    def getall(self, key: str) -> List[T]:
        return self._store.getall(key)

    def __iter__(self) -> Iterator[T]:
        for value in self._store.values():
            if isinstance(value, list):
                yield from value
            else:
                yield value

    def __len__(self) -> int:
        return len(list(iter(self)))

    def __getattr__(self, item: str) -> T | List[T]:
        if any(a in item for a in ["_", "__", "pydantic", "getitem", "getattr", "setattr", "delattr"]):
            return super().__getattr__(item)
        return self._store.__getattribute__(item)

    def __contains__(self, item: str) -> bool:
        return item in self._store

    def __setitem__(self, key: str, value: T) -> None:
        self._store[key] = value


    def __getitem__(self, item: int | str) -> T | List[T]:
        if isinstance(item, int):
            return list(iter(self))[item]
        return self._store[item]

    def items(self) -> Iterable[ItemsView]:
        return self._store.items()

    def values(self) -> Iterable[T]:
        return self._store.values()

    def keys(self) -> Iterable[str]:
        return self._store.keys()

    @staticmethod
    def concat(collections: List["MultiSample[T]"]) -> "MultiSample[T]":
        if len(collections) in [0, 1]:
            return collections[0] if collections else MultiSample()
        result = collections[0]
        for collection in collections[1:]:
            for key, value in collection.items():
                if isinstance(value, list):
                    if key in result:
                        if isinstance(result[key], list):
                            result[key].extend(value)
                        else:
                            result[key] = [result[key], *value]
                    else:
                        result[key] = value
                elif key in result:
                    if isinstance(result[key], list):
                        result[key].append(value)
                    else:
                        result[key] = [result[key], value]
                else:
                    result[key] = value

        return result

    @staticmethod
    def from_list(data: List[T]) -> "MultiSample[T]":
        collection = Collection[T]()
        for item in data:
            key = item.name if hasattr(item, "name") else item.__class__.__name__
            collection.add(key, item)
        return collection

    @overload
    def __init__(self, data_list: list[T]) -> None:
        ...

    @overload
    def __init__(self, data_dict: dict[str, T]) -> None:
        ...

    @overload
    def __init__(self, **data: dict[str, T] | list[T]) -> None:
        ...

    def __init__(self, arg: list[T] | dict[str, T] | None = None, **data: dict[str, T]) -> None:
        """Initialize the MultiSample object with the given data.

        The data can be a list of values, a dictionary of values, or keyword arguments.
        """
        arg = arg or {}
        if isinstance(arg, list):
            objects = {}
            for i, item in enumerate(arg):
                # Determine the key for the object
                key = item.name if hasattr(item, "name") else item.get("name", f"item_{i}")
                
                # Append or initialize the objects under the key
                if key in objects:
                    if isinstance(objects[key], list):
                        objects[key].append(item)
                    else:
                        objects[key] = [objects[key], item]
                else:
                    objects[key] = item  # Initialize with the first item
            arg = objects

        data.update(arg)
        ObjectType = self._object_type # noqa
        # Ensure that we correctly handle lists and dictionaries
        final_data = {}
        for k, v in data.items():
            if isinstance(v, ObjectType):
                final_data[k] = v
            elif isinstance(v, dict):
                final_data[k] = ObjectType(**v)
            elif isinstance(v, list):
                final_data[k] = [ObjectType(**item) if isinstance(item, dict) else ObjectType(item) for item in v]
            else:
                final_data[k] = ObjectType(v)

        super().__init__(**final_data)
        # # Add references to multidict
        for key, value in final_data.items():
            self.add(key, value)

    def __eq__(self, other: object) -> bool:
        return all(
            obj == other_obj or (obj is None and other_obj is None)
            for obj, other_obj in zip(self.values(), other.values(), strict=False)
        )

Collection: TypeAlias = MultiSample[T]

def process_field(value: Any, field_type: Type[Sample]) -> Sample | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return field_type(**value)
    return field_type(value) if not isinstance(value, field_type) else value
class WorldObject(Sample):
    """Model for world Object. It describes the objects in the scene.

    Attributes:
        name (str): The name of the object.
        bbox_2d (BBox2D | None): The 2D bounding box of the object.
        bbox_3d (BBox3D | None): The 3D bounding box of the object.
        pose (Pose | None): The pose of the object.
        pixel_coords (PixelCoords | None): The pixel coordinates of the object.
        mask (NumpyArray | None): The mask of the object.
    """

    name: str = ""
    bbox_2d: BBox2D | None = None
    bbox_3d: BBox3D | None = None
    volume: float | None = None
    pose: Pose6D | None = None
    pixel_coords: PixelCoords | None = None
    mask: NumpyArray[Any, Any] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate(cls, v: Any | None) -> Any:
        v["bbox_2d"] = process_field(v.get("bbox_2d"), BBox2D)
        if v["bbox_2d"] is None:
            del v["bbox_2d"]
        v["bbox_3d"] = process_field(v.get("bbox_3d"), BBox3D)
        if v["bbox_3d"] is None:
            del v["bbox_3d"]
        v["pose"] = process_field(v.get("pose"), Pose6D)
        if v["pose"] is None:
            del v["pose"]
        v["pixel_coords"] = process_field(v.get("pixel_coords"), PixelCoords)
        if v["pixel_coords"] is None:
            del v["pixel_coords"]
        v["mask"] = process_field(v.get("mask"), np.array)
        if v["mask"] is None:
            del v["mask"]
        return v

    def __eq__(self, other):
        return (
            self.name == other.name and
            (self.bbox_2d == other.bbox_2d or (self.bbox_2d is None and other.bbox_2d is None)) and
            (self.bbox_3d == other.bbox_3d or (self.bbox_3d is None and other.bbox_3d is None)) and
            (self.volume == other.volume or (self.volume is None and other.volume is None)) and
            self.pose == other.pose and
            self.pixel_coords == other.pixel_coords and
            (self.mask == other.mask or (self.mask is None and other.mask is None))
        )

class World(Sample):
    """Model for World Data.

    To keep things simple, always keep the objects in the camera frame. Perform transformations during access.
    """

    image: Image | None = None
    depth: Depth | None = None
    annotated: Image | None = None
    objects: Collection[WorldObject] = Field(default_factory=Collection[WorldObject], description="List of scene objects")
    camera: Camera = Field(default_factory=Camera, description="Camera parameters of the scene")

    def __getitem__(self, item):
        # Access the underlying dictionary directly to avoid recursion
        if item in self.objects:
            return self.objects[item]
        return getattr(self, item)

    def object_names(self) -> List[str]:
        return list({obj.name for obj in self.objects} | {"plane", "camera"})

    def add_object(self, obj: WorldObject) -> None:
        self.objects.append(obj)

    @model_validator(mode="before")
    @classmethod
    def validate(cls, v: Any | None) -> Any:
        if v and v.get("objects") is not None and not isinstance(v["objects"], Collection[WorldObject]):
            v["objects"] = Collection[WorldObject](v["objects"])
        return v

    @wraps("World.get_object")
    @cached(ttl=10)
    def aget_object(self, name: str, reference: str | WorldObject | Pose6D | np.ndarray = "camera") -> WorldObject | None:
        return self.get_object(name, reference)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, World):
            return False
        return (
            self.image == other.image
            and self.depth == other.depth
            and self.objects == other.objects
            and self.camera == other.camera
        )

    def get_object(
        self, name: str, reference: str | WorldObject | Pose6D | np.ndarray = "camera"
    ) -> WorldObject | List[WorldObject] | None:
        """Get the object(s) from the scene in the specified reference frame.

        If name is "all", returns all objects in the specified reference frame.
        If reference is another object name, return the pose relative to that object.

        Args:
            name (str): The name of the object. Use "all" to get all objects.
            reference (str | WorldObject | Pose6D | np.ndarray): The reference frame or object of the object(s).

        Returns:
            WorldObject | List[WorldObject] | None: The object(s) in the specified reference frame or None if the object does not exist.

        Examples:
            >>> world.get_object("object1", reference="camera")
            WorldObject(name="object1", pose=Pose(x=0.0, y=0.2032, z=0.0, roll=-1.5707963267948966, pitch=0.0, yaw=-1.57), pixel_coords=PixelCoords(u=320, v=240))
            >>> world.get_object("all", reference="plane")
            [WorldObject(name="object1", pose=Pose(x=0.0, y=0.2032, z=0.0, roll=0.0, pitch=0.0, yaw=0.0), pixel_coords=PixelCoords(u=320, v=240)),
            WorldObject(name="object2", pose=Pose(x=0.1, y=0.2032, z=0.1, roll=0.0, pitch=0.0, yaw=0.0), pixel_coords=PixelCoords(u=400, v=300))]
        """
        # Handle the case where name is "all"
        if name == "all":
            world_copy = self.model_copy()
            world_copy.transform_objects(reference)
            return self.objects

        # Get all objects with the given name
        targets = self.objects.getall(name)
        if not targets:
            return None

        # Handle the case where there are multiple objects
        results = []
        for target in targets:
            new_target = target.model_copy()

            if not hasattr(self, "plane"):
                # Ensure the plane is segmented
                self.plane: Plane = self.depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000, camera=self.camera)
                normal = self.plane.normal(self.plane.coefficients)
                negative_normal = np.array([-normal.x, -normal.y, -normal.z])
                rotation_matrix = rotation_from_z(negative_normal)
                self.transform = Transform3D(rotation=rotation_matrix)

            # Obtain the reference object
            if isinstance(reference, str):
                if reference == "camera":
                    reference_obj = WorldObject(name="camera", pose=Pose6D())
                elif reference == "plane":
                    reference_obj = WorldObject(name="plane", pose=Pose6D())  # Placeholder for the plane pose
                else:
                    reference_obj = self.objects.get(reference)
                    if reference_obj is None:
                        msg = f"Reference object '{reference}' not found."
                        raise ValueError(msg)
            elif isinstance(reference, WorldObject):
                reference_obj = reference
            elif isinstance(reference, Pose6D | np.ndarray):
                reference_obj = WorldObject(
                    name="custom_reference", pose=Pose6D(*reference) if isinstance(reference, np.ndarray) else reference
                )
            else:
                msg = "Reference must be a string, WorldObject, Pose6D, or numpy array."
                raise TypeError(msg)

            # Compute pose if missing
            if target.pose is None:
                point_3d = self.depth.camera.deproject(target.pixel_coords, depth_image=self.depth.array)
                target.pose = Pose6D(*point_3d, roll=0, pitch=0, yaw=0)

            if reference_obj.pose is None:
                point_3d = self.depth.camera.deproject(reference_obj.pixel_coords, depth_image=self.depth.array)
                reference_obj.pose = Pose6D(*point_3d, roll=0, pitch=0, yaw=0)

            if reference_obj.name != "camera":
                target_pose = self.transform.transform(target.pose.numpy()[:3])
                reference_pose = self.transform.transform(reference_obj.pose.numpy()[:3])
            else:
                target_pose, reference_pose = target.pose, reference_obj.pose

            new_target.pose = Pose6D(*(target_pose - reference_pose), roll=0, pitch=0, yaw=0)
            results.append(new_target)

        # Return a single object or a list of objects
        return results[0] if len(results) == 1 else results

    def transform_objects(self, reference: str | WorldObject | Pose6D | np.ndarray = "camera") -> None:
        """Transform all objects in place to the specified reference frame.

        Args:
            reference (str | WorldObject | Pose6D | np.ndarray): The reference frame or object for the transformation.
        """
        # Obtain the reference object
        if isinstance(reference, str):
            if reference == "camera":
                reference_obj = WorldObject(name="camera", pose=Pose6D())
            elif reference == "plane":
                reference_obj = WorldObject(name="plane", pose=Pose6D())  # Placeholder for the plane pose
            else:
                reference_obj = self.objects.get(reference)
                if reference_obj is None:
                    msg = f"Reference object '{reference}' not found."
                    raise ValueError(msg)
        elif isinstance(reference, WorldObject):
            reference_obj = reference
        elif isinstance(reference, Pose6D | np.ndarray):
            reference_obj = WorldObject(
                name="custom_reference", pose=Pose6D(*reference) if isinstance(reference, np.ndarray) else reference
            )
        else:
            msg = "Reference must be a string, WorldObject, Pose6D, or numpy array."
            raise TypeError(msg)

        # Transform all objects in the collection
        for target in self.objects.values():
            if not hasattr(self, "plane"):
                # Ensure the plane is segmented
                self.plane: Plane = self.depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000)
                normal = self.plane.normal(self.plane.coefficients)
                negative_normal = np.array([-normal.x, -normal.y, -normal.z])
                rotation_matrix = rotation_from_z(negative_normal)
                self.transform = Transform3D(rotation=rotation_matrix)

            # Compute pose if missing
            if target.pose is None:
                point_3d = self.depth.camera.deproject(target.pixel_coords, depth_image=self.depth.array)
                target.pose = Pose6D(*point_3d, roll=0, pitch=0, yaw=0)

            if reference_obj.pose is None:
                point_3d = self.depth.camera.deproject(reference_obj.pixel_coords, depth_image=self.depth.array)
                reference_obj.pose = Pose6D(*point_3d, roll=0, pitch=0, yaw=0)

            # Perform the transformation
            if reference_obj.name != "camera":
                target_pose = self.transform.transform(target.pose.numpy()[:3])
                reference_pose = self.transform.transform(reference_obj.pose.numpy()[:3])
            else:
                target_pose, reference_pose = target.pose, reference_obj.pose

            # Update the target object pose
            target.pose = Pose6D(*(target_pose - reference_pose), roll=0, pitch=0, yaw=0)

    def show(self, backend: Literal["open3d", "meshcat"] = "open3d") -> None:
        """Display the world state. Optionally use MeshCat for visualization.

        Args:
            use_meshcat (bool): If True, use MeshCat for visualization; otherwise, use Open3D.
        """
        if backend == "meshcat":
            meshcat = smart_import("meshcat")
            g = smart_import("meshcat.geometry")
            tf = smart_import("meshcat.transformations")
            vis: Visualizer = meshcat.Visualizer()
            vis = vis.open()

            # Transform the plane's point cloud and get objects in reference to the plane
            self.plane.point_cloud.transform(self.transform.matrix())
            self.objects = self.get_object("all", reference="plane")

            inlier_cloud = self.plane.point_cloud.select_by_index(self.plane.inliers)
            outlier_cloud = self.plane.point_cloud.select_by_index(self.plane.inliers, invert=True)

            # Add plane point cloud
            vis["plane"].set_object(g.Points(g.PointsGeometry(self.plane.point_cloud.points), g.PointsMaterial()))

            # Color the inliers red
            vis["inliers"].set_object(g.Points(g.PointsGeometry(inlier_cloud.points), g.PointsMaterial(color=0xff0000)))

            # Add objects to the scene
            for i, obj in enumerate(self.objects):
                vis[f"object_{i}"].set_object(g.TriangleMeshGeometry(), g.MeshPhongMaterial())
                vis[f"object_{i}"].set_transform(tf.translation_matrix(obj.pose.numpy()[:3]))

            # Add a global coordinate frame
            vis["global_frame"].set_object(g.TriangleMeshGeometry(), g.MeshPhongMaterial())
            vis["global_frame"].set_transform(tf.translation_matrix([0, 0, 0]))
            # Print the URL where MeshCat is running
            print(f"MeshCat is running at: {vis.url()}")
            input("Press Enter to shut down the MeshCat server...")
            vis.close()

        else:
            o3d = smart_import("open3d")
            vis = smart_import("open3d.visualization")
            self.plane.point_cloud.transform(self.transform.matrix())
            self.objects = self.get_object("all", reference="plane")
            inlier_cloud = self.plane.point_cloud.select_by_index(self.plane.inliers)
            outlier_cloud = self.plane.point_cloud.select_by_index(self.plane.inliers, invert=True)

            # Color the inliers red
            inlier_cloud.paint_uniform_color([1, 0, 0])

            geometries = (
                [self.plane.point_cloud]
                + [
                    o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=obj.pose.numpy()[:3])
                    for obj in self.objects
                ]
                + [inlier_cloud, outlier_cloud]
                + [
                    o3d.geometry.TriangleMesh.create_coordinate_frame(
                        size=0.1, origin=Pose6D(x=0, y=0, z=0, roll=0, pitch=0, yaw=0).numpy()[:3]
                    )
                ]
            )
            vis.draw_geometries(geometries)

if __name__ == "__main__":
    from mbodied.agents.sense.object_detection_agent import ObjectDetectionAgent

    from embdata.sense.camera import Camera, Distortion, Extrinsics, Intrinsics

    object_detection_agent = ObjectDetectionAgent()
    rgb_path = files("embdata") / "resources" / "color_image.png"
    depth_path = files("embdata") / "resources" / "depth_image.png"
    rgb_image = Image(path=rgb_path)
    object_names = ["Remote Control, Spoon, Basket, Red Marker"]

    world: World = object_detection_agent.act(image=rgb_image, objects=object_names)

    depth = Depth(
        path=depth_path,
        mode="I",
        size=(1280, 720),
        rgb=rgb_image,
        camera=Camera(
            intrinsic=Intrinsics(fx=911.0, fy=911.0, cx=653.0, cy=371.0),
            distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
            extrinsic=Extrinsics(),
            depth_scale=0.001,
        ),
        unit="mm",
    )

    world.depth = depth
    world.camera = depth.camera
    world.image = rgb_image
    print(world)
    print(list(world.objects.keys()))
    relative_pose = world.get_object("Red Marker", reference="Remote Control")
    print(relative_pose)
