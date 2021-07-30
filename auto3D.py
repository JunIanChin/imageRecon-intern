import os
from resize import resize
from masking import masking
import time
import subprocess
from vtkplotter import show


def auto():
    """
    This function automates the process from resizing images to 600x400 pixel for each image,
    then it mask the object from original image to filter noise, then uses VisualSFM(an open source software)
    for 2d-> 3d. Meshlab ballpivoting reconstruction is used to mesh , vtkplotter is used as a default 
    way to show the meshed 3d object. 
    """

    # get cwd of where the script is located 
    # assuming its in the main folder w/o locating in another specific folder
    # eg: pythonscripts folder 

    ori_path = os.getcwd().replace(os.sep , '/')
    img_path = ori_path + '/img'
    vsfm_path = ori_path + '/VisualSFM_windows_cuda_64bit'
    masked_path = img_path + '/masked'
    meshlabserver_path = ori_path + '/MeshLab'
    
    resize(img_path)
    masking(img_path)
    
    # need to run the .exe 
    os.chdir(vsfm_path)

    nvm_folder = "myresult.nvm"
    sfm_commands = ['VisualSFM','sfm+pmvs',masked_path,nvm_folder]
    subprocess.call(sfm_commands)

    mesh_commands = ['meshlabserver' , '-i', vsfm_path + '/myresult.nvm.cmvs/00/models/option-0000.ply',
                     '-o', ori_path + '/final_meshed.ply' , '-s' , ori_path + '/ballpivoting.mlx']

    #need to run the .exe 
    os.chdir(meshlabserver_path)
    subprocess.call(mesh_commands)
    
    #vtkplotter show
    show(ori_path+'/final_meshed.ply')

