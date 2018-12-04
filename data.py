#|-------------------A module for data digging----------------------|
#|-----------------Last touched by Amin Matola----------------------|

#|-------------------Import required modules------------------------|
from urllib import request
import csv
import json
import datetime
import os


opener  = request.build_opener()


class Data:
  """This is class for data manipulations,
  it conforms to seperation of concerns as much as possible.
  by setting the file url, destination file, and additional fieldnames of the file,
  you are good to go."""

  global opener


  def __init__(self,file_location,destination,iterable_fieldnames=[]):
    self.file = file_location
    self.dest = destination
    self.data_fields = iterable_fieldnames
    self.check_inputs()

  def check_inputs(self):
    print('Checking inputs...')
    #-----------The file location must start with 'http(s)' for urllib to open it successfully,otherwise it is on local disk-------|
    if self.file.lower().startswith('http'):
        self.file=self.file_location
        self.file_loc = 'internet'

    elif self.file[:3].lower() == 'www':
      self.file = 'http://%s'%self.file
      self.file_loc = 'internet'

    else:
        self.file_loc = 'local'

    self.process_request()

  def process_request(self):
    print('processing request...')
    if self.file_loc == 'internet': #------Then process url--------#
      try:
        self.remote_file = opener.open(self.file)
        self.remote_file_bytes = self.remote_file.read()
        self.remote_file_string= self.remote_file.decode()
      except Exception as e:
        return "Error openning file at %s.\n %s"%(self.file,e)
    else: #--------Then it is a file in a local disk----------------|
        self.remote_file_string = open(self.file,'r+')


    self.process_data()

  def process_data(self):
    print('processing response data...')
    if self.file_loc=='internet':
        self.file_lines = self.remote_file_string.split('\n')
        self.comma_list = [a.split(',') for a in self.file_lines]
        self.data_list  = []
        for b in self.comma_list:
            self.data_list += b
        self.file_lines = self.data_list




    if len(self.data_fields)>0:
        if self.file_loc.lower().startswith('internet'):
            print('reading internet data list from %s...'%self.file)
            self.file_dict  = csv.DictReader(self.remote_file_string,fieldnames=self.data_fields)
        else:
            print('reading the local opening of %s...'%self.file)
            self.file_dict  = csv.DictReader(self.remote_file_string,fieldnames=self.data_fields)

    else:
      print("-"*40,"\nOops! Oops! The syntax for calling this class is data=Data(file_location,destination_file,iterable_column_names).\nPlease try again")
      return
    self.convert_to_json()

  def convert_to_json(self):
     print('converting %s contents to json...'%str(self.file))
     self.json_data  = []
     for k in [line for line in self.file_dict]:
         self.json_data.append(json.dumps(k))
     self.write_to_json_file()

  def write_to_json_file(self):
     print('writing json data to %s...'%self.dest)
    #------- Now store json results, the 'with' will automatically close the file once done.------|
     self.local_file = open(self.dest,'w+')
     for a in self.json_data:
          self.local_file.write(a)
          self.local_file.write('\n')
     self.local_file.close()

     print("JSON Data written into %s successfully!"%self.dest)


  def __str__(self):
      self.date = datetime.datetime.now().strftime('%d %B %Y')
      return "This class handles remote csv files.\n"+"*"*40+"\nCalled at %s"%self.date




