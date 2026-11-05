"""Monthly Thornthwaite-Mather soil water balance (sheet eqs. 3-7)."""
import numpy as np
import pandas as pd


def thornthwaite_mather(p, pet, smax, s0=0.0):
    """Monthly soil water balance. All values in mm (per month).

    p, pet: pd.Series (same index); smax: soil water capacity; s0: initial soil water.
    Returns a DataFrame with columns p, pet, deficit (L), aet, soil (S at month end), runoff (H).
    P = H + AET + dS closes every month.
    """
    # TODO: Thornthwaite-Mather, sheet eqs. (4)-(7): loop over the months, keeping the deficit L and
    #       the soil water S (L0 = 0, S0 = s0).
    # In: p, pet (pd.Series, mm/month), smax (mm), s0 (mm)
    # Out: DataFrame on the same index with columns p, pet, deficit, aet, soil, runoff (mm)
    raise NotImplementedError('Thornthwaite-Mather, sheet eqs. (4)-(7): loop over the months, keeping the deficit L and the soil water S (L0 = 0, S0 = s0).')
