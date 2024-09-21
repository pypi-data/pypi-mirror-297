import logging

import numpy as np
import pandas as pd
import sympy

from copul.checkerboard.biv_check_pi import BivCheckPi
from copul.wrapper.sympy_wrapper import SymPyFuncWrapper

log = logging.getLogger(__name__)


class Checkerboarder:
    def __init__(self, nrow=10, ncol=None):
        self.nrow = nrow
        self.ncol = ncol if ncol is not None else self.nrow

    def compute_check_copula(self, copula):
        log.debug("Computing checkerboard copula...")
        if isinstance(copula.cdf, SymPyFuncWrapper):
            cdf = sympy.lambdify([copula.u, copula.v], copula.cdf.func, ["numpy"])
        else:

            def cdf(u, v):
                return copula.cdf(u, v)

        nrow = self.nrow
        ncol = self.ncol
        cmatr = sympy.Matrix.zeros(nrow, ncol)
        for i, j in np.ndindex(nrow, ncol):
            if i == 0:
                if j == 0:
                    cmatr[i, j] = cdf(1 / nrow, 1 / ncol)
                else:
                    cmatr[i, j] = cdf(1 / nrow, (j + 1) / ncol) - cdf(
                        1 / nrow, j / ncol
                    )
            elif j == 0:
                cmatr[i, j] = cdf((i + 1) / nrow, 1 / ncol) - cdf(i / nrow, 1 / ncol)
            else:
                cmatr[i, j] = (
                    cdf((i + 1) / nrow, (j + 1) / ncol)
                    + cdf(i / nrow, j / ncol)
                    - cdf(i / nrow, (j + 1) / ncol)
                    - cdf((i + 1) / nrow, j / ncol)
                )
        return BivCheckPi(cmatr)

    def from_data(self, data: pd.DataFrame):
        # transform each column to ranks
        for col in data.columns:
            data[col] = data[col].rank(pct=True)
        n_obs = len(data)
        data = data.sort_values(by=data.columns[0])
        checkerboard_matr = sympy.Matrix.zeros(self.nrow, self.ncol)
        for i in range(self.nrow):
            for j in range(self.ncol):
                # count rows in the i-th and j-th quantile
                n_ij = len(
                    data[
                        (data[data.columns[0]] >= i / self.nrow)
                        & (data[data.columns[0]] < (i + 1) / self.nrow)
                        & (data[data.columns[1]] >= j / self.ncol)
                        & (data[data.columns[1]] < (j + 1) / self.ncol)
                    ]
                )
                checkerboard_matr[i, j] = n_ij / n_obs
        return BivCheckPi(checkerboard_matr)
