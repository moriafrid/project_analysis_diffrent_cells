from open_pickle import read_from_pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
from add_figure import add_figure

def linear(x, m,c):
    return m*x+c
from extra_function import create_folders_list
folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/'
for cell_name in ['2017_05_08_A_4-5','2017_05_08_A_5-4','2017_03_04_A_6-7']:
    plt.close()
    plt.figure()
    folder_data=folder_+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p'
    folder_save=folder_+cell_name+'/fit/tau_m'
    create_folders_list([folder_save])
    # save_folder='data/tau_m'
    # path='/ems/elsc-labs/segev-i/moria.fridman/project/data_analysis_git/data_analysis/data/short_pulse/mean_short_pulse_with_parameters.p'
    # try:os.mkdir(save_folder)
    # except FileExistsError:pass

    short_pulse_dict = read_from_pickle(folder_data)
    short_pulse=short_pulse_dict['mean']
    V = np.array(short_pulse[0])
    short_pulse[1]=short_pulse[1].rescale('ms')
    T = np.array(short_pulse[1])
    T = T-T[0]
    T=T
    ###%%%
    v_t = (V-V.min())[1500:3000]
    T = np.arange(0, len(v_t), 1) * 0.1
    log_v = np.log(v_t)
    plt.plot(T, log_v,label="log(long_pulse)",alpha=0.2,lw=3)
    points=[[295, 1300],[900, 1050],[800, 1000],[805, 1300],[600, 900],[350, 595]]
    colors=['black','purple','orange','yellow','green','red']
    for i,point in enumerate(points):
        popt, pcov = curve_fit(linear, T[point[0]:point[1]], log_v[point[0]:point[1]])
        plt.plot(T, linear(np.array(T), *popt), color=colors[i], lw=1, label='tau=' + str(-1.0 / round(popt[0], 3)) + ' 1/s',
                 alpha=0.5)
        plt.scatter(T[point], log_v[point], color=colors[i], s=80, alpha=0.1)
        print(1.0 / (abs(log_v[point[1]] - log_v[point[0]]) / abs(T[point[1]] - T[point[0]])))
    plt.legend()

    plt.savefig(folder_save+'/all_tau')
    plt.show()
    for i,point in enumerate(points):
        add_figure('find tau from '+str(point),'t[ms]','ln(short_pulse)')
        plt.plot(T, log_v, label="ln(short_pulse)", alpha=0.3, lw=3)
        popt, pcov = curve_fit(linear, T[point[0]:point[1]], log_v[point[0]:point[1]])
        plt.plot(T, linear(np.array(T), *popt), color=colors[i], lw=2, label='tau=' + str( round(-1.0/popt[0], 3)) + ' 1/s',)
        plt.scatter(T[point], log_v[point], color=colors[i], s=80, alpha=0.5)
        print(1.0 / (abs(log_v[point[1]] - log_v[point[0]]) / abs(T[point[1]] - T[point[0]])))
        plt.legend()
        plt.savefig(folder_save+'/tau='+str( -round(1.0/popt[0], 3))+'.png')
    #
    # points = [295, 1300]
    # popt, pcov = curve_fit(linear, T[points[0]:points[1]], log_v[points[0]:points[1]])
    # plt.plot(T, linear(np.array(T), *popt),color='black',lw=1,label='tau='+str(1.0/round(popt[0],3))+' 1/s',alpha=0.5)
    # plt.scatter(T[points], log_v[points], color='black', s=80,alpha=0.1)
    # print(1.0/(abs(log_v[points[1]]-log_v[points[0]])/ abs(T[points[1]]-T[points[0]])))
    #
    # points = [800, 1000]
    # popt, pcov = curve_fit(linear, T[points[0]:points[1]], log_v[points[0]:points[1]])
    # plt.plot(T, linear(np.array(T), *popt),color='orange',lw=1,label='tau='+str(1.0/round(popt[0],3))+' 1/s',alpha=0.5)
    # plt.scatter(T[points], log_v[points], color='orange', s=80,alpha=0.1)
    # print(1.0/(abs(log_v[points[1]]-log_v[points[0]])/ abs(T[points[1]]-T[points[0]])))
    #
    # points = [805, 1300]
    # popt, pcov = curve_fit(linear, T[points[0]:points[1]], log_v[points[0]:points[1]])
    # plt.plot(T, linear(np.array(T), *popt),color='yellow',lw=1,label='tau='+str(1.0/round(popt[0],3))+' 1/s',alpha=0.5)
    # plt.scatter(T[points], log_v[points], color='yellow', s=80,alpha=0.1)
    # print(1.0/(abs(log_v[points[1]]-log_v[points[0]])/ abs(T[points[1]]-T[points[0]])))
    #
    # points = [600, 900]
    # popt, pcov = curve_fit(linear, T[points[0]:points[1]], log_v[points[0]:points[1]])
    # plt.plot(T, linear(np.array(T), *popt),color='green',lw=1,label='tau='+str(1.0/round(popt[0],3))+' 1/s',alpha=0.5)
    # plt.scatter(T[points], log_v[points], color='green', s=80,alpha=0.1)
    # print(1.0/(abs(log_v[points[1]]-log_v[points[0]])/ abs(T[points[1]]-T[points[0]])))
    #
    # points = [350, 595]
    # popt, pcov = curve_fit(linear, T[points[0]:points[1]], log_v[points[0]:points[1]])
    # plt.plot(T, linear(np.array(T), *popt),color='red',lw=1,label='tau='+str(1.0/round(popt[0],3))+' 1/s',alpha=0.5)
    # plt.scatter(T[points], log_v[points], color='red', s=80,alpha=0.1)
    # print(1.0/(abs(log_v[points[1]]-log_v[points[0]])/ abs(T[points[1]]-T[points[0]])))

    ###%%%
