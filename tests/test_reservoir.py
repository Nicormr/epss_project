import numpy as np
import pandas as pd
import pytest

from epss.eflows import eflow_targets
from epss.reservoir import Reservoir


def series(values):
    return pd.Series(values, index=pd.date_range("2000-01-01", periods=len(values), freq="MS"), dtype=float)


@pytest.fixture
def res():
    hv = pd.DataFrame({"h_m": [0, 5, 10], "v_hm3": [0, 2, 8]})
    return Reservoir(hv, hmax=10, area=1.0)


def test_vmax(res):
    assert res.vmax == 8


def test_level_inverts_volume(res):
    assert np.isclose(res.level(res.volume(7.3)), 7.3)


def test_area_from_hv_curve():
    hv = pd.DataFrame({"h_m": np.arange(0, 10.5, 0.5)})
    hv["v_hm3"] = 0.02 * hv.h_m ** 2                    # A = dV/dh = 0.04 h
    res = Reservoir(hv, hmax=10)
    assert np.isclose(res.area(res.volume(6.0)), 0.24, rtol=0.01)


def test_hand_check():
    # Deck T5: Vmax 10, Vmin 1, V0 8, A = 1 km²
    hv = pd.DataFrame({"h_m": [0, 10], "v_hm3": [0, 10]})
    res = Reservoir(hv, hmax=10, hmin=1, area=1.0)
    sim = res.simulate(series([4, 1, 0.2, 0]), series([100, 150, 200, 200]),
                       series([1, 3, 4, 4]), series([0.5] * 4), v0=8)
    assert np.allclose(sim.volume, [10, 7.35, 3.15, 1.0])
    assert np.allclose(sim.spill, [0.4, 0, 0, 0])
    assert np.allclose(sim.deficit, [0, 0, 0, 2.05])


def test_eflow_targets_by_calendar_month():
    q = series([1, 2] + [0] * 10 + [3, 4] + [0] * 10)
    target = eflow_targets(q, 0.10)
    assert np.isclose(target.iloc[0], 0.2) and np.isclose(target.iloc[13], 0.3)


@pytest.mark.parametrize("area", [0.3, None])
def test_properties_on_random_series(area):
    rng = np.random.default_rng(0)
    n = 240
    hv = pd.DataFrame({"h_m": np.arange(0, 12.5, 0.5)})
    hv["v_hm3"] = 0.01 * hv.h_m ** 2.5
    res = Reservoir(hv, hmax=8, hmin=1, area=area)
    q = series(rng.gamma(0.5, 0.4, n))
    ev = series(rng.uniform(20, 200, n))
    d = series(np.where(np.arange(n) % 12 >= 5, 0.15, 0.0))
    target = eflow_targets(q)
    sim = res.simulate(q, ev, d, target)
    out = sim.eflow + sim.evaporation + sim.supply + sim.spill
    assert np.isclose(sim.volume.iloc[-1] - res.vmax, (sim.inflow - out).sum())     # mass
    assert (sim.volume >= res.vmin - 1e-9).all() and (sim.volume <= res.vmax + 1e-9).all()
    assert np.allclose(sim.volume[sim.spill > 0], res.vmax)                        # spill only when full
    assert np.allclose(sim.eflow, np.minimum(target, q))                           # e-flow rule
