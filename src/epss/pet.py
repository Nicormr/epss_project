"""Potential evapotranspiration with Hargreaves (sheet eqs. 1-2)."""
import numpy as np
import pandas as pd


def extraterrestrial_radiation(lat_deg, doy):
    """Extraterrestrial radiation Ra (MJ m-2 day-1), FAO-56 eq. 21 (sheet eq. 2).

    lat_deg: latitude (°, north positive); doy: day of the year J (1-366).
    """
    gsc = 0.0820                                   # MJ m-2 min-1
    phi = np.radians(lat_deg)
    j = np.asarray(doy, dtype=float)
    dr = 1 + 0.033 * np.cos(2 * np.pi * j / 365)
    delta = 0.409 * np.sin(2 * np.pi * j / 365 - 1.39)
    ws = np.arccos(np.clip(-np.tan(phi) * np.tan(delta), -1, 1))
    return 24 * 60 / np.pi * gsc * dr * (ws * np.sin(phi) * np.sin(delta)
                                         + np.cos(phi) * np.cos(delta) * np.sin(ws))


def hargreaves(tmean, tmax, tmin, ra):
    """Hargreaves PET (mm/day).

    tmean, tmax, tmin: °C; ra: extraterrestrial radiation as evaporation equivalent (mm/day).
    """
    # TODO: Hargreaves equation (sheet eq. 1) with Ra already in mm/day: PET = 0.0023 * Ra * (T +
    #       17.8) * sqrt(Tmax - Tmin).
    # In: tmean, tmax, tmin (°C), ra (mm/day): numbers, arrays or pd.Series
    # Out: PET (mm/day)
    return 0.0023 * ra * (tmean + 17.8) * np.sqrt(tmax - tmin)


def pet_monthly(tmean, tmax, tmin, lat_deg):
    """Monthly PET (mm/month) from monthly temperatures (°C, pd.Series at month start).

    Ra is taken on the 15th of each month and converted with 0.408 (MJ m-2 day-1 -> mm/day).
    """
    # TODO: Monthly PET: Ra on the 15th of each month (extraterrestrial_radiation x 0.408 -> mm/day),
    #       then hargreaves(), then x days in month.
    # In: tmean, tmax, tmin (pd.Series, °C, month-start index), lat_deg (°)
    # Out: pd.Series named 'pet' (mm/month), same index
    day15 = tmean.index + pd.Timedelta(days=14)                  # 15th of each month
    ra = extraterrestrial_radiation(lat_deg, day15.day_of_year) * 0.408   # MJ m-2 day-1 -> mm/day
    pet_day = hargreaves(tmean, tmax, tmin, ra)                  # mm/day
    return (pet_day * tmean.index.days_in_month).rename("pet")   # mm/month
