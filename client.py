import requests 
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setGeometry(800, 200, 500, 200)
        self.setWindowTitle("클라이언트")
		
    def setupUI(self):
        self.layout = QVBoxLayout()
		
        radiogroupBox = QGroupBox("파일 형식", self)
        self.radiopdf = QRadioButton("PDF", self)
        self.radiopdf.setChecked(True)
        self.radiomp4 = QRadioButton("MP4", self)
        rediogroup = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
   
        self.path = "http://neobby.asuscomm.com:8080/facility/drawing/createDrawing"
        self.pathEdit = QLineEdit("http://neobby.asuscomm.com:8080/facility/drawing/createDrawing",self)
        self.pathEdit.setReadOnly(True)
        self.pathEdit.resize(200,3)
        
        rediogroup.addWidget(self.radiopdf)
        rediogroup.addWidget(self.radiomp4)
        rediogroup.addWidget(self.pathEdit)
        radiogroupBox.setLayout(rediogroup)
        
        inputgroupBox = QGroupBox("보내는 파일", self)
        self.input = ""
        self.contents_file = {}
        self.inputEdit = QLineEdit(self)
        self.inputEdit.setReadOnly(True)		
        self.openButton = QPushButton("Open")
        
        inputgroup = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        inputgroup.addWidget(self.inputEdit)
        inputgroup.addWidget(self.openButton)
        inputgroupBox.setLayout(inputgroup)
        
        foldergroupBox = QGroupBox("폴더명", self)
        self.folder_name = '상부구조'
        self.folder = QComboBox()
        self.folder.addItems(['상부구조','하부구조','교량,받침','강박스','보고서','영상'])
        self.folder.currentTextChanged.connect(self.foldernameSelect)
        foldergroup = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        foldergroup.addWidget(self.folder)
        foldergroupBox.setLayout(foldergroup)
		
        namegroupBox = QGroupBox("프로젝트명", self)
        self.name = QLineEdit(self)
        namegroup = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        namegroup.addWidget(self.name)
        namegroupBox.setLayout(namegroup)
        
        descgroupBox = QGroupBox("설명", self)
        self.desc = QTextEdit(self)
        descgroup = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        descgroup.addWidget(self.desc)
        descgroupBox.setLayout(descgroup)
		
        self.sendButton = QPushButton("Send")
		
        self.listview = QListView(self)
        
        self.radiopdf.clicked.connect(self.radioButtonClicked)
        self.radiomp4.clicked.connect(self.radioButtonClicked)
        self.openButton.clicked.connect(self.inputButtonClicked)
        self.sendButton.clicked.connect(self.sendButtonClicked)
        
        self.layout.addWidget(radiogroupBox)
        self.layout.addWidget(inputgroupBox)
        self.layout.addWidget(foldergroupBox)
        self.layout.addWidget(namegroupBox)
        self.layout.addWidget(descgroupBox)
        self.layout.addWidget(self.sendButton)
        self.layout.addWidget(self.listview)
        self.setLayout(self.layout)
        
        """
        self.layout.addWidget(groupBox, 0 ,0)
        #self.layout.addWidget(self.pathEdit, 0, 1)
        self.layout.addWidget(self.inputEdit, 1, 0)
        self.layout.addWidget(self.openButton, 1, 1)
        self.layout.addWidget(self.folder, 2, 0)
        self.layout.addWidget(self.name, 2, 1)
        self.layout.addWidget(self.desc, 3, 0)
        self.layout.addWidget(self.sendButton, 3, 1)
        self.setLayout(self.layout)
		"""
    def radioButtonClicked(self):
        if self.radiopdf.isChecked():
            self.path = "http://neobby.asuscomm.com:8080/facility/drawing/createDrawing"
            self.pathEdit.setText(self.path)
        else:
            self.path = "http://neobby.asuscomm.com:8080/facility/video/createVideo"	
            self.pathEdit.setText(self.path)
		
		
    def inputButtonClicked(self):
        filename = QFileDialog.getOpenFileName(self)
        self.inputEdit.setText(filename[0])
		
        self.input = filename[0]
        try:
            file = open(self.input,'rb')
            self.contents_file = {'contents_file':file}
        except FileNotFoundError:
            pass
        
	
    def foldernameSelect(self,text):
        self.folder_name = text
    
    def sendButtonClicked(self):
    
        model = QStandardItemModel()
        project_folder = 'IoT, XAI 기반 실시간 교량 점검'
		
        print(self.path)
        print(self.name.text())
        print(project_folder)
        print(self.input)
        print(self.folder_name)
        print(self.desc.toPlainText())
		
        model.appendRow(QStandardItem(self.path))
        self.listview.setModel(model)
        model.appendRow(QStandardItem(self.name.text()))
        self.listview.setModel(model)
        model.appendRow(QStandardItem(project_folder))
        self.listview.setModel(model)
        model.appendRow(QStandardItem(self.input))
        self.listview.setModel(model)
        model.appendRow(QStandardItem(self.folder_name))
        self.listview.setModel(model)
        model.appendRow(QStandardItem(self.desc.toPlainText()))
        self.listview.setModel(model)
        
        paramDict = {
			'name': self.name.text(),
			'project_folder':project_folder,
			'folder_name':self.folder_name,
			'desc': self.desc.toPlainText()
            }
            
        print(paramDict)
        #model.appendRow(QStandardItem(paramDict))
        #self.listview.setModel(model)
        
        response = requests.post(self.path,data=paramDict,files=self.contents_file) 
        response.status_code 
        text = response.text
        
        print(text)
        model.appendRow(QStandardItem(text))
        self.listview.setModel(model)
		
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()		