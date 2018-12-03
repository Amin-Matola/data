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
    self.file_loc = 'internet'
    self.check_inputs()
    
   def check_inputs(self):
    #-----------The url must start with 'http(s)' for urllib to open it successfully,otherwise it is on local disk-------|
    if self.file.lower().startswith('http'):
      pass
    
    elif self.file[:3].lower() == 'www':
      self.file = 'http://%s'%self.file
      
    elif self.file.startswith('C:\') or self.file.startswith(r'/usr'):
       self.file_loc = 'local'
      
    else:
      return "Your location is invalid, it must start with 'http' or 'www'"
    
    self.process_request()
      
   def process_request(self):
    if self.file_loc == 'internet': #------Then process url--------#                  
      try:
        self.remote_file = opener.open(self.file)
        self.remote_file_bytes = remote_file.read()
        self.remote_file_string= remote_file.decode()
      except Exception as e:
        return "Error openning file at %s.\n %s"%(self.dest,e)
    else: #--------Then it is a file in a local disk----------------|
        self.remote_file = open(self.dest)
        self.remote_file_string = remote_file.read()
     
    self.process_data()
    
   def process_data(self):
    self.file_lines = self.remote_file_string.split('\n')
    if len(self.data_fields):
      self.file_dict  = csv.DictReader(self.file_lines,fieldnames=self.data_fields[0])
    else:
      self.file_dict  = list(csv.reader(self.file_lines))
      self.convert_to_json()
      
   def convert_to_json(self):
     self.json_data = json.dumps([line for line in self.file_dict])
     write_to_json_file()
     
   def write_to_json_file(self):
    #------- Now store json results, the 'with' will automatically close the file once done.------|
     try:
      with open(self.dest,'r+') as storage:
       storage.write(self.json_data)
     except Exception as e:
        self.error = """Wo! Wo! Wait, there was an error writing to %s, 
                       please check destination file location.\n The error returned was %"%(self.dest,self.error)
                       
        choice     = input(self.error+"\n Would you like us to create this file for you in the current directory?(y/n)")
        if choice.lower()=='y':
          if len(self.dest.split('/'))>1:
           self.dest = os.mknod(os.path.join(os.getcwd(),self.dest.split('/')[-1]))
           
           #-------------Go to storage processing again--------|
           write_to_json()
          else:
            self.dest = os.mknod(os.getcwd()+self.dest)
            write_to_json()
        else:
           return self.error
        
     return "JSON Data written into %s successfully!"%self.dest
   
       
   def __str__(self):
      self.date = datetime.datetime.now().strftime('%d %B %Y')
      return "This class handles remote csv files.\n"+"*"*40+"\nCalled at %s"%self.date
      
     
      
    
