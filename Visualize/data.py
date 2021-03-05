""" 
Data File, this is the main data manipulator/processor for the app
All Data Passed from the UI are sent to this file for further processing
"""
import matplotlib.pyplot as plt
from matplotlib import rcParams as rp
import numpy as np, pandas as pd, os, sys


class Data :
  
  """ This is main Data Class, handling the data passed to the app"""
  
	data_store = []
  
	def __init__(self, source, field1, field2, filt="Lymphoedema"):
		self.files 			= source
		if not type(source) == list:
			self.files   	= [source]
		self.x 				= field1
		self.y 				= field2
		self.xaxis 			= ""
		self.yaxis 			= []
		self.xlabel			= ""
		self.ylabel 		= ""
		self.rawData 		= ""
		self.title 			= "Compression Hosiery within CCG %s (£’s)"%self.y
		self.data_store 	= []
		self.xt 			= []
		self.pie_sum 		= []
		self.filt 			= filt
		self.big_o			= []


		self.config()
		if type(source) == list:
			for f in source[::-1]:
				self.readExcel(f)
		else:
			self.readExcel(source)

	def config(self):
		plt.clf()
		plt.style.use("seaborn-dark")
		plt.tight_layout()
		#.text(wrap=True)
		#plt.xticks([], rotation=90)
		plt.rc('xtick', labelsize=8)
		plt.grid(axis="y")

	def readExcel(self, source = ""):
		if len(source):
			self.file 	= source

		self.rawData 	= pd.read_excel(source)
		self.boot()

	def setAxisLabels(self, x = "", y = "", color="#0f39af"):
		if len(x):
			plt.xlabel(x, color = color);
		if len(y):
			plt.ylabel(y, color = color)


	def boot(self):
		temp 			= [a for a,b in self.rawData[self.rawData.Category.str.startswith(self.filt, na=False)].groupby(
			by=["CCG Name"]
			)[self.x]]

		
		if len(temp) > 0 and len(temp) > len(self.big_o):
			self.big_o 	= temp.copy()

		self.xaxis 		= temp.copy()

		#self.xaxis 		= self.rawData[self.rawData.Category.str.startswith("Lymphoedema", na=False)][self.x]
		self.yaxis 		= [b for b in self.rawData[self.rawData.Category.str.startswith(self.filt, na=False)].groupby(
			by=["CCG Name"])[self.y].sum()]

		f 				= self.file.split("/")[-1].split("_")
		self.data_store.append((np.arange(len(self.xaxis.copy())), self.yaxis.copy(), f[0], " January ", f[1][3:] ))
		


	def plot(self, aspng = False, pie = False):
		width 		= 0.8/len(self.files)
		plt.title(self.title)
		plt.xticks(np.arange(len(self.big_o)), labels = self.big_o, rotation=75)

		explode 	= []

		if type(self.files) == list:
			for i in range(len(self.files)):
				if i == 1 and len(self.files) > 2:
					explode.append(0.1)
				else:
					explode.append(0.0)


		if pie:
			self.setAxisLabels(" "," ")
			plt.axis('equal')
			plt.pie([sum(a[1]) for a in self.data_store],
				wedgeprops={"edgecolor":"orange"}, 
				labels=["%s %s %s"%(a[2], a[3], a[4]) for a in self.data_store],
				autopct="%1.2f%%",
				#shadow=True,
				explode=explode,
				startangle=90)
		else:
			for a in self.data_store:
				if a.__eq__(self.data_store[0]):
					plt.bar(a[0] - width, a[1], width = width, label = "%s %s %s" % (a[2], a[3], a[4]), color="#9f0000")
				elif a.__eq__(self.data_store[-1]):
					plt.bar(a[0], a[1], label = "%s %s %s" % (a[2], a[3], a[4]), width = width, color="orange")
				else:
					plt.bar(a[0] + width, a[1], label = "%s %s %s" % (a[2], a[3], a[4]), width = width, color="#00009f")

		plt.legend()
		
		if "s.png" in os.listdir():
			os.remove("s.png")

		if aspng == 0:
				plt.savefig("s.png", dpi=100)
				
		else:
				plt.show()
