# -*- coding: utf-8 -*-
"""
Test the static solver.

@author: ricriv
"""

# Here we are relying on the default behavior of pytest, which is to execute
# the tests in the same order that they are specified.
# If one day this will not be the case anymore, we can enforce the order by
# using the solution proposed at: https://stackoverflow.com/a/77793427/3676517

import pytest

import numpy as np
from numpy import testing as npt

from h2lib._h2lib import H2Lib
from h2lib_tests.test_files import tfp

from .test_write_htc import (
    write_dtu10mw_only_blade,
    write_dtu10mw_only_blade_low_max_iter,
)


@pytest.fixture(scope="module")
def h2_dtu_10mw_only_blade(write_dtu10mw_only_blade):
    h2 = H2Lib(suppress_output=True)
    model_path = f"{tfp}DTU_10_MW/"
    htc_path = "htc/DTU_10MW_RWT_only_blade.htc"
    h2.init(htc_path=htc_path, model_path=model_path)
    yield h2
    h2.close()


@pytest.fixture(scope="module")
def h2_dtu10mw_only_blade_low_max_iter(write_dtu10mw_only_blade_low_max_iter):
    h2 = H2Lib(suppress_output=True)
    model_path = f"{tfp}DTU_10_MW/"
    htc_path = "htc/DTU_10MW_RWT_only_blade_low_max_iter.htc"
    h2.init(htc_path=htc_path, model_path=model_path)
    yield h2
    h2.close()


def test_solver_static_update_no_init(h2_dtu_10mw_only_blade):
    with pytest.raises(RuntimeError, match="STATIC_SOLVER_NOT_INITIALIZED"):
        h2_dtu_10mw_only_blade.solver_static_update()


def test_solver_static_solve_no_init(h2_dtu_10mw_only_blade):
    with pytest.raises(RuntimeError, match="STATIC_SOLVER_NOT_INITIALIZED"):
        h2_dtu_10mw_only_blade.solver_static_solve()


def test_solver_static_init(h2_dtu_10mw_only_blade):

    # First execution is fine.
    h2_dtu_10mw_only_blade.solver_static_init()

    # The next should automatically deallocate the static solver and initialize it again.
    h2_dtu_10mw_only_blade.solver_static_init()


def test_solver_static_update(h2_dtu_10mw_only_blade):
    # This should happen after test_solver_static_init().
    h2_dtu_10mw_only_blade.solver_static_update()


def test_solver_static_solve(h2_dtu_10mw_only_blade):
    # This should happen after test_solver_static_update().
    h2_dtu_10mw_only_blade.solver_static_solve()


def test_solver_static_delete(h2_dtu_10mw_only_blade):
    h2_dtu_10mw_only_blade.solver_static_delete()


def test_static_solver_run(h2_dtu_10mw_only_blade):
    # Add a sensor for the blade root moment, in this case only due to gravity.
    id = h2_dtu_10mw_only_blade.add_sensor("mbdy momentvec blade1 1 1 blade1")

    # Run the static solver.
    h2_dtu_10mw_only_blade.solver_static_run()

    # Do 1 step to get the output.
    h2_dtu_10mw_only_blade.step()
    val = h2_dtu_10mw_only_blade.get_sensor_values(id)
    # Test against: initial_condition 2; followed by time simulaiton.
    npt.assert_allclose(
        val, np.array([-1.07213851e04, -4.55385871e-02, -3.94623708e01])
    )


def test_static_solver_run_fail(h2_dtu10mw_only_blade_low_max_iter):
    with pytest.raises(RuntimeError, match="STATIC_SOLVER_DID_NOT_CONVERGE"):
        h2_dtu10mw_only_blade_low_max_iter.solver_static_run()
