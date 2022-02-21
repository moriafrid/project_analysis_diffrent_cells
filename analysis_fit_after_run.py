import numpy as np
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
from add_figure import add_figure
import os
import pickle
from glob import glob
import sys
from extra_function import create_folders_list

spine_type="mouse_spine"
print(sys.argv,flush=True)
if len(sys.argv) != 6:
    cell_name= '2017_03_04_A_6-7'
    file_type='ASC'
    resize_diam_by=1.0
    shrinkage_factor=1.0
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
   cell_name = sys.argv[1]
   file_type=sys.argv[2] #hoc ar ASC
   resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
   shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
   folder_= sys.argv[5] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
   if not folder_.endswith("/"):
       folder_ += "/"
save_dir ="cells_outputs_data/"
initial_folder=folder_+save_dir+cell_name+'/fit_short_pulse_'+file_type+'/'
# initial_folder+=spine_type
initial_folder+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))

# location='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/2017_05_08_A_4-5/fit_short_pulse_ASC/dend*1.0&F_shrinkage=1.0/basic_fit'
# datas2=glob(location+'/*/final_result*.p')
def analysis_fit(location):
    save_folder=location+'/analysis'
    create_folders_list([save_folder])
    errors,RAs,RMs,CMs,names,diffrent_condition=[],[],[],[],[],[]
    for dirr in glob(location+'/*/*result*.p'):
        dict=read_from_pickle(dirr)
        errors.append(dict['error']['decay&max'])
        RAs.append(dict['RA'])
        RMs.append(dict['RM'])
        CMs.append(dict['CM'])
        text=dirr.split('/')[-2]
        names.append(text)
        diffrent_condition.append(float(text.split('=')[-1]))
    condition=text.split('=')[-2]
    minimums_arg = np.argsort(errors)
    dict_minimums={}
    add_figure('diffrent RA against error\n'+dirr.split('/')[-3],'RA','errors')
    plt.plot(RAs,errors,'.')
    for mini in minimums_arg[:10]:
        plt.plot(RAs[mini], errors[mini], '*',
                 label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(
                     round(RAs[mini], 2)) + ' CM=' + str(
                     round(CMs[mini], 2)) +' '+names[mini]+ ' error=' +  str(round(errors[mini], 3)) )
    plt.legend(loc='upper left')
    plt.savefig(save_folder+'/diffrent RA against error.png')

    add_figure('diffrent '+condition+' against CM\n'+dirr.split('/')[-1],condition,'CM')
    plt.plot(diffrent_condition,CMs,'.')
    plt.savefig(save_folder+'/diffrent '+condition+' against CM.png')
    add_figure('diffrent '+condition+' against RA after fit\n'+dirr.split('/')[-3],'RA0','RA')
    plt.plot(diffrent_condition,RAs,'.')
    plt.savefig(save_folder+'/diffrent '+condition+' against RA after fit.png')
    add_figure('diffrent '+condition+' against RM\n'+dirr.split('/')[-3],'RA0','RM')
    plt.plot(diffrent_condition,RMs,'.')
    plt.savefig(save_folder+'/diffrent '+condition+' against RM.png')
    pickle.dump(dict_minimums, open(save_folder + "/ "+condition+" _10_minimums.p", "wb"))

if __name__ == '__main__':
    analysis_fit(initial_folder+'/basic_fit')
    # analysis_fit(initial_folder+'/const_param')

    initial_locs=glob(initial_folder)
    for loc in initial_locs:
        data=glob(loc+'/const_param/RA/Ra_const_errors.p')[0]
        save_folder1=data[:data.rfind('/')]+'/analysis'
        try:os.mkdir(save_folder1)
        except FileExistsError:pass
        dict3=read_from_pickle(data)
        RA0=dict3['RA']
        RAs,RMs,CMs,errors=[],[],[],[]
        errors=dict3['error']['decay&max']
        error_all=dict3['error']
        RAs=[value['RA'] for value in dict3['params']]
        RMs=[value['RM'] for value in dict3['params']]
        CMs=[value['CM'] for value in dict3['params']]
        add_figure('RA const against errors\n'+loc.split('/')[-1],'RA const','error')
        plt.plot(RA0,errors)
        minimums_arg=np.argsort(errors)
        dict_minimums2={}
        for mini in minimums_arg[:10]:
            plt.plot(RA0[mini], errors[mini], '*',label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)))
            dict_minimums2['RA_const=' + str(RA0[mini])]={'params': {'RM': RMs[mini], 'RA': RAs[mini], 'CM': CMs[mini]},'error':{key2:error_all[key2][mini] for key2 in error_all.keys()} }
        pickle.dump(dict_minimums2, open(save_folder1 + "/RA_const_10_minimums.p", "wb"))
        plt.legend(loc='upper left')
        plt.savefig(save_folder1+'/RA const against errors')
        plt.savefig(save_folder1+'/RA const against errors.pdf')

        end_plot=60
        add_figure('RA const against errors\n'+loc.split('/')[-1],'RA const','error')
        plt.plot(RA0[:end_plot],errors[:end_plot])
        for mini in minimums_arg[:10]:
            plt.plot(RA0[mini], errors[mini], '*',label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)))
        plt.legend(loc='upper left')
        plt.savefig(save_folder1+'/RA const against errors until point '+str(end_plot))

        add_figure('RA const against RMs\n'+loc.split('/')[-1],'RA const','RM')
        plt.plot(RA0,RMs)
        plt.savefig(save_folder1+'/RA const against RM')
        add_figure('RA const against RA after fit\n'+loc.split('/')[-1],'RA const','RA')
        plt.plot(RA0,RAs)
        plt.savefig(save_folder1+'/RA const against RA after fit')
        add_figure('RA const against CM\n'+loc.split('/')[-1],'RA const','CM')
        plt.plot(RA0,CMs)
        plt.savefig(save_folder1+'/RA const against CMs')


        datas=glob(loc+'/different_initial_conditions/RA0*/RA0_fit_results.p')
        for data in datas:
            if '+' in data: datas.remove(data)
        print(loc)
        print('datas', datas)
        data1,data2=datas
        #####change the locations
        for data in [data1,data2]:
            save_folder=data[:data.rfind('/')]+'/analysis'
            try:os.mkdir(save_folder)
            except FileExistsError: pass

            dict=read_from_pickle(data)
            dict1=read_from_pickle(data1)
            dict2=read_from_pickle(data2)

            RA0=np.sort([float(key.split('=')[-1]) for key in dict.keys()])
            value=[dict[key] for key in dict.keys()]
            # errors=[value[i]['error']['decay&max'] for i in range(len(value))]
            # RAs=[value[i]['RA'] for i in range(len(value))]
            # RMs=[value[i]['RM'] for i in range(len(value))]
            # CMs=[value[i]['CM'] for i in range(len(value))]
            RAs,RMs,CMs,errors=[],[],[],[]
            for key in dict.keys():
                RAs.append(dict[key]['RA'])
                RMs.append(dict[key]['RM'])
                CMs.append(dict[key]['CM'])
                errors.append(dict[key]['error']['total_error'])
                # errors.append(dict[key]['error']['decay&max'])
            add_figure('diffrent RA0 against error\n'+loc.split('/')[-1],'RA0','errors')
            plt.plot(RA0,errors)
            minimums_arg = np.argsort(errors)
            dict_minimums={}
            for mini in minimums_arg[:10]:
                plt.plot(RA0[mini], errors[mini], '*',
                         label='RA0=' + str(RA0[mini]) + ' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(
                             round(RAs[mini], 2)) + ' CM=' + str(
                             round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)))
                del value[mini]['error']
                dict_minimums['RA0=' + str(RA0[mini])]=value[mini]
            plt.legend(loc='upper left')
            plt.savefig(save_folder+'/diffrent RA0 against error.png')

            add_figure('diffrent RA against error\n'+loc.split('/')[-1],'RA','errors')
            plt.plot(RAs,errors,'.')
            for mini in minimums_arg[:10]:
                plt.plot(RAs[mini], errors[mini], '*',
                         label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(
                             round(RAs[mini], 2)) + ' CM=' + str(
                             round(CMs[mini], 2)) +' RA0=' + str(RA0[mini])+ ' error=' +  str(round(errors[mini], 3)) )
            plt.legend(loc='upper left')
            plt.savefig(save_folder+'/diffrent RA against error.png')

            add_figure('diffrent RA0 against CM\n'+loc.split('/')[-1],'RA0','CM')
            plt.plot(RA0,CMs)
            plt.savefig(save_folder+'/diffrent RA0 against CM.png')
            add_figure('diffrent RA0 against RA after fit\n'+loc.split('/')[-1],'RA0','RA')
            plt.plot(RA0,RAs)
            plt.savefig(save_folder+'/diffrent RA0 against RA after fit.png')
            add_figure('diffrent RA0 against RM\n'+loc.split('/')[-1],'RA0','RM')
            plt.plot(RA0,RMs)
            plt.savefig(save_folder+'/diffrent RA0 against RM.png')
            pickle.dump(dict_minimums, open(save_folder + "/RA0_10_minimums.p", "wb"))
        if float(next(iter(dict1.keys())).split('=')[-1])<float(next(iter(dict2.keys())).split('=')[-1]):
            dict = dict1.copy()  # Copy the dict1 into the dict3 using copy() method
            for key, value in dict2.items():  # use for loop to iterate dict2 into the dict3 dictionary
                dict[key] = value
        else:
            dict = dict2.copy()  # Copy the dict1 into the dict3 using copy() method
            for key, value in dict1.items():  # use for loop to iterate dict2 into the dict3 dictionary
                dict[key] = value

        save_folder=loc+'/different_initial_conditions/'+data1.split('/')[-2]+'+'+data2.split('/')[-2]
        try:os.mkdir(save_folder)
        except FileExistsError: pass

        RA0=[float(key.split('=')[-1]) for key in dict.keys()]
        value=[dict[key] for key in dict.keys()]
        RAs,RMs,CMs,errors=[],[],[],[]
        for key in dict.keys():
            RAs.append(dict[key]['RA'])
            RMs.append(dict[key]['RM'])
            CMs.append(dict[key]['CM'])
            errors.append(dict[key]['error']['total_error'])
        add_figure('diffrent RA0 against error\n'+loc.split('/')[-1],'RA0','errors')
        plt.plot(RA0,errors)
        minimums_arg=np.argsort(errors)
        # mini = np.argmin(errors)
        dict_minimums={}
        # print(loc)
        for mini in minimums_arg[:10]:
            plt.plot(RA0[mini], errors[mini], '*',label='RA0=' + str(RA0[mini]) + ' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' + str(round(errors[mini], 3)))
            dict_minimums['RA0=' + str(RA0[mini])]=dict.get('RA0=' + str(RA0[mini]), dict.get('RA0=' + str(int(RA0[mini])), None))
            if dict_minimums['RA0=' + str(RA0[mini])] is None:
                raise TypeError("dict_minimums get None")
        pickle.dump(dict_minimums, open(save_folder + "/RA0_10_minimums.p", "wb"))
        plt.legend(loc='upper left')
        plt.savefig(save_folder+'/diffrent RA0 against error.png')

        add_figure('diffrent RA against error\n'+loc.split('/')[-1],'RA','errors')
        plt.plot(RAs,errors,'.')
        for mini in minimums_arg[:10]:
            plt.plot(RAs[mini], errors[mini], '*',label= 'RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' + str(round(errors[mini], 3)) )
        plt.legend(loc='upper left')
        plt.savefig(save_folder+'/diffrent RA against error.png')

        add_figure('diffrent RA0 against CM\n'+loc.split('/')[-1],'RA0','CM')
        plt.plot(RA0,CMs)
        plt.savefig(save_folder+'/diffrent RA0 against CM.png')
        add_figure('diffrent RA0 against ֵֻֻRA after fit\n'+loc.split('/')[-1],'RA0','RA')
        plt.plot(RA0,RAs)
        plt.savefig(save_folder+'/diffrent RA0 against RA after fit.png')
        add_figure('diffrent RA0 against RM\n'+loc.split('/')[-1],'RA0','RM')
        plt.plot(RA0,RMs)
        plt.savefig(save_folder+'/diffrent RA0 against RM.png')


