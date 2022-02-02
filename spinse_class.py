from math import pi,sqrt
from extra_function import mkcell
import numpy as np
from glob import glob


class SpinesParams:
    def __init__(self, cell_name, is_general_mouse_type=False,is_general_human_type=False,spine_num=1):
        self.cell_name=cell_name
        if is_general_mouse_type:
            #mouse https://link.springer.com/content/pdf/10.1023/A:1024134312173.pdf
            self.head_area=0.37
            self.R_head=sqrt(self.head_area/(4*pi))
            self.neck_length=0.73
            self.head_diam=2*self.R_head
            self.spine_neck_diam=0.25 #0.164/07=0.23
            self.spine_density=1.08
            self.V_head=4/3*pi*self.R_head**3
        elif is_general_mouse_type == "shaft_spine":
            self.neck_length=0.001
            self.head_diam=0.944
            self.R_head=self.head_diam/2
        elif is_general_human_type:
            self.neck_length=1.35
            self.head_diam=0.944
        elif cell_name is not None:
            if cell_name == "2017_05_08_A_4-5":
                self.V_spine=0.16884774101 #[µm^3]
                self.V_head=0.13906972096 #4/3*pi*self.R_head**3
                self.v_neck=0.02977802005
                self.neck_length = 0.782 #µm
                self.neck_diam = 0.164 #µm
                self.R_head = (self.V_spine/(4*pi/3))**(1/3) #0.32µm
                self.head_diam=2*self.R_head #µm 0.64
                self.PSD_area=0.14
            if cell_name == "2017_05_08_A_5-4":
                if spine_num==1:
                    self.V_spine=0.06818310193 #[µm^3]
                    self.V_head=0.03371715503 #[µm^3] #4/3*pi*self.R_head**3
                    self.v_neck=0.0344659469 #[µm^3]
                    self.neck_length = 1.266 #µm
                    self.neck_diam =0.125 #µm
                    self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                    self.head_diam=2*self.R_head #µm
                    self.PSD_area=0.066
                elif spine_num==2:
                    self.V_spine=0.02865474235 #[µm^3]
                    self.V_head=0.01125841287 #[µm^3] #4/3*pi*self.R_head**3
                    self.v_neck=0.01739632948 #[µm^3]
                    self.neck_length = 1.121 #µm
                    self.neck_diam =0.102 #µm
                    self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                    self.head_diam=2*self.R_head #µm
                    self.PSD_area=0.014
                else: raise "there is more than one syn"

            if cell_name == "2017_03_04_A_6-7":
                if spine_num==1:
                    self.V_spine=0.08501695029 #[µm^3]
                    self.V_head=0.0745871871 #[µm^3] #4/3*pi*self.R_head**3
                    self.v_neck=0.01042976319 #[µm^3]

                    self.neck_length = 0.763 #µm
                    self.neck_diam =0.134 #µm

                    self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                    self.head_diam=2*self.R_head #µm
                    self.PSD_area=0.114
                elif spine_num==2:
                    self.V_spine=0.0783942101 #[µm^3]
                    self.V_head=0.06459193692 #[µm^3] #4/3*pi*self.R_head**3
                    self.v_neck=0.01380227318 #[µm^3]

                    self.neck_length = 0.905 #µm
                    self.neck_diam =0.039 #µm

                    self.R_head = (self.V_spine/(4*pi/3))**(1/3) #µm
                    self.head_diam=2*self.R_head #µm
                    self.PSD_area=0.039
                else: raise "there is more than one syn"
    def calculate_F_factor(self,data_folder,spines_density=1.08):
        print(glob(data_folder+"/"+self.cell_name+'/*ASC'))
        cell=mkcell(glob(data_folder+"/"+self.cell_name+'/*ASC')[0])
        dend_len=np.sum([sec.L for sec in cell.dend])
        spine_in_Micron_density=spines_density#12/10 #[N_spine/micrometer] number of spines in micrometer on the dendrite
        # r_head=(self.V_head/(4*pi/3))**(1/3)
        head_area=4*pi*self.R_head**2
        neck_area=2*pi*(self.neck_diam/2)*self.neck_length
        spine_area=neck_area+head_area
        spines_area=spine_area*dend_len*spine_in_Micron_density
        dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
        F_factor=(spines_area+dends_area)/dends_area
        return F_factor




class SpineLocatin:
    def __init__(self, cell_name=None,spine_num=0):
        if cell_name!=None:
            if cell_name == "2017_05_08_A_4-5":
                self.dis_from_soma=83.8
                self.locatin_xyz=()
                self.PSD=0.14
            if cell_name == "2017_05_08_A_5-4":
                if spine_num==1:
                    self.dis_from_soma=77.5
                    self.locatin_xyz=()
                    self.PSD=0.066
                elif spine_num==2:
                    self.dis_from_soma=74.3
                    self.locatin_xyz=()
                    self.PSD=0.014
                else: raise "there is more than one syn"
            if cell_name == "2017_03_04_A_6-7":
                if spine_num==1:
                    self.dis_from_soma=32.6
                    self.locatin_xyz=()
                    self.PSD=0.144
                elif spine_num==2:
                    self.dis_from_soma=50.6
                    self.locatin_xyz=()
                    self.PSD=0.039
                else: raise "there is more than one syn"

if __name__ == '__main__':
    spine=SpinesParams("2017_05_08_A_4-5")
    spine.calculate_F_factor('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information')
    a=1
