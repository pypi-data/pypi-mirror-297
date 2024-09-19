"""Functions that calculate log spirals and their residuals."""

from typing import TypeVar

import numpy as np
from numpy.typing import NDArray

FloatType = TypeVar("FloatType", np.float32, np.float64)


def log_spiral(
    theta: NDArray[FloatType],
    offset: float,
    growth_factor: float,
    initial_radius: float,
    *,
    use_modulo: bool,
) -> NDArray[FloatType]:
    """Calculate the radius of a log spiral given parameters and theta.

    Parameters
    ----------
    theta : NDArray[FloatType]
        The polar angle of the log spiral in radians.
    offset : float
        The offset angle in radians.
    growth_factor : float
        The growth factor.
    initial_radius : float
        The initial radius in pixels.
    use_modulo : bool
        Set this flag to apply the modulo operator to the angles before computing the radii.

    """
    angles = theta - offset
    if use_modulo:
        angles %= 2 * np.pi
    result: NDArray[FloatType] = np.multiply(initial_radius, np.exp(np.multiply(-growth_factor, angles)))
    return result


def calculate_log_spiral_residual_vector(
    radii: NDArray[FloatType],
    theta: NDArray[FloatType],
    weights: NDArray[FloatType],
    offset: float,
    growth_factor: float,
    initial_radius: float,
    *,
    use_modulo: bool,
) -> NDArray[FloatType]:
    """Calculate the residuals of a log spiral with respect to a cluster.

    Parameters
    ----------
    radii : NDArray[FloatType]
        The polar radii of the cluster's pixels in pixels.
    theta : NDArray[FloatType]
        The polar angle of the cluster's pixels in radians.
    weights : NDArray[FloatType]
        The weights of the cluster's pixels in pixels.
    offset : float
        The offset angle in radians.
    growth_factor : float
        The growth factor.
    initial_radius : float
        The initial radius in pixels.
    use_modulo : bool
        Set this flag to apply the modulo operator to the angles before computing the radii.

    Returns
    -------
    NDArray[FloatType]
        The residual associated with each pixel in the cluster.

    """
    return np.multiply(
        np.sqrt(weights),
        (radii - log_spiral(theta, offset, growth_factor, initial_radius, use_modulo=use_modulo)),
    )


def calculate_log_spiral_error(
    radii: NDArray[FloatType],
    theta: NDArray[FloatType],
    weights: NDArray[FloatType],
    offset: float,
    growth_factor: float,
    initial_radius: float,
    *,
    use_modulo: bool,
) -> tuple[float, NDArray[FloatType]]:
    """Calculate the sum of square residuals of a log spiral with respect to a cluster.

    Parameters
    ----------
    radii : NDArray[FloatType]
        The polar radii of the cluster's pixels in pixels.
    theta : NDArray[FloatType]
        The polar angle of the cluster's pixels in radians.
    weights : NDArray[FloatType]
        The weights of the cluster's pixels in pixels.
    offset : float
        The offset angle in radians.
    growth_factor : float
        The growth factor.
    initial_radius : float
        The initial radius in pixels.
    use_modulo : bool
        Set this flag to apply the modulo operator to the angles before computing the radii.

    Returns
    -------
    float
        The sum of square residuals.
    NDArray[FloatType]
        The residual associated with each pixel in the cluster.

    """
    residuals = calculate_log_spiral_residual_vector(
        radii,
        theta,
        weights,
        offset,
        growth_factor,
        initial_radius,
        use_modulo=use_modulo,
    )
    sum_square_error = np.sum(np.square(residuals))
    return (sum_square_error, residuals)


def calculate_log_spiral_error_from_growth_factor(
    growth_factor: float,
    radii: NDArray[FloatType],
    theta: NDArray[FloatType],
    weights: NDArray[FloatType],
    offset: float,
    *,
    use_modulo: bool,
) -> NDArray[FloatType]:
    """Return the residuals of a log spiral fit to the given cluster.

    This function automatically determines the optimal initial radius given an offset and the growth factor.

    Parameters
    ----------
    growth_factor : float
        The growth factor.
    radii : NDArray[FloatType]
        The polar radii of the cluster's pixels in pixels.
    theta : NDArray[FloatType]
        The polar angle of the cluster's pixels in radians.
    weights : NDArray[FloatType]
        The weights of the cluster's pixels in pixels.
    offset : float
        The offset angle in radians.
    initial_radius : float
        The initial radius in pixels.
    use_modulo : bool
        Set this flag to apply the modulo operator to the angles before computing the radii.

    Returns
    -------
    NDArray[FloatType]
        The residual associated with each pixel in the cluster.

    """
    initial_radius = calculate_best_initial_radius(radii, theta, weights, offset, growth_factor, use_modulo=use_modulo)
    return calculate_log_spiral_residual_vector(
        radii,
        theta,
        weights,
        offset,
        growth_factor,
        initial_radius,
        use_modulo=use_modulo,
    )


def calculate_best_initial_radius(
    radii: NDArray[FloatType],
    theta: NDArray[FloatType],
    weights: NDArray[FloatType],
    offset: float,
    growth_factor: float,
    *,
    use_modulo: bool,
) -> float:
    """Determine the most optimal initial radius given a growth factor and offset.

    This function automatically determines the optimal initial radius given an offset and growth factor.

    Parameters
    ----------
    radii : NDArray[FloatType]
        The polar radii of the cluster's pixels in pixels.
    theta : NDArray[FloatType]
        The polar angle of the cluster's pixels in radians.
    weights : NDArray[FloatType]
        The weights of the cluster's pixels in pixels.
    offset : float
        The offset angle in radians.
    growth_factor : float
        The growth factor.
    use_modulo : bool
        Set this flag to apply the modulo operator to the angles before computing the radii.

    Returns
    -------
    float
        The optimal initial radius.

    """
    log_spiral_term = log_spiral(theta, offset, growth_factor, 1, use_modulo=use_modulo)
    return float(np.sum(radii * weights * log_spiral_term) / np.sum(weights * np.square(log_spiral_term)))
