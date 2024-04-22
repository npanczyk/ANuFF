import numpy as np
import pandas as pd
import random
import datetime as dt


def make_temp(y, t, h=3.8, reactor="PWR", n_pins=289):
    """
    Parameters:
        y (float): vertical position from the bottom of the test fuel rod
        time (float): the time value, in seconds, since beginning of the experiment
        power (float): operational power level of the reactor,
        r (float): radius of a fuel pin,
        h (float): height of a fuel pin, in meters,
        n_pins (float): number of pins
    Returns:
        temp (float): the temperature of the cladding, in degrees Celsius
    """
    if t == 0:
        return 20 # at first time step, assume the whole rod is at room temp
    elif t > 0 and t <= 3600: # first hour of warm up
        m = (176.6-20)/3600
        return 20 + 100*np.sin(np.pi*y/h)/h + m*t
    elif t > 3600 and t <= 3600*2: # second hour of warm up
        m = (292-176.6)/3600
        return 20 + 100*np.sin(np.pi*y/h)/h + m*t
    else:
        return 292 + 100*np.sin(np.pi*y/h)/h

def make_pressure(time):
    """
    Parameters:
        time (numpy array): time array, in seconds, since beginning of the experiment
    Returns:
        pressure (float): the average system pressure in Pa
        Should be around 1.55e7 Pa
        https://direns.mines-paristech.fr/Sites/Thopt/en/co/centrales-nucleaires-eau.html
    """
    pressure = random.uniform(1.5e7,1.6e7)
    change = random.uniform(-1000,1000)
    pressure = pressure + change
    if (pressure > 1.6e7):
        pressure = 1.6e7
    elif (pressure < 1.5e7):
        pressure = 1.5e7
    return pressure

def make_pH(time):
    """
    Parameters:
        time (numpy array): time array, in seconds, since beginning of the experiment
    Returns:
        pH (float): the coolant pH
        Should be between 6.9 and 7.4
        https://inis.iaea.org/collection/NCLCollectionStore/_Public/28/075/28075997.pdf
    """
    pH = random.uniform(6.9,7.4)
    change = random.uniform(-0.025,0.025)
    pH = pH + change
    if (pH > 7.4):
        pH = 7.4
    elif (pH < 6.9):
        pH = 6.9
    return pH

def get_failure(t, time, seed=None):
    """
    Parameters:
        t (int): current time index in the experiment
        time (numpy array): time array, in seconds, since the beginning of the experiment
    Returns:
        fail (bool): If the fuel rod has failed, returns True
    """
    if seed is not None:
        np.random.seed(seed)

    pr = 0.00001

    if t > len(time) // 4:
        pr = 0.0001
    if t > len(time) // 2:
        pr = 0.0002
    if t > 3 * len(time) // 4:
        pr = 0.0005
    if make_pressure(time) > 1.55e7:
        pr *= 1.3
    if make_pH(time) > 7.15:
        pr *= 1.5
    if make_temp(1.9, t) > 130:
        pr *= 1.1


    return np.random.choice([True, False], size=1, replace=True, p=[pr, 1-pr])[0]


def make_data(time, h, seed=None):
    """
    Parameters:
        time (numpy array): time array, in seconds, since beginning of the experiment
        h (float): height of the fuel rod, in meters
        seed (int): value to set the seed for repeatability, defaults to None
        burnup (float): burnup of the rod when it was removed from the reactor, in GWd
    Returns:
        df (pandas dataframe): dataframe containing system parametric info and failure status for each timestep in test period
    """
    temp_base = []
    temp_middle = []
    temp_top = []
    pressure = []
    pH = []
    fail = []
    tval = []

    for i, t in enumerate(time):
        if i == 0:
            temp_base.append(make_temp(y=0,t=t))
            temp_middle.append(make_temp(y=h/2, t=t))
            temp_top.append(make_temp(y=h, t=t))
            pressure.append(make_pressure(t))
            pH.append(make_pH(t))
            fail.append(False)
            tval.append(t)
        elif i != 0 and fail[i-1] == False:
            temp_base.append(make_temp(y=0,t=t))
            temp_middle.append(make_temp(y=h/2, t=t))
            temp_top.append(make_temp(y=h, t=t))
            pressure.append(make_pressure(t))
            pH.append(make_pH(t))
            fail.append(get_failure(t, time))
            tval.append(t)
        else:
            break
    data = {
        'time':tval,
        'base temperature':temp_base,
        'middle temperature':temp_middle,
        'top temperature':temp_top,
        'pressure':pressure,
        'pH':pH,
        'fail':fail
    }
    df = pd.DataFrame(data)
    return df

def get_data(runtime=6*3600, timestep=1):
    time = np.arange(0, runtime, timestep) # time array in seconds (6 hours total)
    dfs = []
    for i in range(10):
        dfs.append(make_data(time=time, h=3.8, seed=1))
    return pd.concat(dfs)

if __name__=="__main__":
    data = get_data()  
    data.to_excel(f'fab_data.xlsx')