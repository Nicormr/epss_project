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
    L, S = 0.0, s0
    rows = []
    for P, E in zip(p.values, pet.values):
        S_prev = S
        if P >= E:                                   # wet month
            L = 0.0
            S = min(S_prev + P - E, smax)
            aet = E
        else:                                        # dry month
            L = L + (P - E)                          # accumulated deficit (negative)
            S = S_prev * np.exp(L / smax)
            aet = min(E, P + S_prev - S)
        H = max(P - E - (S - S_prev), 0.0)           # runoff
        rows.append((P, E, L, aet, S, H))
    return pd.DataFrame(rows, index=p.index,
                        columns=["p", "pet", "deficit", "aet", "soil", "runoff"])
