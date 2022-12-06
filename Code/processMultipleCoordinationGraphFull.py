#JHM 17June2018 
#does data analysis/graphing on a directory of separate BOS runs
#these procedures are closely tied to how the data is output, so be careful with changes either
#here or at the program level!

#run in the Output directory

import glob #used to grab all the file names 

#imports for plotting (for ps output, include next two lines and line near end of file
import matplotlib #include for postscript output
matplotlib.use('PS') #include for postscript output, exclude otherwise
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

def plotIt(plt,data,title):
  plt.ylim(0.0,1.0) #set the y-axis range
  plt.plot(data[:,0], data[:,1], label='(0,0)')
  plt.plot(data[:,0], data[:,2], label='(0,1)')
  plt.plot(data[:,0], data[:,3], label='(1,0)')
  plt.plot(data[:,0], data[:,4], label='(1,1)')
  plt.plot(data[:,0], data[:,5], linestyle = ':', label='<00 11> or\n<11 00>')
  plt.xlabel('(V-C)/2') #label the axes
  plt.ylabel('proportion')
  plt.title(title) #eliminate for final figs
  plt.subplots_adjust(right=0.75) #reduce the width so we can fit the legend
  plt.legend(loc='center left', bbox_to_anchor=(1,0.5)) #put the legend on outside, right
  return (plt);

def finalizePlot(plt,file):
  plt.show() #doesn't show if PS is invoked
  plt.savefig(file) #create a PS file of the fig
  plt.clf() #clear the plot
  return;

directory = "Output" #directory with the individual run files

toplot = [None]*20 #will hold the various plots...assumes a given structure
dfiles = glob.glob(directory+'/*') #get the directories
for dname in dfiles:
  files = glob.glob(dname+'/*') #get the files in the directory
  data = [] #holds the data for each run
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
      x = line.find("5.000,")#get the M parameter
      if (x != -1):
        m = float(line[x+6:x+12])
    fh.close()

    #get the key data about observed plays 
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

    #calculate the average time in a key terminal cycle
    #closely tied to set up
    fh = open(dname+'/'+name+'/'+name+'.processed.txt','r') #open the processed data file
    counter = 0
    termcycletime = 0.0
    for line in fh:
      counter += 1
      if (counter > 2):  #clear out first two lines of file
        #print(line[99:104], line[105:110])
        termcycletime += float(line[99:104]) + float(line[105:110])

    #print(name,tstates,rop,m,x00,x01,x10,x11,round(termcycletime/(counter-2),3),sep=", ")

    data.append([m,x00,x01,x10,x11,termcycletime/(counter-2)]) #add to the data array

  data = np.asarray(data) #convert to np arrays for processing and plotting
  data = data[data[:,0].argsort()] #sort by M value (in the 0th column)
  #print out the files
  print("\nCoordination",str(tstates)+"s",str(rop)+"r")
  print(data)

  #plot out the individual files
  plotIt(plt,data,"COORDINATION "+str(tstates)+"s "+str(rop)+"r")
  finalizePlot(plt,"COORDINATION"+str(tstates)+"s"+str(rop)+"r")

 
  r = 0
  if rop == 4:
    r = 1
  if rop == 10:
    r = 2
  toplot[(tstates-1)*3 + r] = data

for s in range(1,6):
  grid = GridSpec(3,1, hspace = 0.5)
  #grid.update(hspace = 1.5)
  for r in range(0,3):
    round = 1;
    if r == 1:
      round = 4;
    if r == 2:
      round = 10
    data = toplot[(s-1)*3+r] 
    plt.rcParams.update({'font.size':5})
    plt.subplot(grid[r,0])
    plotIt(plt,data,"COORDINATION "+str(s)+"s "+str(round)+"r")
  finalizePlot(plt,"pCORDINATION"+str(s)+"s")
