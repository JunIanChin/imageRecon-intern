import tkinter as tk 
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import os 
from resize import resize
from img_process import img_process
import subprocess 
from vtkplotter import show
from auto3D import auto

class Application(tk.Frame):
    """
    A class that handles everything for the gui 

    """
    def __init__(self,master= None):
        super().__init__(master)
        self.master = master      
       # self.testgrid = Frame(self.master)
        #self.master.resizable(0,0)
        self.create_widgets()
        self.masked_dir = ""
        self.ori_path = os.getcwd().replace(os.sep, '/')

    def create_widgets(self):
        """
        Creating buttons 
        """
        
        gridFrame = Frame(self.master)
        self.hi_there = tk.Button(gridFrame,text = "Automate process\n (Use all images)", command = self.auto3D)
        self.hi_there.grid(row = 0, column = 0, pady = 10, padx = 25, sticky = W )

        self.resize =  tk.Button(gridFrame, text= "Resize image to 600x400", command = self.resize_img)
        self.resize.grid(row =1, column = 0, pady = 10, padx = 25, sticky = W)

        self.imgprocess = tk.Button(gridFrame, text= "Image processing", command = self.img_process)
        self.imgprocess.grid(row= 2 ,column = 0, pady = 10, padx = 25, sticky = W)

        self.visualSFM = tk.Button(gridFrame, text="VisualSFM", command = self.openvSFM)
        self.visualSFM.grid(row = 3, column = 0, pady = 10, padx = 25, sticky = W)

        self.meshing = tk.Button(gridFrame, text = "Mesh", command = self.mesh)
        self.meshing.grid(row = 4, column = 0, pady = 10, padx = 25, sticky = W )

        self.vtkplot = tk.Button(gridFrame, text = "Show Mesh" , command = self.showmesh)
        self.vtkplot.grid(row = 5, column = 0 , pady = 10, padx= 25, sticky = W )

        self.quit = tk.Button(gridFrame, text= "Quit", fg="red",command = self.master.destroy)
        self.quit.grid(row = 6, column = 0, pady = 10, padx = 25, sticky = W)

        gridFrame.pack(anchor = NW)

    def auto3D(self):
        auto()

    # supportive function 
    def ask_imgdir(self):
        get_dir = filedialog.askdirectory(title = "Select image folder directory ")
        return get_dir 

    def resize_img(self):
        img_dir = self.ask_imgdir()
        resize(img_dir)
    
    def img_process(self):
        tosave_dir = self.ask_imgdir()
        img_process(tosave_dir)
        self.masked_dir = tosave_dir + '/masked'

    def openvSFM(self):
        sfm_dir = filedialog.askdirectory(title = "Select visualSFM.exe directory ")
        os.chdir(sfm_dir)
        subprocess.call('VisualSFM.exe')

    def mesh(self):
        mesh_commands = ['meshlabserver' , '-i', self.masked_dir + '/temp.nvm.cmvs/00/models/option-0000.ply',
                     '-o', self.ori_path + '/final_meshed.ply' , '-s' , self.ori_path + '/ballpivoting.mlx']
        meshserver_dir = filedialog.askdirectory(title = "Select meshlab server directory")
        os.chdir(meshserver_dir)
        subprocess.call(mesh_commands)
    
    def showmesh(self):
        meshfile = filedialog.askopenfilename(title= "Select mesh file to show")
        show(meshfile)

 
def main():
    root = Tk()
    root.geometry ("800x480")
    app = Application(root)
    app.mainloop()

if __name__ == "__main__":
    main()
