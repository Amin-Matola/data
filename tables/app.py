from PySide2.QtWidgets import (
	QWidget, QVBoxLayout, QApplication, 
	QTableWidget, QTableWidgetItem, QHeaderView,
	QFileDialog, QPushButton
	)

from numpy import genfromtxt

app = QApplication([])

class Table(QWidget):

	def __init__(self, data = []):
		super(Table, self).__init__()

		self.data_  = data
		self.btn 	= QPushButton("Open")
		self.table 	= False

		self.btn.clicked.connect(self.open)

		self.setTable()
		self.ly 	= QVBoxLayout()

		self.ly.addWidget(self.btn)
		self.ly.addWidget(self.table)
		self.setLayout(self.ly)

	def open(self):
		name 	= QFileDialog.getOpenFileName(self, "", "")
		try:
			self.data_ 	= genfromtxt(name[0], 
				dtype=str, 
				invalid_raise=False,
				missing_values='',
				loose = True,
				usemask = False,
				filling_values="N/a",
				delimiter=",")
		except:
			pass

		self.setTable()
		

	def setTable(self):
		if not self.table:
			self.table 	= QTableWidget()

		if not len(self.data_):
			return
		self.hders 	= self.data_[0]
		
		self.table.setRowCount(len(self.data_))
		self.table.setColumnCount(len(self.hders))
		#Table will fit the screen horizontally 
		self.table.horizontalHeader().setStretchLastSection(True) 
		self.table.horizontalHeader().setSectionResizeMode( 
            QHeaderView.Stretch) 

		self.addCustomData()

	def addCustomData(self):
		for row in range(len(self.data_)):
			for column in range(len(self.hders)):
				self.table.setItem(
					row, 
					column, 
					QTableWidgetItem(str(self.data_[row][column]))
					)


 
w = Table()
w.show()

app.exec_()