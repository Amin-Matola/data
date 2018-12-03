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


  def __init__(self,file_location,destination,*fieldnames):
    self.file = file_location
    self.dest = destination
    self.data_fields = fieldnames
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
        return "Error openning file at %s.\n %s"%(self.dest,e)
    else: #--------Then it is a file in a local disk----------------|
        self.remote_file = open(self.dest,'r+')
        self.remote_file_string = self.remote_file.read()

    self.process_data()

  def process_data(self):
    print('processing request data...')
    if self.file_loc=='internet':
        self.file_lines = self.remote_file_string.split('\n')
        self.comma_list = [a.split(',') for a in self.file_lines]
        self.data_list  = []
        for b in self.comma_list:
            self.data_list += b
        self.file_lines = self.data_list

    else:
        self.file_lines = self.remote_file_string



    if len(self.data_fields):
      self.file_dict  = csv.DictReader(self.file_lines,fieldnames=self.data_fields[0])
    else:
      return "The syntax for calling this class is data=Data(file_location,destination_file,iterable_field_names)"
    self.convert_to_json()

  def convert_to_json(self):
     print('converting to json...')
     self.json_data = json.dumps([line for line in self.file_dict])
     self.write_to_json_file()

  def write_to_json_file(self):
     print('writing to json file...')
    #------- Now store json results, the 'with' will automatically close the file once done.------|
     try:
      self.local_file = open(self.dest,'w+')
      self.local_file.write(self.json_data)
      self.local_file.close()

     except Exception as e:
        self.error = """Wo! Wo! Wait, there was an error writing to %s,
                       please check destination file location.\n The error returned was %"""%(self.dest,self.error)

        choice     = input(self.error+"\n Would you like us to create this file for you in the current directory?(y/n)")
        if choice.lower()=='y':
          if len(self.dest.split('/'))>1:
           self.dest = os.mknod(os.path.join(os.getcwd(),self.dest.split('/')[-1]))

           #-------------Go to storage processing again--------|
           self.write_to_json_file()
          else:
            self.dest = os.mknod(os.getcwd()+self.dest)
            self.write_to_json_file()
        else:
           return self.error

     print("JSON Data written into %s successfully!"%self.dest)


  def __str__(self):
      self.date = datetime.datetime.now().strftime('%d %B %Y')
      return "This class handles remote csv files.\n"+"*"*40+"\nCalled at %s"%self.date




