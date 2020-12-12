# Copyright 2020-, Gavin E. Crooks and contributors
#
# This source code is licensed under the Apache License 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

import numpy as np
import pytest
import quantumflow as qf

from qf_diamond_norm import diamond_norm


def test_diamond_norm() -> None:
    # Test cases borrowed from qutip,
    # https://github.com/qutip/qutip/blob/master/qutip/tests/test_metrics.py
    # which were in turn  generated using QuantumUtils for MATLAB
    # (https://goo.gl/oWXhO9)

    RTOL = 0.01
    chan0 = qf.I(0).aschannel()
    chan1 = qf.X(0).aschannel()
    dn = diamond_norm(chan0, chan1)
    assert np.isclose(2.0, dn, rtol=RTOL)

    turns_dnorm = [
        [1.000000e-03, 3.141591e-03],
        [3.100000e-03, 9.738899e-03],
        [1.000000e-02, 3.141463e-02],
        [3.100000e-02, 9.735089e-02],
        [1.000000e-01, 3.128689e-01],
        [3.100000e-01, 9.358596e-01],
    ]

    for turns, target in turns_dnorm:
        chan0 = qf.XPow(0.0, 0).aschannel()
        chan1 = qf.XPow(turns, 0).aschannel()

        dn = diamond_norm(chan0, chan1)
        assert np.isclose(target, dn, rtol=RTOL)

    hadamard_mixtures = [
        [1.000000e-03, 2.000000e-03],
        [3.100000e-03, 6.200000e-03],
        [1.000000e-02, 2.000000e-02],
        [3.100000e-02, 6.200000e-02],
        [1.000000e-01, 2.000000e-01],
        [3.100000e-01, 6.200000e-01],
    ]

    for p, target in hadamard_mixtures:
        tensor = qf.I(0).aschannel().tensor * (1 - p) + qf.H(0).aschannel().tensor * p
        chan0 = qf.Channel(tensor, [0])

        chan1 = qf.I(0).aschannel()

        dn = diamond_norm(chan0, chan1)
        assert np.isclose(dn, target, rtol=RTOL)

    chan0 = qf.YPow(0.5, 0).aschannel()
    chan1 = qf.I(0).aschannel()
    dn = diamond_norm(chan0, chan1)
    assert np.isclose(dn, np.sqrt(2), rtol=RTOL)

    chan0 = qf.CNot(0, 1).aschannel()
    chan1 = qf.CNot(1, 0).aschannel()
    diamond_norm(chan0, chan1)


def test_diamond_norm_err() -> None:
    with pytest.raises(ValueError):
        chan0 = qf.I(0).aschannel()
        chan1 = qf.I(1).aschannel()
        diamond_norm(chan0, chan1)


# fin
