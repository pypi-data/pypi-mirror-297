import numpy as np
import numpy.typing as npt
import pytest

from scipy.optimize import rosen  # type: ignore

from ..src.gridnm import GridNM


def mckinnon(x: npt.NDArray[np.float64], theta: float = 6, phi: float = 60, w: float = 2) -> np.float64:
    """
    McKinnon function for which the regular Nelder-Mead algorithm can be
    initialized such that it does not converge to a stationary point.
    """
    if x[0] < 0:
        return theta * phi * np.abs(x[0]) ** w + x[1] + x[1] ** 2
    else:
        return theta * x[0] ** w + x[1] + x[1] ** 2


### Tests ###


def test_rosenbrock_2d() -> None:
    """
    2D Rosenbrock function
    """
    x0 = np.array([-1.2, 1])
    xopt = np.ones(2)
    gridnm = GridNM(rosen, x0)
    sol = gridnm.solve()
    np.testing.assert_allclose(sol.x, xopt, float(gridnm.xrtol), float(gridnm.xatol))
    assert sol.nfev < 500


def test_rosenbrock_8d() -> None:
    """
    8D extended Rosenbrock function
    """
    x0 = np.zeros(8)
    xopt = np.ones(8)
    gridnm = GridNM(rosen, x0)
    sol = gridnm.solve()
    np.testing.assert_allclose(sol.x, xopt, float(gridnm.xrtol), float(gridnm.xatol))
    assert sol.nfev < 3000


def test_mckinnon() -> None:
    """
    McKinnon function with initial simplex chosen such that the regular
    Nelder-Mead algorithm does does converge to a stationary point
    """
    x0 = np.array([(1 + np.sqrt(33)) / 8, (1 - np.sqrt(33)) / 8])
    S0 = np.array([[1.0, 1.0], x0, [0.0, 0.0]])
    xopt = np.array([0.0, -0.5])
    gridnm = GridNM(mckinnon, x0, initial_simplex=S0)
    sol = gridnm.solve()
    np.testing.assert_allclose(sol.x, xopt, float(gridnm.xrtol), float(gridnm.xatol))
    assert sol.nfev < 300
