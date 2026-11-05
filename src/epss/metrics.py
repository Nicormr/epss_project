"""Reliability (sheet eqs. 14-15) and design search for hmax."""
import numpy as np

from .reservoir import Reservoir


def reliability_time(sim):
    """Rt = irrigation months without deficit / irrigation months (demand > 0)."""
    # TODO: Time reliability (sheet eq. 14): share of irrigation months (demand = supply + deficit >
    #       0) without deficit.
    # In: sim (DataFrame from Reservoir.simulate)
    # Out: float in [0, 1]
    raise NotImplementedError('Time reliability (sheet eq. 14): share of irrigation months (demand = supply + deficit > 0) without deficit.')


def reliability_volume(sim):
    """Rv = total supply / total demand."""
    # TODO: Volumetric reliability (sheet eq. 15): total supply / total demand.
    # In: sim (DataFrame from Reservoir.simulate)
    # Out: float in [0, 1]
    raise NotImplementedError('Volumetric reliability (sheet eq. 15): total supply / total demand.')


def required_hmax(hv, inflow, evap_mm, demand, eflow, target, hmin=0.0, area=None, tol=0.01):
    """Smallest hmax (m) with Rt >= target, by bisection within the h-V range.

    Returns np.nan if even the top of the h-V curve does not reach the target.
    """
    # TODO: Smallest hmax with reliability_time >= target, by bisection between hmin and the top of
    #       the h-V curve; np.nan if the top is not enough.
    # In: hv (DataFrame h_m, v_hm3), series as in Reservoir.simulate, target (-), hmin (m), area (km²
    #      or None)
    # Out: hmax (m), float
    raise NotImplementedError('Smallest hmax with reliability_time >= target, by bisection between hmin and the top of the h-V curve; np.nan if the top is not enough.')
