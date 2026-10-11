import numpy as np
import pytest
from publication_reconstruction.noise_model import add_relative_gaussian_noise

def test_reproducible_and_input_not_mutated():
    reference = np.array([1.0, 2.0, -4.0, 0.0])
    original = reference.copy()
    a = add_relative_gaussian_noise(reference, seed=19)
    b = add_relative_gaussian_noise(reference, seed=19)
    np.testing.assert_array_equal(a, b)
    np.testing.assert_array_equal(reference, original)
    assert a[-1] == 0.0

def test_noise_output_shape_and_finiteness():
    reference = np.array([1.0, 10.0, 100.0])
    result = add_relative_gaussian_noise(reference, relative_sigma=0.013, seed=5)
    assert result.shape == reference.shape
    assert np.all(np.isfinite(result))
    assert not np.array_equal(result, reference)

def test_zero_scale_requires_explicit_positive_scale():
    with pytest.raises(ValueError):
        add_relative_gaussian_noise([0.0], zero_policy="scale")
    result = add_relative_gaussian_noise([0.0], zero_policy="scale", zero_scale=2.0, seed=4)
    assert result[0] != 0.0

def test_invalid_inputs_rejected():
    with pytest.raises(ValueError):
        add_relative_gaussian_noise([np.nan])
    with pytest.raises(ValueError):
        add_relative_gaussian_noise([1.0], relative_sigma=-0.1)
