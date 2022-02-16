#!/bin/bash
# run with: sbatch <script name> <cell name>

# Write output as following (%j is JOB_ID)
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err
# Ask for one CPU, one GPU, enter the GPU queue, and limit run to 1 days
#SBATCH -p ss.q
#SBATCH --mem 10000
#SBATCH -c 1
#SBATCH -t 1-0
# check if script is started via SLURM or bash
# if with SLURM: there variable '$SLURM_JOB_ID' will exist

echo $#

if [[ $# -ne 5 ]] ; then
    echo "Wrong usage. not have enought parameters"
    exit 1
fi

cell_name=$1
file_type2read=$2
folder=$3
resize_diam=$4
shrinkage_factor=$5
shift $#

# `if [ -n $SLURM_JOB_ID ]` checks if $SLURM_JOB_ID is not an empty string
if [ -n $SLURM_JOB_ID ]; then
# check the original location through scontrol and $SLURM_JOB_ID
   SCRIPT_PATH=$(scontrol show job $SLURM_JOBID | awk -F= '/Command=/{print $2}' | cut -d" " -f1)
else
# otherwise: started with bash. Get the real location.
   SCRIPT_PATH=$(realpath $0)
fi
# get script's path to allow running from any folder without errors
path=$(dirname $SCRIPT_PATH)
# If necessary, activate anaconda installed on your user (Default: /ems/..../<lab>/<user>/anaconda3
# source anaconda3/bin/activate
conda init
conda activate project
# put your script here - example script is sitting with this bash script


#python3 $path/main_cell_data.py $cell_name $folder $data_dir $save_dir
echo python3 $path/analysis_fit_after_run.py $cell_name $file_type2read
python3 $path/analysis_fit_after_run.py $cell_name $file_type2read $resize_diam $shrinkage_factor $folder
#
#echo python3 $path/cell_properties.py $cell_name $file_type2read
#python3 $path/cell_properties.py $cell_name $file_type2read $folder $data_dir $save_dir
#
#python3 $path/find_synaptic_loc.py
#
#python3 $path/plot_neuron_3D.py
#
#echo python3 $path/Rin_Rm_plot.py $cell_name $file_type2read
#python3 $path/Rin_Rm_plot.py $cell_name $file_type2read $folder $data_dir $save_dir
#
#echo python3 $path/find_Rinput.py $cell_name
#python3 $path/find_Rinput.py $cell_name $folder $save_dir $save_dir
echo python3 $path/dendogram.py $cell_name $file_type2read
python3 $path/dendogram.py $cell_name $file_type2read $folder $data_dir $save_dir

echo python3 $path/attenuations.py $cell_name $file_type2read $passive_val
python3 $path/attenuations.py $cell_name $file_type2read $folder $data_dir $save_dir $passive_val


echo "execute_level1 is complite to run"

