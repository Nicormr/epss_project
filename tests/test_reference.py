"""Compare the package with the reference case in data/reference (synthetic climate)."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from epss.eflows import eflow_targets
from epss.metrics import reliability_time, reliability_volume, required_hmax
from epss.pet import pet_monthly
from epss.reservoir import Reservoir
from epss.soil import thornthwaite_mather

DATA = Path(__file__).parents[1] / "data"
REF = DATA / "reference"


@pytest.fixture(scope="module")
def case():
    inp = pd.read_csv(REF / "inputs.csv", index_col=0, parse_dates=True)
    par = json.loads((REF / "params.json").read_text())
    exp = pd.read_csv(REF / "expected_catchment.csv", index_col=0, parse_dates=True)
    return inp, par, exp


def test_catchment(case):
    inp, par, exp = case
    pet = pet_monthly(inp.t_c, inp.tmax_c, inp.tmin_c, par["latitude_deg"])
    tm = thornthwaite_mather(inp.p_mm, pet, par["smax_mm"])
    for col in ["pet", "aet", "soil", "runoff"]:
        np.testing.assert_allclose(tm[col], exp[col], rtol=1e-6, atol=1e-9)


@pytest.mark.parametrize("name", ["fixed", "variable"])
def test_simulation(case, name):
    inp, par, exp = case
    area = par["area_fixed_km2"] if name == "fixed" else None
    hv = pd.read_csv(DATA / "hv_curve.csv")
    sim = Reservoir(hv, par["hmax_m"], par["hmin_m"], area).simulate(exp.inflow, exp.pet, exp.demand, exp.eflow_target)
    ref = pd.read_csv(REF / f"expected_simulation_{name}.csv", index_col=0, parse_dates=True)
    for col in ref.columns:
        np.testing.assert_allclose(sim[col], ref[col], rtol=1e-6, atol=1e-9)
    met = json.loads((REF / "expected_metrics.json").read_text())[name]
    assert np.isclose(reliability_time(sim), met["Rt"]) and np.isclose(reliability_volume(sim), met["Rv"])


def test_required_hmax(case):
    inp, par, exp = case
    hv = pd.read_csv(DATA / "hv_curve.csv")
    h = required_hmax(hv, exp.inflow, exp.pet, exp.demand, eflow_targets(exp.inflow, par["eflow_fraction"]),
                      par["target_reliability"], par["hmin_m"])
    assert np.isclose(h, json.loads((REF / "expected_metrics.json").read_text())["required_hmax_m"], atol=0.02)
