# import sys
import pickle
from glob import glob
import numpy as np
from matplotlib import pyplot as plt, gridspec
import pickle5 as pickle
from open_pickle import read_from_pickle
import sys
#%% load simulation data
without_axons=True
data_dir = '/kaggle/input/fiter-and-fire-paper'
if len(sys.argv) != 2:
    cell_name="2017_05_08_A_4-5"
else:
    cell_name=sys.argv[1]

def get_morphology(morphology_filename="./morphology_dict.pickle", experiment_dict={'Params': {}},
                   experiment_table=None):
    morphology_dict = pickle.load(open(morphology_filename, "rb"), encoding='latin1')
    # allSectionsLength                  = morphology_dict['all_sections_length']
    # allSections_DistFromSoma           = morphology_dict['all_sections_distance_from_soma']
    # allSegmentsLength                  = morphology_dict['all_segments_length']
    allSegmentsType = morphology_dict['all_segments_type']
    # allSegments_DistFromSoma           = morphology_dict['all_segments_distance_from_soma']
    # allSegments_SectionDistFromSoma    = morphology_dict['all_segments_section_distance_from_soma']
    allSegments_SectionInd = morphology_dict['all_segments_section_index']
    allSegments_seg_ind_within_sec_ind = morphology_dict['all_segments_segment_index_within_section_index']

    all_basal_section_coords = morphology_dict['all_basal_section_coords']
    all_basal_segment_coords = morphology_dict['all_basal_segment_coords']
    all_apical_section_coords = morphology_dict['all_apical_section_coords']
    all_apical_segment_coords = morphology_dict['all_apical_segment_coords']

    if experiment_dict['Params'] == {} and experiment_table is not None:
        section_index = np.array(experiment_table.allSegments_SectionInd)
        distance_from_soma = np.array(experiment_table.allSegments_SecDistFromSoma)
        is_basal = np.array([x == 'basal' for x in experiment_table.allSegmentsType])
    elif experiment_dict['Params'] != {}:
        section_index = np.array(experiment_dict['Params']['allSegments_SectionInd'])
        distance_from_soma = np.array(experiment_dict['Params']['allSegments_SecDistFromSoma'])
        is_basal = np.array([x == 'basal' for x in experiment_dict['Params']['allSegmentsType']])
    # else:
    #     return

    seg_ind_to_xyz_coords_map = {}
    seg_ind_to_sec_ind_map = {}
    for k in range(len(allSegmentsType)):
        curr_segment_ind = allSegments_seg_ind_within_sec_ind[k]
        if allSegmentsType[k] == 'basal':
            curr_section_ind = allSegments_SectionInd[k]
            seg_ind_to_xyz_coords_map[k] = all_basal_segment_coords[(curr_section_ind, curr_segment_ind)]
            seg_ind_to_sec_ind_map[k] = ('basal', curr_section_ind)
        elif allSegmentsType[k] == 'apical':
            curr_section_ind = allSegments_SectionInd[k] - len(all_basal_section_coords)
            seg_ind_to_xyz_coords_map[k] = all_apical_segment_coords[(curr_section_ind, curr_segment_ind)]
            seg_ind_to_sec_ind_map[k] = ('apical', curr_section_ind)
        else:
            print('error!')

    return seg_ind_to_xyz_coords_map, seg_ind_to_sec_ind_map, section_index, distance_from_soma, is_basal

def plot_morphology(ax, segment_colors, names=[], width_mult_factors=None, seg_ind_to_xyz_coords_map={}):
    if width_mult_factors is None:
        width_mult_factor = 1.2
        width_mult_factors = width_mult_factor * np.ones((segment_colors.shape))

    if segment_colors.max()!=0:
        segment_colors = segment_colors / segment_colors.max()
    colors = plt.cm.jet(segment_colors)

    all_seg_inds = seg_ind_to_xyz_coords_map.keys()

    # assemble the colors for each dendritic segment
    colors_per_segment = {}
    widths_per_segment = {}
    for seg_ind in all_seg_inds:
        colors_per_segment[seg_ind] = colors[seg_ind]
        widths_per_segment[seg_ind] = width_mult_factors[seg_ind]

    # plot the cell morphology
    for key in all_seg_inds:
        if without_axons:
            if 'axon' in seg_ind_to_xyz_coords_map[key]['sec name']:
                print(seg_ind_to_xyz_coords_map[key]['sec name'])
                continue
        seg_color = colors_per_segment[key]
        # seg_line_width = width_mult_factor * np.array(seg_ind_to_xyz_coords_map[key]['d']).mean()
        seg_line_width = min(6, widths_per_segment[key] * np.array(seg_ind_to_xyz_coords_map[key]['d']).mean())
        # print(np.array(seg_ind_to_xyz_coords_map[key]['d']).mean())
        seg_x_coords = seg_ind_to_xyz_coords_map[key]['x']
        seg_y_coords = seg_ind_to_xyz_coords_map[key]['y']

        if np.isscalar(seg_ind_to_xyz_coords_map[key]['x']):
            ax.scatter(seg_x_coords, seg_y_coords,s=40, color=seg_color)
        else:
            ax.plot(seg_x_coords, seg_y_coords, lw=seg_line_width, color=seg_color)
    if names != []:
        for ind in all_seg_inds:
            ax.text(np.max(seg_ind_to_xyz_coords_map[key]['x']), np.max(seg_ind_to_xyz_coords_map[key]['y']),
                    names[ind])

    # add black soma
    # ax.scatter(x=45.5, y=19.8, s=120, c='k')
    # ax.set_xlim(-180, 235)
    # ax.set_ylim(-210, 1200);
    plt.show()

# morphology_filename=glob('cells_initial_information/2017_03_04_A_6-7/morphology_dict.pickle')
morphology_filename=glob('cells_initial_information/'+cell_name+'/dict_morphology.pickle')

seg_ind_to_xyz_coords_map=read_from_pickle(morphology_filename[0])
# sim_results=None
# seg_ind_to_xyz_coords_map, seg_ind_to_sec_ind_map, section_index, distance_from_soma, is_basal = \
#     get_morphology(morphology_filename=morphology_filename, experiment_dict={"Params": {}}, experiment_table=sim_results)

# data_dir='David_kaggel_data/'
# morphology_filename = os.path.join(data_dir, 'morphology_dict.pickle')
# seg_ind_to_xyz_coords_map, seg_ind_to_sec_ind_map, section_index, distance_from_soma, is_basal = get_morphology(morphology_filename=morphology_filename)

plt.close('all')
fig = plt.figure(figsize=(17,16))
gs_figure = gridspec.GridSpec(nrows=8,ncols=5)
gs_figure.update(left=0.04, right=0.95, bottom=0.05, top=0.95, wspace=0.5, hspace=0.9)
ax_morphology=fig.gca()

# plot the morphology with a few selected segments highlighted

##creat the basic color
num_segments=len(seg_ind_to_xyz_coords_map)
segment_colors_selected = np.zeros(num_segments)
segment_widths_selected = 1.2 * np.ones(segment_colors_selected.shape)

##highlith the selected part
chosen_PSP_segment_inds = []
# chosen_PSP_segment_inds = [1, 49, 132, 200, 344, 468, 530]
chosen_PSP_segment_colors = 0.5 + np.arange(len(chosen_PSP_segment_inds)) / len(chosen_PSP_segment_inds)
for curr_selected_segment_index, color in zip(chosen_PSP_segment_inds, chosen_PSP_segment_colors):
    segment_colors_selected[curr_selected_segment_index] = color
    segment_widths_selected[curr_selected_segment_index] = 30.0

plot_morphology(ax_morphology, segment_colors_selected, width_mult_factors=segment_widths_selected,
                seg_ind_to_xyz_coords_map=seg_ind_to_xyz_coords_map, names=[])
ax_morphology.set_axis_off()