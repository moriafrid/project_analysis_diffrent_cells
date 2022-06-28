from open_pickle import read_from_pickle
from glob import glob
import pickle
new=[]
unmV=read_from_pickle(glob('cells_outputs_data_old_runs/2017_05_08_A_5-4/data/electrophysio_records/syn/mean_syn.p')[0])[1].units
uns=read_from_pickle(glob('cells_outputs_data_old_runs/2017_05_08_A_5-4/data/electrophysio_records/syn/mean_syn.p')[0])[0].units
path1=glob('cells_outputs_data_short/*/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')

####i need correct the mean_short_pulse_with_paramaters.p
path1=glob('cells_outputs_data_short/*/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')
path2=glob('cells_initial_information/*/mean_short_pulse_with_parameters.p')
path3=glob('cells_outputs_data_old_runs/*/data/electrophysio_records/short_pulse/short_pulse.p')
for path in path2:
    cell_name=path.split('/')[1]
    if cell_name!='2016_05_12_A':continue
    path3=glob('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/syn/clear_syn0.p')[0]
    time=read_from_pickle(path3)[1]
    data=read_from_pickle(path3)
    data1=[]
    data1.append(data[0]*unmV)
    data1.append(data[1])
    # data1={}
    # data1['mean']=[data['mean'][0][:len(time)]*unmV,time]
    # data1['E_pas']=data['E_pas']
    # data1['points2calsulate_E_pas']=data['points2calsulate_E_pas']
    # print(len(data1['mean'][0]),len(data1['mean'][1]))
    print(data1)
    with open('cells_initial_information/'+cell_name+'/clear_syn0.p', 'wb') as handle:
        pickle.dump(data1, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #
    # # print(path)
    # dicty=read_from_pickle(path)
    # # new_mean=dicty['mean'][0]+dicty['E_pas']
    # # new_dicty=dicty.copy()
    # # new_dicty['mean'][0]=new_mean
    # # print(new_dicty)
    # print(dicty['mean'][0])
    # with open(path[:path.find('_temp.p')]+".p", 'wb') as handle:
    #     pickle.dump(dicty, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #
    #
    # if 'mean' in path.split('/')[-1]:
    #     'cells_outputs_data_short/2017_02_20_B/data/electrophysio_records/short_pulse/mean0_short_pulse_with_parameters.p'
    #     new_dict={}
    #     # print(path[:path.find('mean')]+'mean0_short_pulse_with_parameters.p')
    #     temp_dict=read_from_pickle(glob(path[:path.find('mean')]+'mean0_short_pulse_with_parameters.p')[0])
    #     new_dict['mean']=new
    #     new_dict['E_pas']=temp_dict['E_pas']
    #     new_dict['points2calsulate_E_pas']=temp_dict['points2calsulate_E_pas']
    #     print(new_dict)
    #     print(path[:path.find('mean')]+'mean_short_pulse_with_parameters.p')
    #     with open(path[:path.find('mean')]+'mean_short_pulse_with_parameters.p', 'wb') as handle:
    #         pickle.dump(new_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
