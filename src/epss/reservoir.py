"""Monthly reservoir mass balance (sheet eqs. 10-13).

Units: volumes hm³, levels m, areas km², evaporation mm/month.
1 hm³/m = 1 km², so dV/dh from the h-V table is directly an area in km².
"""
import numpy as np
import pandas as pd


class Reservoir:
    def __init__(self, hv, hmax, hmin=0.0, area=None):
        """hv: DataFrame with columns h_m, v_hm3 (increasing).
        area: fixed surface area A0 (km²), or None to use A(h) = dV/dh.
        """
        self.hv = hv.sort_values("h_m").reset_index(drop=True)
        self.area0 = area
        self.hmax, self.hmin = hmax, hmin
        self.vmax = float(self.volume(hmax))
        self.vmin = float(self.volume(hmin))

    def volume(self, h):
        """Volume (hm³) at level h (m)."""
        return np.interp(h, self.hv.h_m, self.hv.v_hm3)

    def level(self, v):
        """Level (m) at volume v (hm³), inverse interpolation of the h-V curve."""
        # TODO: Level from volume: inverse interpolation of the h-V curve (np.interp with volumes as x).
        # In: v (hm³)
        # Out: h (m)
        raise NotImplementedError('Level from volume: inverse interpolation of the h-V curve (np.interp with volumes as x).')

    def area(self, v):
        """Surface area (km²) at volume v: fixed A0, or dV/dh at level(v)."""
        # TODO: Surface area: the fixed A0 if it was given; otherwise A = dV/dh from the h-V table
        #       (np.gradient), interpolated at level(v).
        # In: v (hm³)
        # Out: A (km²); note that 1 hm³/m = 1 km²
        raise NotImplementedError('Surface area: the fixed A0 if it was given; otherwise A = dV/dh from the h-V table (np.gradient), interpolated at level(v).')

    def simulate(self, inflow, evap_mm, demand, eflow, v0=None):
        """Month-by-month simulation. All inputs are pd.Series on the same monthly index.

        inflow, demand, eflow (target): hm³/month; evap_mm: mm/month.
        Order per month: inflow -> e-flow -> evaporation -> supply -> spill.
        Returns a DataFrame with inflow, eflow, evaporation, supply, deficit, spill,
        volume and level (end of month).
        """
        # TODO: Monthly mass balance (sheet 3.5). Each month: 1) V* = V + Qin; 2) e-flow = min(target,
        #       Qin); 3) evaporation = evap_mm * area(V) / 1000, never below Vmin; 4) supply = min(D,
        #       water above Vmin), deficit = D - supply; 5) spill above Vmax. Start at v0 (default Vmax).
        # In: inflow, demand, eflow targets (hm³/month), evap_mm (mm/month), pd.Series on the same index
        # Out: DataFrame with columns inflow, eflow, evaporation, supply, deficit, spill, volume, level
        #      (end of month)
        raise NotImplementedError('Monthly mass balance (sheet 3.5). Each month: 1) V* = V + Qin; 2) e-flow = min(target, Qin); 3) evaporation = evap_mm * area(V) / 1000, never below Vmin; 4) supply = min(D, water above Vmin), deficit = D - supply; 5) spill above Vmax. Start at v0 (default Vmax).')
