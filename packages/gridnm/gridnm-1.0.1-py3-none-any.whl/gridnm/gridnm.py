from typing import Callable, List, Tuple, Union
from warnings import warn

import numpy as np
import numpy.typing as npt
from numpy.linalg import norm
from scipy.optimize import OptimizeResult  # type: ignore


# Custom types
anyfloat = Union[float, np.float64]


# SciPy Status messages
STATUS_MESSAGE = {
    "success": "Optimization terminated successfully.",
    "failure": "Optimization did not converge to desired accuracy.",
    "maxfev": "Maximum number of function evaluations has been exceeded.",
    "maxiter": "Maximum number of iterations has been exceeded.",
}


def simplex_from_point(
    x: npt.NDArray[np.float64], d_rel: anyfloat = 0.0, d_abs: anyfloat = 0.1
) -> npt.NDArray[np.float64]:
    """
    Construct simplex from point using relative shift size 'd_rel' and absolute shift size 'd_abs'.
    """
    D = np.diag(np.abs(x) * d_rel + d_abs)
    return np.vstack((x, x + D))


class GridNM:
    """
    Grid restrained variant of the Nelder-Mead algorithm that, in contrast to the original
    Nelder-Mead algorithm, provably converges to a stationary point. See [1] for details.

    This implemenation was done from scratch based on the pseudo code in [1]. The MATLAB
    implementation [2] by the authors of [1] and the PyOPUS implementation [3] were used for
    reference. Variable names and default values were taken from [1].

    [1] Bűrmen, Árpád & Puhan, Janez & Tuma, Tadej. (2006). Grid Restrained Nelder-Mead Algorithm.
        Computational Optimization and Applications. 34. 359-375. 10.1007/s10589-005-3912-z.

    [2] https://fides.fe.uni-lj.si/~arpadb/software-grnm.html

    [3] http://spiceopus.si/pyopus/doc/optimizer.grnm.html?highlight=grnm#module-pyopus.optimizer.grnm

    [4] Gao, F. and Han, L. Implementing the Nelder-Mead simplex algorithm with adaptive
        parameters. 2012. Computational Optimization and Applications. 51:1, pp. 259-277
    """

    def __init__(
        self,
        func: Callable[[npt.NDArray[np.float64]], anyfloat],
        x0: npt.NDArray[np.float64] | List,
        maxiter: int | float = np.inf,
        maxfev: int | float = np.inf,
        verbosity: int = 0,
        initial_simplex: npt.NDArray[np.float64] | None = None,
        xatol: anyfloat = 1e-4,
        xrtol: anyfloat = 1e-4,
        fatol: float = 0.0,
        frtol: float = 0.0,
        adaptive: bool = True,
    ) -> None:
        """
        Initialize new instance of grid restrained Nelder-Mead optimizer.

        func:            cost function
        x0:              initial point
        maxiter:         maximum number of iterations (Nelder-Mead steps)
        maxfev:          maximum number of function evaluations
        verbosity:       0: silent
                         1: print non-standard operations (reshape, pseudo expansion, etc.)
                         2: also print current minimum at each iteration
                         3: also print current simplex at each iteration
        initial_simplex: initial simplex, constructed from x0 if not specified
        [fx][ar]tol:     absolute/relative stopping tolerances for x and func(x)
        adaptive:        use adaptive simmplex parameters; see [4] for details.
        """
        # Opt problem properties
        self.dim = len(x0)
        self.func = func
        self.verbosity = verbosity
        self.maxiter = maxiter
        self.maxfev = maxfev

        # Initial simplex
        if initial_simplex is None:
            x0 = np.atleast_1d(x0).flatten()
            x0 = np.asarray(x0, np.float64)
            S = simplex_from_point(x0)
        else:
            S = np.atleast_2d(initial_simplex).copy()
            S = np.asarray(S, np.float64)
            if S.ndim != 2 or S.shape[0] != S.shape[1] + 1:
                raise ValueError("'initial_simplex' should be an array of shape (N+1, N)")
            if len(x0) != S.shape[1]:
                raise ValueError("Size of 'initial_simplex' is not consistent with 'x0'")
        self.S = S
        self.D = self.S[1:] - self.S[0]
        self.f = np.array([self.func(x) for x in self.S])

        # Counters
        self.nit = 0
        self.nfev = self.f.size
        self.nreshape = 0
        self.nmsteps = 0

        # Stopping tolerances
        self.fatol = fatol
        self.frtol = frtol
        self.xatol = xatol
        self.xrtol = xrtol

        # Simplex update parameters
        if adaptive:
            self.gamma_r = 1.0
            self.gamma_e = 1.0 + 2 / self.dim
            self.gamma_c = 0.75 - 1 / (2 * self.dim)
            self.gamma_p = 1.0 - 1 / self.dim
        else:
            self.gamma_r = 1.0
            self.gamma_e = 1.2
            self.gamma_c = 0.5
            self.gamma_p = 0.25

        # Simplex shape parameters
        self.shapefact = 1e-6
        self.normfact = 2.0
        self.normfactmax = 2**52

        # Grid parameters
        self.gridorigin = x0
        self.gridsize = np.zeros(self.dim)
        self.gridnorm = 0
        self.gridrtol = 2**-52
        self.gridatol = 1e-100
        self.update_grid(np.full(self.dim, norm(self.D.diagonal(), ord=-np.inf) / 10))

    def eval_func(self, x: npt.NDArray[np.float64]) -> anyfloat:
        """
        Evaluate cost function at 'x' and increase nfev counter.
        Display progress based on 'verbosity'.
        """
        self.nfev += 1
        f = self.func(x)
        if np.isnan(f):
            warn("NaN value encountered")
        if self.verbosity > 1:
            print_simplex = f", simplex =\n{self.S}" if self.verbosity > 2 else ""
            print(f"nfev = {self.nfev}, f_min = {self.f[0]}{print_simplex}")
        return f

    def converged(self) -> np.bool_:
        """
        Check if simplex satisfies stopping criteria.
        """
        # Get best vertex
        idx_min = np.argmin(self.f)
        f_min = self.f[idx_min]
        s_min = self.S[idx_min]
        # Get differences
        fdiff = np.max(self.f) - f_min
        xdiff = norm(self.S[1:] - self.S[0], ord=np.inf, axis=0)
        # Get tolerances
        ftol = np.maximum(np.abs(f_min) * self.frtol, self.fatol)
        xtol = np.maximum(np.abs(s_min) * self.xrtol, self.xatol)
        # Check condition
        return fdiff <= ftol or np.all(xdiff <= xtol)

    def get_optimize_result(self) -> OptimizeResult:
        """
        Construct SciPy OptimizeResult object with current state of the algorithm.
        """
        # Make sure simplex is sorted
        self.sort_simplex()
        converged = self.converged()
        warnflag = 0
        if self.nfev >= self.maxfev:
            warnflag = 1
            msg = STATUS_MESSAGE["maxfev"]
            if self.verbosity > 0:
                warn(msg)
        elif self.nit >= self.maxiter:
            warnflag = 2
            msg = STATUS_MESSAGE["maxiter"]
            if self.verbosity > 0:
                warn(msg)
        elif not converged:
            warnflag = 3
            msg = STATUS_MESSAGE["failure"]
            if self.verbosity > 0:
                warn(msg)
        else:
            msg = STATUS_MESSAGE["success"]
        return OptimizeResult(
            {
                "x": self.S[0],
                "success": converged,
                "status": warnflag,
                "message": msg,
                "fun": self.f[0],
                "nfev": self.nfev,
                "nit": self.nit,
                "final_simplex": self.S,
            }
        )

    def project_to_grid(self, x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """
        Round point 'x' to closest grid point.
        """
        n = np.round((x - self.gridorigin) / self.gridsize)
        return self.gridorigin + n * self.gridsize

    def sort_simplex(self) -> None:
        """
        Sort simplex vertices by cost function value in increasing order.
        """
        sorted_idx = np.argsort(self.f)
        self.f = self.f[sorted_idx]
        self.S = self.S[sorted_idx]

    def eval_simplex(self, offset: int = 0):
        """
        Evaluate cost function at simplex vertices, skip first 'offset' vertices.
        'offset' can be used to avoid re-evaluating the best vertex, which is left
        unchanged during the 'rebase' step.
        """
        self.f[offset:] = np.array([self.eval_func(x) for x in self.S[offset:]])

    def replace_vertex(self, f: anyfloat, x: npt.NDArray[np.float64], idx: int = -1):
        """
        Replace vertex at 'idx' with new point 'x' and value 'f'.
        """
        self.f[idx] = f
        self.S[idx] = x

    def check_simplex_shape(self) -> Tuple[np.bool_, npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """
        Check for bad simplex shape. Return Q and diagonal of R of the QR decomposition
        since they are needed for the 'rebase' step.
        """
        D = self.S[1:] - self.S[0]
        idx_sorted = np.flip(np.argsort(norm(D, ord=2, axis=1)))
        # Use sorted and transposed (!) D for QR decomposition
        # We want D to be a column matrix, by default it is a row matrix
        Q, R = np.linalg.qr(D[idx_sorted].T)
        r = R.diagonal()
        bad_shape = norm(r, ord=-np.inf) < self.shapefact * self.gridnorm
        if bad_shape and self.verbosity > 0:
            print("bad simplex shape")
        return bad_shape, r, Q

    def rebase_simplex(self, r: npt.NDArray[np.float64], Q: npt.NDArray[np.float64]) -> None:
        """
        Update basis to colums of Q matrix, weighted by (clipped) values in r.
        """
        if self.verbosity > 0:
            print("updating basis")
        sign_r = 2 * (r >= 0) - 1
        r_clipped = sign_r * np.clip(np.abs(r), self.normfact * self.gridnorm, self.normfactmax * self.gridnorm)
        D = Q @ np.diag(r_clipped)
        # We need to revert the transposition in check_simplex_shape
        self.D = D.T

    def reshape_simplex(self) -> None:
        """
        Reshape simplex using basis D and increase counter.
        """
        if self.verbosity > 0:
            print("reshaping simplex")
        self.S[1:] = np.array([self.project_to_grid(self.S[0] + d) for d in self.D])
        self.nreshape += 1

    def pseudo_expansion(self) -> bool:
        """
        Try pseudo expansion and return whether it was successful.
        """
        # Get pseudo expansion point and function value
        xcw = np.mean(self.S[1:], axis=0)  # centroid of n worst vertices
        xpe = self.S[0] + (self.gamma_e / self.gamma_r - 1) * (self.S[0] - xcw)
        xpe = self.project_to_grid(xpe)
        fpe = self.eval_func(xpe)

        # Pseudo expansion was successful
        if fpe < self.f[0]:
            if self.verbosity > 0:
                print("pseudo expansion successful")
            self.replace_vertex(fpe, xpe, 0)
            return True

        # Pseudo expansion failed
        if self.verbosity > 0:
            print("pseudo expansion failed")
        return False

    def update_grid(self, gridsize: npt.NDArray[np.float64], origin: npt.NDArray[np.float64] | None = None):
        """
        Update grid size, origin, and grid norm.
        """
        if origin is not None:
            self.gridorigin = origin
        gridtol = np.maximum(np.abs(self.gridorigin) * self.gridrtol, self.gridatol)
        self.gridsize = np.maximum(gridtol, gridsize)
        self.gridnorm = np.sqrt(self.dim) * norm(self.gridsize, ord=2) / 2

    def refine_grid(self) -> None:
        """
        Refine grid if necessary.
        """
        Dnorm = norm(self.D, ord=2, axis=1)
        idx_min = np.argmin(Dnorm)
        Dmin = np.abs(self.D[idx_min])
        dmin = Dnorm[idx_min]
        if dmin < self.normfact * self.gridnorm:
            if self.verbosity > 0:
                print("refining grid")
            gridsize_max = np.maximum(Dmin / self.dim, dmin / self.dim ** (3 / 2)) / (250 * self.normfact)
            gridsize_new = np.minimum(self.gridsize, gridsize_max)
            self.update_grid(gridsize_new, self.S[0])

    def nm_iteration(self) -> bool:
        """
        Single iteration of Nelder-Mead algorithm with strict acceptance rule (< instead of <=)
        and no shrinkage.
        """
        # Sort simplex
        self.sort_simplex()

        # Get best, worst and second worst point
        fb, fw, fsw = self.f[0], self.f[-1], self.f[-2]
        xw = self.S[-1]

        # Set failure flag to 0
        success = True

        # Try reflection
        xc = np.mean(self.S[:-1], axis=0)  # centroid of n best points
        xr = self.project_to_grid(xc - self.gamma_r * (xw - xc))
        fr = self.eval_func(xr)

        if fr < fsw:
            if fb <= fr:
                self.replace_vertex(fr, xr)
            else:
                # Try expansion
                xe = self.project_to_grid(xc - self.gamma_e * (xw - xc))
                fe = self.eval_func(xe)
                if fe < fr:
                    self.replace_vertex(fe, xe)
                else:
                    self.replace_vertex(fr, xr)
        else:
            if fr >= fw:
                # Try inner contraction
                xci = self.project_to_grid(xc + self.gamma_c * (xw - xc))
                fci = self.eval_func(xci)
                if fci < fsw:
                    self.replace_vertex(fci, xci)
                else:
                    success = False
            else:
                # Try outer contraction
                xco = self.project_to_grid(xc - self.gamma_c * (xw - xc))
                fco = self.eval_func(xco)
                if fco < fsw:
                    self.replace_vertex(fco, xco)
                else:
                    success = False

        self.nit += 1
        return success

    def solve(self) -> OptimizeResult:
        """
        Run grid-constrained Nelder-Mead algorithm until converged or
        number of iterations exceed bounds.
        """
        while self.nit < self.maxiter and self.nfev < self.maxfev and not self.converged():
            # Reset reshape counter
            self.nreshape = 0

            # Run standard NM until progress stops
            while self.nm_iteration():
                pass

            # Check for bad shape and reshape if necessary
            bad_shape, r, Q = self.check_simplex_shape()
            if bad_shape:
                self.rebase_simplex(r, Q)
                self.reshape_simplex()
                self.eval_simplex(1)

            # Try pseudo expansion
            if self.pseudo_expansion():
                continue

            # Make sure simplex is reshaped before shrinking
            if self.nreshape == 0:
                self.rebase_simplex(r, Q)
                self.reshape_simplex()
                self.eval_simplex(1)

            # Shrink until improved or converged
            while np.min(self.f[1:]) >= self.f[0]:
                if self.nreshape % 2 == 0:
                    # Minimal positive basis found, return if converged
                    if self.converged():
                        break
                    # Otherwise shrink basis and refine grid if necessary
                    if self.verbosity > 0:
                        print("shrinking basis")
                    self.D *= self.gamma_p
                    self.refine_grid()

                # Flip basis and evaluate simplex
                self.D *= -1
                self.reshape_simplex()
                self.eval_simplex(1)

        return self.get_optimize_result()
