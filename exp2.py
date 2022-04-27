from open_MOO_after_fit import OPEN_RES
import numpy as np
# from neuron import h
import matplotlib.pyplot as plt
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese,get_parameter
import os
from glob import glob
from tqdm import tqdm
import pickle
import matplotlib
from open_pickle import read_from_pickle
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

folder_= ''
folder_data=folder_+'cells_outputs_data_short/*6-7/MOO_results*re*/*/F_shrinkage=*/const_param/'
save_name='/AMPA&NMDA'

for model_place in tqdm(glob(folder_data+'*')):
    # print(model_place)
    type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    if type!='test': continue
    loader=None
    try:loader = OPEN_RES(res_pos=model_place+'/')
    except:
       print(model_place + '/hall_of_fame.p is not exsist' )
       continue
    if 'relative' in model_place:
        psd_sizes=get_parameter(cell_name,'PSD')
        argmax=np.argmax(psd_sizes)
        reletive_strengths=psd_sizes/psd_sizes[argmax]
    else:
        reletive_strengths=np.ones(get_n_spinese(cell_name))
    model=None
    model=loader.get_model()

    h=loader.sim.neuron.h
    netstim = h.NetStim()  # the location of the NetStim does not matter
    netstim.number = 1
    netstim.start = 200
    netstim.noise = 0

    secs,segs=get_sec_and_seg(cell_name)
    num=0
    V_spine=[]
    spines=[]
    syn_objs=[]
    for sec,seg in zip(secs,segs):
        dict_spine_param=get_building_spine(cell_name,num)
        spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,reletive_strengths[num], number=num,netstim=netstim)
        spines.append(spine)
        syn_objs.append(syn_obj)
        # V_spine.append(h.Vector())
        # V_spine[num].record(spine[1](1)._ref_v)
        num+=1

    # spine, syn_obj = loader.create_synapse(model.dend[82], 0.165, netstim=netstim)
    h.tstop = 400
    time = h.Vector()
    time.record(h._ref_t)
    V_soma = h.Vector()
    V_soma.record(model.soma[0](0.5)._ref_v)
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt
    h.run()

    V_soma_All = np.array(V_soma)[1700:]
    time_all = np.array(time)[1700:]
    time_all-=time_all[0]
    # take syn_obj to be 0 to see the NMDA
    for j in range(num):
        syn_objs[j][1][1].weight[0]=0
    h.dt=0.1
    h.steps_per_ms = 1.0/h.dt
    h.run()
    V_soma_AMPA = np.array(V_soma)[1700:]
    time_AMPA = np.array(time)[1700:]
    V_NMDA = V_soma_All-V_soma_AMPA
    from add_figure import add_figure

    passive_propert_title='Rm='+str(round(1.0/model.soma[0].g_pas,2)) +' Ra='+str(round(model.soma[0].Ra,2))+' Cm='+str(round(model.soma[0].cm,2))
    fig=add_figure('AMPA and NMDA impact on voltage '+" ".join(model_place.split('/')[-1].split('_')[2:])+'\n'+passive_propert_title,'time[ms]','Voltage[mV]')
    plt.plot(time_all, V_soma_All, color='g', lw=5,label='all',alpha=0.4)
    plt.plot(time_all, V_soma_AMPA, color='b', lw=2,linestyle='--', label='AMPA',alpha=0.8)
    # plt.plot(time_all, V_NMDA,lw=2, color='r', linestyle='--', label='NMDA',alpha=0.8)
    plt.plot(time_all, V_NMDA+V_soma_All[0],lw=2, color='r', linestyle='--', label='NMDA',alpha=0.8)
    RDSM_objective_file = folder_+'cells_initial_information/'+cell_name+"/mean_syn.p"
    T_data,V_data=read_from_pickle(RDSM_objective_file)
    T_data=np.array(T_data.rescale('ms'))[700:]
    T_data=T_data-T_data[0]
    plt.plot(np.array(T_data), np.array(V_data)[700:]+loader.get_param('e_pas'), color='black',label='EP record',alpha=0.2,lw=5)

    plt.legend()
    plt.savefig(model_place+save_name+'.png')
    plt.savefig(model_place+save_name+'.pdf')
    pickle.dump(fig, open(model_place+save_name+'.p', 'wb'))

    # plt.show()
