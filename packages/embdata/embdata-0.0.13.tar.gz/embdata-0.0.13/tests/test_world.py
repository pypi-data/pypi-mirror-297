import time
import time
from embdata.sense.depth import Depth, Plane
from embdata.sense.world import World, WorldObject, PixelCoords, Collection, MultiSample
from embdata.sense.image import Image
from embdata.sense.camera import Camera, Distortion, Intrinsics
from embdata.geometry import Transform3D
from embdata.utils.geometry_utils import rotation_between_two_points
from embdata.coordinate import Coordinate, Point, Pose6D
from lager import log
import numpy as np
import pytest
from embdata.coordinate import Pose
from importlib_resources import files

import open3d as o3d

WORLD_POSE = Pose(x=0.0, y=0.2032, z=0.0, roll=-np.pi / 2, pitch=0.0, yaw=-np.pi / 2)
camera = Camera(
    intrinsic=Intrinsics(fx=911, fy=911, cx=653, cy=371),
    distortion=Distortion(k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0),
    depth_scale=0.001,
)

DEFAULT_WORLD = World(
    objects=[WorldObject(name="object1", pose=Pose(), pixel_coords=PixelCoords(u=320, v=240))],
    image=Image(array=np.zeros([480, 640, 3], dtype=np.uint8), mode="RGB", encoding="png"),
    depth=Depth(
        path=files("embdata") / "resources/depth_image.png",
        mode="I",
        encoding="png",
        size=(1280, 720),
        camera=camera,
        rgb=Image(path=files("embdata") / "resources/color_image.png", mode="RGB", encoding="png"),
        unit="mm",
    ),
    camera=camera,
)
DEPTH_IMAGE_PATH = files("embdata") / "resources/depth_image.png"
COLOR_IMAGE_PATH = files("embdata") / "resources/color_image.png"
@pytest.fixture
def setup_world_pose() -> Pose:
    return WORLD_POSE


@pytest.fixture
def setup_camera() -> Camera:
    return camera


@pytest.fixture
def depth_image_path() -> Image:
    return DEPTH_IMAGE_PATH



@pytest.fixture
def color_image_path():
  return COLOR_IMAGE_PATH


@pytest.fixture
def test_world() -> World:
    return DEFAULT_WORLD


def test_get_object(test_world):
    example_scene = test_world
    print(example_scene.objects)
    print(example_scene.objects._store)
    print(list(example_scene.objects.keys()))
    depth = example_scene.depth

    # Perform plane segmentation
    plane_normal: Coordinate = depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000)
    normal = plane_normal.normal(plane_normal.coefficients)
    np.allclose(normal, Point(**{"x": 0.017803989474007905, "y": 0.9977034758324792, "z": 0.06535129892051982}).numpy())
    # Define the origin and z-axis
    result = example_scene.get_object("object1", reference="plane")
    assert result is not None

    result = example_scene.get_object("all", reference="plane")
    assert result is not None
    result = example_scene.get_object("all", reference="plane")
    assert result is not None

    result = example_scene.get_object("object1", reference="object1")
    assert result is not None
    result = example_scene.get_object("object1", reference="object1")
    assert result is not None

def test_get_object_with_duplicate(test_world: World):
    example_scene = test_world
    example_scene.objects.append(WorldObject(name="object_dup", pose=Pose(), pixel_coords=PixelCoords(u=320, v=240)))
    example_scene.objects.append(WorldObject(name="object_dup", pose=Pose(), pixel_coords=PixelCoords(u=400, v=500)))
    depth = example_scene.depth

    # Perform plane segmentation
    plane_normal: Coordinate = depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000)
    normal = plane_normal.normal(plane_normal.coefficients)
    np.allclose(normal, Point(**{"x": 0.017803989474007905, "y": 0.9977034758324792, "z": 0.06535129892051982}).numpy())
    # Define the origin and z-axis
    result = example_scene.get_object("all", reference="plane")
    for obj in result:
        assert obj.name is not None

def test_transform_object(test_world: World):
    example_scene = test_world
    depth = example_scene.depth

    # Perform plane segmentation
    plane_normal: Coordinate = depth.segment_plane(threshold=0.01, min_samples=3, max_trials=1000)
    normal = plane_normal.normal(plane_normal.coefficients)
    np.allclose(normal, Point(**{"x": 0.017803989474007905, "y": 0.9977034758324792, "z": 0.06535129892051982}).numpy())
    # Define the origin and z-axis
    example_scene.transform_objects(reference="plane")


@pytest.fixture
def setup_collection() -> Collection[WorldObject]:
    """Fixture to create a collection of WorldObjects."""
    return Collection[WorldObject]()


def test_append_and_retrieve_by_key(setup_collection):
    """Test appending items and retrieving them by key."""
    collection = setup_collection

    # Create and append objects
    obj1 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj2 = WorldObject(name="object2", pixel_coords=PixelCoords(u=300, v=400))
    obj3 = WorldObject(name="object1", pixel_coords=PixelCoords(u=500, v=600))  # Duplicate key

    collection.append(obj1)
    collection.append(obj2)
    collection.append(obj3)

    # Assert that objects are retrievable by key
    assert collection["object1"] == obj1  # Gets the first "object1"
    assert collection.getall("object1") == [obj1, obj3]  # Should return a list of all "object1"
    assert collection["object2"] == obj2


def test_retrieve_by_index(setup_collection):
    """Test retrieving items by index."""
    collection = setup_collection

    # Create and append objects
    obj1 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj2 = WorldObject(name="object2", pixel_coords=PixelCoords(u=300, v=400))

    collection.append(obj1)
    collection.append(obj2)

    # Assert retrieval by index
    assert collection[0] == obj1
    assert collection[1] == obj2


def test_iteration(setup_collection):
    """Test iteration over the collection."""
    collection = setup_collection

    # Create and append objects
    obj1 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj2 = WorldObject(name="object2", pixel_coords=PixelCoords(u=300, v=400))

    collection.append(obj1)
    collection.append(obj2)

    # Assert that iteration yields all objects
    items = list(iter(collection))
    assert items == [obj1, obj2]


def test_multiple_iteration(setup_collection):
    """Test iteration over the collection."""
    collection = setup_collection

    # Create and append objects
    obj1 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj2 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj3 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj4 = WorldObject(name="object2", pixel_coords=PixelCoords(u=300, v=400))

    collection.append(obj1)
    collection.append(obj2)
    collection.append(obj3)
    collection.append(obj4)

    # Assert that iteration yields all objects
    items = list(iter(collection))
    assert items == [obj1, obj2, obj3, obj4]


def test_length(setup_collection):
    """Test the length calculation of the collection."""
    collection = setup_collection

    # Create and append objects
    obj1 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj2 = WorldObject(name="object2", pixel_coords=PixelCoords(u=300, v=400))

    collection.append(obj1)
    collection.append(obj2)

    # Assert that length matches the number of objects
    assert len(collection) == 2


def test_concatenation():
    """Test concatenating multiple collections."""
    collection1 = Collection[WorldObject]()
    collection2 = Collection[WorldObject]()

    obj1 = WorldObject(name="object1", pixel_coords=PixelCoords(u=100, v=200))
    obj2 = WorldObject(name="object2", pixel_coords=PixelCoords(u=300, v=400))
    obj3 = WorldObject(name="object3", pixel_coords=PixelCoords(u=500, v=600))

    collection1.append(obj1)
    collection2.append(obj2)
    collection2.append(obj3)

    concatenated = Collection.concat([collection1, collection2])
    print(concatenated)
    
    # Assert all objects are in the concatenated collection
    assert len(concatenated) == 3
    assert concatenated.getall("object1") == [obj1]
    assert concatenated.getall("object2") == [obj2]
    assert concatenated.getall("object3") == [obj3]


@pytest.mark.network
def test_fastapi(test_world: World):
    from fastapi import FastAPI
    from httpx import Client
    from embdata.utils.network_utils import get_open_port
    from time import sleep
    import uvicorn
    
    app = FastAPI()
    
    @app.post("/test")
    async def test(d: World) -> World:
        assert isinstance(d, World)
        assert d.objects == test_world.objects
        return world
    port = get_open_port()
    
    import threading
    thread = threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": "localhost", "port": port}, daemon=True)
    thread.start()
    sleep(5)
    client = Client()
    world = test_world
    response = client.post(f"http://localhost:{port}/test", json=world.model_dump(mode="json"))

    assert response.status_code == 200
    world_resp = World(**response.json())
    assert np.allclose(world_resp.depth.array, world.depth.array)
    assert world_resp.camera == world.camera
    assert world_resp.objects == world.objects

    thread.join(timeout=10)  # Add a timeout to prevent hanging
    print("Test completed")

if __name__ == "__main__":
    pytest.main([__file__, "-vv"])