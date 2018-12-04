#|---------------------------This module deals with excel data specifically--------------------------|

#|___________________________ Last Modified By Amin Matola __________________________________________|

from xlrd import open_workbook as owork
from urllib import request
import json


opener   = urllib.build_opener()

class Json_convertor:
  
  global opener
  
  def __init__(self,source_workbook,sheet_name,dest):
    self.source = source_workbook
    self.sheet  = sheet_name
    self.destination  = dest
    
    self.process_workbook()
    
  def process_workbook(self):  
    self.book = owork(self.source)
    self.sheet = self.book.sheet_by_name(self.sheet)
    
    self.process_sheet_data()
    
  def process_sheet_data(self):
    self.excel_data = []
    self.data_headers = []
    for cell in sheet.row(0):
      self.data_headers.append(cell.value)
    for row_number in range(sheet.nrows):
      if row_number == 0:
        continue
      self.row_data = {}
      for column, cell in enumerate(worksheet.row(row_number)):
        self.row_data[self.data_headers[column]] = cell.value
      self.excel_data.append(row_data)
      
      self.convert_to_json(self):
    
    def convert_to_json(self):
      self.json_data  = json.dumps({'results': self.excel_data})
      
      self.write_to_json_file(self):
        self.json_file  = open(self.destination, 'w+')
        self.json_file.write(self.json_data)
        self.json_file.close()
