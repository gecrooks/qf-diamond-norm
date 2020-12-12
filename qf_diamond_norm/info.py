# Copyright 2020-, Gavin E. Crooks and contributors
#
# This source code is licensed under the Apache License 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.


"""
====================
Information Measures
====================

Channel Measures
#################

.. autofunction:: diamond_norm
"""

import numpy as np
from quantumflow import Channel

__all__ = ("diamond_norm",)


def diamond_norm(chan0: Channel, chan1: Channel) -> float:
    """Return the diamond norm between two completely positive
    trace-preserving (CPTP) superoperators.

    Note: Requires "cvxpy" package (and dependencies) to be fully installed.

    The calculation uses the simplified semidefinite program of Watrous
    [arXiv:0901.4709](http://arxiv.org/abs/0901.4709)
    [J. Watrous, [Theory of Computing 5, 11, pp. 217-238
    (2009)](http://theoryofcomputing.org/articles/v005a011/)]
    """
    # Kudos: Based on MatLab code written by Marcus P. da Silva
    # (https://github.com/BBN-Q/matlab-diamond-norm/)
    import cvxpy as cvx

    if set(chan0.qubits) != set(chan1.qubits):
        raise ValueError("Channels must operate on same qubits")

    if chan0.qubits != chan1.qubits:
        chan1 = chan1.permute(chan0.qubits)

    N = chan0.qubit_nb
    dim = 2 ** N

    choi0 = chan0.choi()
    choi1 = chan1.choi()

    delta_choi = choi0 - choi1

    # Density matrix must be Hermitian, positive semidefinite, trace 1
    rho = cvx.Variable([dim, dim], complex=True)
    constraints = [rho == rho.H]
    constraints += [rho >> 0]
    constraints += [cvx.trace(rho) == 1]

    # W must be Hermitian, positive semidefinite
    W = cvx.Variable([dim ** 2, dim ** 2], complex=True)
    constraints += [W == W.H]
    constraints += [W >> 0]

    constraints += [(W - cvx.kron(np.eye(dim), rho)) << 0]

    J = cvx.Parameter([dim ** 2, dim ** 2], complex=True)
    objective = cvx.Maximize(cvx.real(cvx.trace(J.H * W)))

    prob = cvx.Problem(objective, constraints)

    J.value = delta_choi
    prob.solve()

    dnorm = prob.value * 2

    # Diamond norm is between 0 and 2. Correct for floating point errors
    dnorm = min(2, dnorm)
    dnorm = max(0, dnorm)

    return dnorm


# fin
