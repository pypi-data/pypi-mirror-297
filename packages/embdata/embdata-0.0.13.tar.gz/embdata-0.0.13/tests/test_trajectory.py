from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING
import numpy as np
import pytest
from embdata.trajectory import stats, Trajectory

if TYPE_CHECKING:
    import contextlib
    with contextlib.suppress(ImportError):
        from plotext import play_video
        from plotext._figure import _figure_class
        import pandas as pd


def test_stats():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = stats(array)
    expected_result = {
        "mean": [4.0, 5.0, 6.0],
        "variance": [6.0, 6.0, 6.0],
        "skewness": [0.0, 0.0, 0.0],
        "kurtosis": [-1.5, -1.5, -1.5],
        "min": [1, 2, 3],
        "max": [7, 8, 9],
    }
    assert np.array_equal(result["mean"], expected_result["mean"])
    # assert np.array_equal(result['variance'], expected_result['variance'])
    assert np.array_equal(result["skewness"], expected_result["skewness"])
    assert np.array_equal(result["kurtosis"], expected_result["kurtosis"])
    assert np.array_equal(result["min"], expected_result["min"])
    assert np.array_equal(result["max"], expected_result["max"])


def test_relative():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    trajectory = Trajectory(array, freq_hz=1)
    relative_trajectory = trajectory.relative_to(-1)
    expected_array = np.array([[3, 3, 3], [3, 3, 3]])
    assert np.array_equal(relative_trajectory.array, expected_array)


def test_minmax():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    trajectory = Trajectory(steps=array, freq_hz=1)
    minmax_trajectory = trajectory.minmax(0, 255)
    expected_array = 255 * (array - np.min(array, axis=0)) / (np.max(array, axis=0) - np.min(array, axis=0))
    assert np.array_equal(minmax_trajectory, expected_array)


def test_resample():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(steps=array, freq_hz=1)
    resampled_trajectory = trajectory.resample(target_hz=0.5)
    expected_array = np.array([[1, 2, 3], [7, 8, 9]])
    assert np.allclose(resampled_trajectory.array, expected_array)
    assert resampled_trajectory.freq_hz == 0.5


def test_upsample():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(steps=array, freq_hz=1)
    upsampled_trajectory = trajectory.resample(target_hz=2)
    expected_array = np.array(
        [
            [1.0, 2.0, 3.0],
            [2.5, 3.5, 4.5],
            [4.0, 5.0, 6.0],
            [5.5, 6.5, 7.5],
            [7.0, 8.0, 9.0],
            [8.5, 9.5, 10.5],
            [10.0, 11.0, 12.0],
        ]
    )
    assert np.allclose(upsampled_trajectory.array, expected_array)


def test_minmax():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(steps=array, freq_hz=1)
    minmax_trajectory = trajectory.minmax(0, 255)
    expected_array = np.array([[0.0, 0.0, 0.0], [85.0, 85.0, 85.0], [170.0, 170.0, 170.0], [255.0, 255.0, 255.0]])
    assert np.allclose(minmax_trajectory.array, expected_array)


def test_normalize():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(array, freq_hz=1)
    normalized_trajectory = trajectory.standardize()
    expected_array = np.array(
        [
            [-1.3416407864998738, -1.3416407864998736, -1.3416407864998736],
            [-0.44721359549995787, -0.44721359549995776, -0.44721359549995765],
            [0.44721359549995776, 0.44721359549995776, 0.44721359549995776],
            [1.3416407864998736, 1.3416407864998736, 1.3416407864998736],
        ]
    )
    assert np.allclose(normalized_trajectory.array, expected_array)


def test_unnormalize():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(steps=array, freq_hz=1)
    mean, std = trajectory.mean(), trajectory.std()
    normalized_trajectory = trajectory.standardize()
    unnormalized_trajectory = normalized_trajectory.unstandardize(mean, std).array
    expected_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    assert np.allclose(unnormalized_trajectory, expected_array)


def test_unminmax():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(array, freq_hz=1)
    min, max = trajectory.min(), trajectory.max()
    minmax_trajectory = trajectory.minmax(0, 255)
    norm_min, norm_max = minmax_trajectory.min(), minmax_trajectory.max()
    unminmax_trajectory = minmax_trajectory.unminmax(min, max).array
    expected_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    assert np.allclose(unminmax_trajectory, expected_array)


def pca():
    # Given array
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])

    # Step 1: Center the data
    centered_data = array - np.mean(array, axis=0)

    # Step 2: Compute the covariance matrix
    cov_matrix = np.cov(centered_data.T)

    # Step 3: Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # Step 4: Sort eigenvectors by eigenvalues in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Step 5: Project the data onto the principal components
    pca_transform = centered_data.dot(sorted_eigenvectors)

    # To verify the results, let's check the explained variance ratio
    explained_variance_ratio = sorted_eigenvalues / np.sum(sorted_eigenvalues)


def test_pca():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(array, freq_hz=1)
    pca_trajectory = trajectory.pca(whiten=False)
    expected_array = np.array(
        [
            [-7.79422863, 0.0, -0.0],
            [-2.59807621, 0.0, 0.0],
            [2.59807621, 0.0, 0.0],
            [7.79422863, -0.0, 0.0],
        ]
    )
    pca()

    assert np.allclose(pca_trajectory.array, expected_array)


def test_unpca():
    array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    trajectory = Trajectory(array, freq_hz=1)
    pca_trajectory = trajectory.pca(whiten=False)
    unpca_trajectory = pca_trajectory.unpca().array
    expected_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    assert np.allclose(unpca_trajectory, expected_array)


def test_oned_input_gets_promoted():
    array = np.array([1, 2, 3, 4])
    trajectory = Trajectory(array, freq_hz=1)
    assert np.allclose(trajectory.array, array.reshape(-1, 1))


@pytest.mark.network
def test_plot():
    from embdata.schema.metadata import Metadata
    import pandas as pd
    # logging.basicConfig(level=logging.DEBUG, handlers=[RichHandler()])
    def get_oxe_metadata(dataset_name: str = "utokyo_xarm_pick_and_place_converted_externally_to_rlds") -> Metadata:
        import pandas as pd
        path = files("embdata") / "resources" /"oxe.csv"
        oxe_dataset_metadata = pd.read_csv(path)

        if dataset_name not in oxe_dataset_metadata["Registered Dataset Name"].values:  # noqa: PD011
            raise ValueError(f"Dataset {dataset_name} not found in OXE Overview metadata.")  # noqa

        return Metadata(
            oxe_dataset_metadata[oxe_dataset_metadata["Registered Dataset Name"] == dataset_name].to_dict(
                orient="records"
            )[0]
        )

    from datasets import load_dataset, get_dataset_config_names
    from embdata.episode import Episode
    from embdata.describe import describe
    from embdata.sense.image import Image
    import rich

    repo = "jxu124/OpenX-Embodiment"
    Path("outs").mkdir(exist_ok=True)
    for name in ["bridge", "utokyo_xarm_pick_and_place_converted_externally_to_rlds"]:
        m = get_oxe_metadata(name)
        rich.print(m)
        ds = load_dataset(repo, name, split="train[2:6]")
        describe(ds)
        e = Episode(ds, image_keys=["image"], metadata=m)
        from embdata.sense.video import Video

        e.describe()

        # input("Press Enter to continue...")
        e.trajectory().plot().save(f"outs/{name}.png").show()
        e.trajectory().frequencies().plot().save(f"outs/{name}_frequencies.png").show()
        e.trajectory().pca().save(f"outs/{name}_pca.png").show()
        Video(frames=[Image(step.flatten(include="image")[0]) for step in e.steps], fps=int(m.control_frequency)).save(
            "outs/video.mp4"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
