from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5 import QtGui, QtCore
import sys 
import os 
from resize import resize
from img_process import img_process
import subprocess
import open3d as o3d 

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "NDR-beta"
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 800  
        self.imageList = []
        self.oripath = os.getcwd().replace(os.sep,'/')
        self.visualSFMpath = self.oripath + '/VisualSFM_windows_cuda_64bit'
        self.meshServerPath = self.oripath + '/MeshLab'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #init buttons 
        button = QPushButton('Choose images to reconstruction', self)
        button.clicked.connect(self.get_images)
        button.move(0,50)
        button.setFixedSize(200,50)

        button1 = QPushButton('Quit Application',self)
        button1.clicked.connect(self.destroy)
        button1.move(0,100)
        button1.setFixedSize(200,50)
        
        
        #init background logo
        oImage = QImage("C:/Users/chin1/Desktop/ndrlogo.jpg")
        sImage = oImage.scaled(QSize(1200,800))
        palette = QPalette()
        palette.setBrush(QPalette.Window,QBrush(sImage))
        self.setPalette(palette)

      
    @pyqtSlot()
    def get_images(self):
        filterr = "JPG (*.jpeg);;PNG (*.png)"
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files")
        
        for files in names[0]:
            self.imageList.append(files)
        
        resize(self.imageList)
        resized_path = self.oripath + '/resized'
        img_process(resized_path)

        masked_path = self.oripath + '/masked'
        os.chdir(self.visualSFMpath)

        nvm_folder = "myresult.nvm"
        sfm_commands = ['VisualSFM','sfm+pmvs',masked_path,nvm_folder]
        subprocess.call(sfm_commands)

        os.chdir(self.meshServerPath)
        mesh_output = self.oripath + '/final_meshed.ply'

        mesh_commands = ['meshlabserver' , '-i', self.visualSFMpath + '/myresult.nvm.cmvs/00/models/option-0000.ply',
                     '-o', mesh_output , '-s' , self.oripath + '/ballpivoting.mlx']

        subprocess.call(mesh_commands)

        pcd = o3d.io.read_point_cloud(mesh_output)
        o3d.visualization.draw_geometries([pcd])

    @pyqtSlot()
    def destroy(self):
        sys.exit()

   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec_())
