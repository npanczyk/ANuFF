import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import datetime as dt
import yaml


def failed_rod_plot(failed_rods):
    bin_size = 1000
    bins = np.arange(0, failed_rods['time'].max() + bin_size, bin_size)
    failed_rods['TimeBin'] = pd.cut(failed_rods['time'], bins=bins, labels=(bins[:-1] / bin_size).astype(int))
    binned_data = failed_rods.groupby('TimeBin')['fail'].sum()
    plt.figure(figsize=(10, 5))
    plt.bar(binned_data.index, binned_data.values, width=1, edgecolor='black')
    plt.xlabel('Time (1000s of seconds)')
    plt.ylabel('Number of Failures')
    plt.grid(True, axis='y')
    plt.savefig('figures/failed_rods.png')
    return 

def first_rod_temp(data, failed_rods):
    fig, ax = plt.subplots()
    cutoff = np.array(failed_rods['time'])[0]
    ax.plot(data['time'][:cutoff], data['base temperature'][:cutoff], label='Base Temperature for Rod 1')
    ax.plot(data['time'][:cutoff], data['middle temperature'][:cutoff], label='Middle Temperature for Rod 1')
    ax.plot(data['time'][:cutoff], data['top temperature'][:cutoff], linestyle=':', color = 'k', label='Top Temperature for Rod 1')
    ax.vlines(cutoff, 20, np.array(data['middle temperature'])[cutoff], color='red', label='Time of Failure')
    ax.set_xlabel('Time, t [s]')
    ax.set_ylabel('Temperature, T [$^{\\circ}C$]')
    ax.legend()
    plt.savefig(f'figures/temp_v_time_.png', dpi=300)
    return

def pressure_plot(data, failed_rods):
    cutoff = np.array(failed_rods['time'])[0]
    fig, ax = plt.subplots()
    ax.plot(data['time'][:cutoff], data['pressure'][:cutoff])
    print( np.array(data['time'])[:cutoff])
    ax.vlines(cutoff, 1.45e7, 1.65e7, color='red', label='Time of Failure')
    ax.set_xlabel('Time, t [s]')
    ax.set_ylim(1.45e7, 1.65e7)
    ax.set_ylabel('Pressure, P [Pa]')
    ax.legend()
    plt.savefig(f'figures/pressure_v_time.png', dpi=300)
    return 

def pH_plot(data, failed_rods):
    cutoff = np.array(failed_rods['time'])[0]
    fig, ax = plt.subplots()
    ax.plot(data['time'][:cutoff], data['pH'][:cutoff], color='orange')
    ax.vlines(cutoff, 6, 8, color='red', label='Time of Failure')
    ax.set_xlabel('Time, t [s]')
    ax.set_ylabel('pH')
    ax.legend()
    plt.savefig(f'figures/pH_v_time.png', dpi=300)
    return

def spatial_temp():
    fig, ax = plt.subplots()
    y_arr = np.arange(0, 3.8, 0.1)
    temp = lambda y, t: 20 + 100*np.sin(np.pi*y/3.8)/3.8 + ((176.6-20)/3600)*t
    ax.plot(temp(y_arr, 0), y_arr, label='Time: 0 Seconds')
    ax.plot(temp(y_arr, 3600*0.25), y_arr, label='Time: 15 Minutes')
    ax.plot(temp(y_arr, 3600*0.5), y_arr, label='Time: 30 Minutes')
    ax.plot(temp(y_arr, 3600*0.75), y_arr, label='Time: 45 Minutes')
    ax.plot(temp(y_arr, 3600*1), y_arr, label='Time: 1 Hour')
    #ax.plot(temp(y_arr, 3600*2), y_arr, label='Time: 2 Hours')
    ax.set_xlabel('Temperature, T [$^{\\circ}C$]')
    ax.set_ylabel('Vertical Position Along Rod, y [m]')
    ax.legend()
    plt.savefig(f'figures/spatial_temp.png', dpi=300)
    return 



if __name__=="__main__":
    # read input file stuff
    with open('input.yml', 'r') as f:
        doggo = yaml.full_load(f)
    data = pd.read_excel(doggo.get('data_file'))
    failed_rods = data.loc[data['fail'] == True]
    failed_rod_plot(failed_rods)
    first_rod_temp(data, failed_rods)
    pressure_plot(data, failed_rods)
    pH_plot(data, failed_rods)
    spatial_temp()

