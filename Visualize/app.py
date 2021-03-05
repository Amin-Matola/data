"""
The main Application Window for this app
"""
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from data import *
from os import path, getcwd

# Save this object for calling during execution
defaultApp = QApplication(sys.argv)

class App(QWidget):

	def __init__(self, image = ''):
		super(App, self).__init__()

		self._layout = QGridLayout()
		self.style 	 = self.loadStyles()
		self.aspie 	 = False
		self.setUp()
		
		self.setLayout(self._layout)
		
		self.setMinimumWidth(900)
		self.setMaximumWidth(1200)
		self.setMinimumHeight(700)
		self.setMaximumHeight(900)
		self.setWindowTitle( "Data Visualization Window" )
		self.setAutoFillBackground( True )
		self.setBackgroundRole( QPalette.Highlight )

		self.files 				= []
		self.fields 			= []
		self.pix 				= ""
		self.config 			= {}
		self.x 					= ""
		self.y 					= ""
		self.its 				= []

	def loadStyles(self):
		if self.curdir() != self.package():
			return eval(open(f"{self.package()}/style.txt").read())
		return eval(open("./style.txt").read())


	def setUp(self):

		self.f_o 	= QLabel("Select file to be used")
		self.f_o.setStyleSheet(self.style["label"])
		self.f_o.setMaximumHeight(50)
		self._label   				= QLabel("No file to be visualized")
		self._label.setScaledContents(True)
		self._label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.pie 					= QCheckBox("Plot as a pie chart")
		self.pie.setStyleSheet(self.style["checkbox"])
		self.pie.stateChanged.connect(lambda:self.stateData(self.pie))

		self.opener 				= QPushButton("Browse")
		self.opener.setStyleSheet(self.style["button"])
		self.opener.clicked.connect(self.file_dialog)

		self.combox 				= QComboBox()
		self.comboy 				= QComboBox()
		self.combox.addItem("None")
		self.comboy.addItem("None")


		self.combox.currentIndexChanged.connect(lambda x:self.changeX())
		self.comboy.currentIndexChanged.connect(lambda x:self.changeY())


		labelx						= QLabel("X - Labels")
		labelx.setStyleSheet(self.style["minor"])
		labelx.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		labely						= QLabel("Y - Values")
		labely.setStyleSheet(self.style["minor"])
		labely.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

		# Roll one
		self.push(self.f_o, 0, 0, 1, 4)
		self.push(self.opener, 0, 4, 1, 1)

		# Roll two
		self.push(self.pie, 1, 0, 1, 1)
		self.push(labelx, 1, 1, 1, 1)
		self.push(self.combox, 1, 2, 1, 1)
		self.push(labely, 1, 3, 1, 1)
		self.push(self.comboy, 1, 4, 1, 1)

		# Roll five
		self.push(self._label, 3, 0, 3, 5)

		#self.load_image()

	def load_image(self):
		self.pix = QPixmap("s.png")
		self._label.setPixmap(self.pix)

	def changeX(self):
		self.x 		= self.combox.currentText()
		self.draw()
		

	def changeY(self):
		self.y 		= self.comboy.currentText()
		self.draw()

	def push( self, widget, *position):
		self._layout.addWidget(widget, *position)

	def stateData(self, button):
		if button.isChecked() == True:
			self.aspie = True
		else:
			self.aspie = False

		self.config["pie"] = self.aspie
		self.draw()

	def draw(self):

		self.its 	= ["Lymphoedema", "Elastic", "Venous"]

		if not len(self.x) or not len(self.y):
			return
		master = Data (self.files, self.x, self.y,filt="Venous")
		master.setAxisLabels("", "%s per CCG"%self.y)
		master.plot(False, pie=self.aspie)
		self.load_image()
		#master.plot(True, pie=False)

	def file_dialog(self):
		f, _ 				= QFileDialog.getOpenFileName(self, "Load Image", "~/Desktop/", "Files (*.xlsx, *.xls)")
		d 					= ""
		
		if len(f) and not f in self.files:
			self.files.append(f)
			

		if len(self.files) <= 1:
			if len(self.files) == 1:
				self.f_o.setStyleSheet(self.style["label"]+"color:#4b4b6b;")
				self.fields    = pd.read_excel(self.files[0], index_col=0)
				for field in self.fields:
					self.combox.addItem(field)
					self.comboy.addItem(field)
			d = f.split("/")[-1]
		else:
			d = self.f_o.text() + ", %s"%f.split("/")[-1]
		self.f_o.setText(d)

		self.draw()

	def curdir(self):
		return path.basename(getcwd())

	def package(self):
			return path.basename(path.dirname(path.abspath(__file__)))

	def build(self):
		return defaultApp.exec_()

	def boot():
		app = App()
		app.show()
		sys.exit(defaultApp.exec_())

		
		




# Incase it is called on console
if len(sys.argv):
	if len(sys.argv) > 1 and sys.argv[1] == "-b":
		App.boot()
	else:
		if not sys.argv[0].__eq__("."):
			print("\n\tAdd -b to the end of the file call to start the app.")
