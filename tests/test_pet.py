import numpy as np
import pandas as pd

from epss.pet import extraterrestrial_radiation, hargreaves, pet_monthly


def test_ra_fao56_example_8():
    # FAO-56 example 8: 20 °S, 3 September (J = 246) -> Ra = 32.2 MJ m-2 day-1
    assert np.isclose(extraterrestrial_radiation(-20, 246), 32.2, atol=0.1)


def test_no_temperature_range_no_pet():
    assert hargreaves(20, 20, 20, ra=15) == 0


def test_hargreaves_known_value():
    expected = 0.0023 * 15 * (20 + 17.8) * 14 ** 0.5
    assert np.isclose(hargreaves(tmean=20, tmax=27, tmin=13, ra=15), expected)


def test_pet_monthly_uses_day_15_and_days_in_month():
    idx = pd.date_range("2001-07-01", periods=1, freq="MS")
    t, tx, tn = (pd.Series([v], index=idx) for v in (25.0, 33.0, 17.0))
    ra = 0.408 * extraterrestrial_radiation(38.0, 196)          # 15 July
    expected = 0.0023 * ra * (25 + 17.8) * 4.0 * 31
    assert np.isclose(pet_monthly(t, tx, tn, 38.0).iloc[0], expected)
