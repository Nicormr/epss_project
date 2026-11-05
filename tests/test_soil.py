import numpy as np
import pandas as pd

from epss.soil import thornthwaite_mather


def series(values):
    return pd.Series(values, index=pd.date_range("2000-10-01", periods=len(values), freq="MS"), dtype=float)


def test_hand_checked_months():
    # Smax 100, S0 0: wet, wet (fills + surplus), dry, dry
    tm = thornthwaite_mather(series([120, 150, 20, 10]), series([40, 50, 70, 90]), smax=100)
    assert np.allclose(tm.soil.iloc[:2], [80, 100])
    assert np.allclose(tm.runoff.iloc[:2], [0, 80])
    s3 = 100 * np.exp(-50 / 100)                    # L = -50
    assert np.isclose(tm.soil.iloc[2], s3)
    assert np.isclose(tm.aet.iloc[2], 20 + 100 - s3)
    assert np.isclose(tm.deficit.iloc[3], -130)       # L accumulates


def test_balance_closes_every_month():
    rng = np.random.default_rng(1)
    p, pet = series(rng.gamma(1.0, 50, 120)), series(rng.uniform(10, 180, 120))
    tm = thornthwaite_mather(p, pet, smax=80)
    # TODO: Write the checks of this test. Balance every month: P = H + AET + dS (dS = S(t) - S(t-1),
    #       S0 = 0). Bounds: 0 <= S <= Smax, H >= 0, AET <= PET.
    # In: tm (DataFrame from thornthwaite_mather, Smax = 80 mm, S0 = 0)
    # Out: assert statements (np.allclose for float comparisons)
    raise NotImplementedError('Write the checks of this test. Balance every month: P = H + AET + dS (dS = S(t) - S(t-1), S0 = 0). Bounds: 0 <= S <= Smax, H >= 0, AET <= PET.')
