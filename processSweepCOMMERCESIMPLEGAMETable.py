#JHM 21June2018 
#does data analysis of sweeps for a simple trading game for commerce
#Outputs the key table in LaTex format

#tied to the output stream, so be careful if you make changes there or here
#run in the directory above "output"
#invoke with "python processSweepCOMMERCESIMPLEGAMETable.py > Output_COMMERCESIMPLEGAMETable.txt"

import glob #used to grab all the file names 
import numpy as np
directory = "output" #directory with the individual run files

data = [] #holds the data for each run
dfiles = glob.glob(directory+'/*') #get the subdirectories
for dname in dfiles:
  files = glob.glob(dname+'/*') #get the files in the sub-subdirectory
  for name in files: #for each file in the directory
    name = name[len(dname)+1:] #remove the directory name and / 
    fh = open(dname+'/'+name+'/'+name+'.txt','r') #open the general info file
    for line in fh: #for each line in the file
      x = line.find("TStates: ") #find total states
      if (x != -1):
        tstates = int(line[x+9:x+12]) #pull off total states---format is important
      x = line.find("RoundsOfPlay: ") #pull off rounds of play
      if (x != -1):
        rop = int(line[x+14:x+16])
    fh.close()

    #get the data about observed plays in terms of % of time in 00 01 10 11 
    fh = open(dname+'/'+name+'/'+name+'.Epochs.txt','r') #open the epoch file
    for line in fh:
      x = line.find("-> (0,0):")  #grab the percent of 0,0 play
      if (x != -1): 
        x00 = float(line[x+9:x+14])
      x = line.find("-> (0,1):")  #grab the 0,1 play
      if (x != -1): 
        x01 = float(line[x+9:x+14])
      x = line.find("-> (1,0):") #grab the 1,0 play
      if (x != -1): 
        x10 = float(line[x+9:x+14]) 
      x = line.find("-> (1,1):")  #grab the 1,1 play
      if (x != -1): 
        x11 = float(line[x+9:x+14])
    fh.close()

    print(name,tstates,rop,x00,x01,x10,x11,sep=", ")

    data.append([tstates,rop,x00,x01,x10,x11]) #add to the data array

print("*********************")
data = np.asarray(data) #convert to np arrays for processing and plotting
data = data[np.lexsort((data[:,1],data[:,0]))] #lexiographcally sort by tstates,rop
 
print(data) #just prints out the data matrix
#generate a data table suitable for latex
print("States & Rounds & $\{0,0\}$ & $\{0,1\}$ & $\{1,0\}$ & $\{1,1\}$ \\\\")
st = 0
for line in data:
  if (st == line[0]):
    state = " "
  else:
    print("\hline")
    st = line[0]
    state = str(int(line[0]))
  print(state,"&",str(int(line[1])),"&",str(round(line[2],2)),"&",str(round(line[3],2)),"&",str(round(line[4],2)),"&",str(round(line[5],2)),"\\\\")