#JHM 16July2018 
#does data analysis/graphing for codification runs
#these procedures are closely tied to how the data is output, so be careful with changes either
#here or at the program level!

#this should be run in the Output directory

import glob #used to grab all the file names 

#imports for plotting (for ps output, include next two lines and line near end of file
import matplotlib #include for postscript output
matplotlib.use('PS') #ONLY include for postscript output
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

data = [] #holds the data for each run
directory = "output" #directory with the individual run files

dfiles = glob.glob(directory+'/*') #get the directories
for dname in dfiles:
  files = glob.glob(dname+'/*') #get the files in the directory
  for name in files: #for each file in the directory
    name = name[len(dname)+1:] #remove the directory name and / 
    fh = open(dname+'/'+name+'/'+name+'.txt','r') #open the general info file
    pop2 = False
    for line in fh: #for each line in the file
      x = line.find("Population 2:") #see if tstates is for the observer
      if (x != -1):
        pop2 = True
      x = line.find("TStates: ") #find total states
      if (x != -1):
        if (not pop2):
          tstates = int(line[x+9:x+12]) #pull off total states---format is important
        else:
          tstatesObs = int(line[x+9:x+12]) #pull off total states---format is important
      x = line.find("RoundsOfPlay: ") #pull off rounds of play
      if (x != -1):
        rop = int(line[x+14:x+16])
      x = line.find("CARROT payoff") #get the carrot payoff
      if (x != -1):
        colon = line.find(":")
        carrot = float(line[colon+1:colon+10]) #pull off the reward value
      x = line.find("STICK payoff") #get the stick payoff
      if (x != -1):
        colon = line.find(":")
        stick = float(line[colon+1:colon+10]) #pull off the reward value
      x = line.find("Penalty Imposed") #get the imposed penalty on players
      if (x != -1):
        colon = line.find(":")
        penalty = float(line[colon+1:colon+10]) #pull off the reward value
    fh.close()

    #get the data about observed plays 
    #this only works for observers with 2 NOT 4 actions
    fh = open(dname+'/'+name+'/'+name+'.Epochs.txt','r') #open the epoch file
    for line in fh:
      x = line.find("-> (0,0,0):")  #grab the percent of 0,0,0 play
      if (x != -1): 
        x000 = float(line[x+11:x+17])
      x = line.find("-> (0,0,1):")  #grab the percent of 0,0,1 play
      if (x != -1): 
        x001 = float(line[x+11:x+17])
      x = line.find("-> (1,1,0):")  #grab the percent of 1,1,0 play
      if (x != -1): 
        x110 = float(line[x+11:x+17])
      x = line.find("-> (1,1,1):")  #grab the percent of 1,1,1 play
      if (x != -1): 
        x111 = float(line[x+11:x+17])
      x = line.find("-> (0,1,0):")  #grab the percent of 0,0,0 play
      if (x != -1): 
        x010 = float(line[x+11:x+17])
      x = line.find("-> (0,1,1):")  #grab the percent of 0,0,1 play
      if (x != -1): 
        x011 = float(line[x+11:x+17])
      x = line.find("-> (1,0,0):")  #grab the percent of 1,1,0 play
      if (x != -1): 
        x100 = float(line[x+11:x+17])
      x = line.find("-> (1,0,1):")  #grab the percent of 1,1,1 play
      if (x != -1): 
        x101 = float(line[x+11:x+17])
    fh.close()

    #print(name,tstates,tstatesObs,rop,carrot,stick,penalty,sep=", ")
    #print(x000,x001,x110,x111,x100,x101,x010,x011,sep=", ") #all possible auto actions
    #print(x000+x001,x110+x111,x001+x011+x101+x111,sep=",") # 0,0 plays, 1,1 plays, and % time a penalty was imposed

    #get the data about ideal outcome 
    fh = open(dname+'/'+name+'/'+name+'.processed.txt','r') #open the processed file
    l = 0
    cycle = 0.0
    for line in fh:
      l += 1
      if (l > 2):
        d = line.split()
        gen = int(d[0]) #generation
        cycle += float(d[-2]) #penultimate data point is the % of <0,0 1,1> cycles
    fh.close()
    #print(cycle/gen) #average over total generations
    
    print(tstates,tstatesObs,carrot,stick,x000+x001,x110+x111,x001+x011+x101+x111,cycle/gen,sep=",")    
    data.append([tstates,tstatesObs,carrot,stick,x000+x001,x110+x111,x001+x011+x101+x111,cycle/gen])

data = np.asarray(data) #convert to np arrays for processing and plotting
data = data[np.lexsort((data[:,3],data[:,2],data[:,1],data[:,0],data[:,7]))] #lexiographcally sort by tstate, then obsstate

dim = data.shape
print("dim",dim)

for obs in range(0,dim[0]):
  st = ["%.3f" % c for c in data[obs]] #nicely format the data row
  print(st)


    #print(tstates,tstatesObs,carrot,stick,x000+x001,x110+x111,x001+x011+x101+x111,cycle/gen,sep=",")

"""
    if ((10*reward % 5) == 0) and ((10*punishment % 5) == 0):
      data.append([reward,punishment,x00,x01+x10,x11]) #add to the data array

  data = np.asarray(data) #convert to np arrays for processing and plotting
  data = data[np.lexsort((data[:,1],data[:,0]))] #lexiographcally sort by reward, then punishment
 
  print(data) #just prints out the data matrix
  #generate a series of pie charts by reward and punishment values
  dim = data.shape #dimensions of the data array
  reward = np.unique(data[:,0]) #find the unique values of rewards (will be ordered from low to high)
  punishment = np.unique(data[:,1]) #find the unique values of punishment (will be ordered from low to high)
  grid = GridSpec(len(reward),len(punishment))
  labels = '00','alt','11' #labels for the pie chart
  colors = ['limegreen','yellow','tomato'] #colors for the chart
  for obs in range(0,dim[0]): #for each observationo
    row = len(reward)-1 - reward.tolist().index(data[obs,0]) #find the reward index and reverse the y-axis presentation
    col = punishment.tolist().index(data[obs,1]) #find the punishment index
    print("Observation:",obs,data[obs,0],data[obs,1],row,col)
    plt.subplot(grid[row,col], aspect=1) #locate the pie chart in the overall figure
    ##plt.pie(data[obs,2:5], labels=labels, startangle=90, colors=colors) #plot the pie chart
    plt.pie(data[obs,2:5], startangle=90, colors=colors) #plot the pie chart
    #plt.title(str(data[obs,0])+"/"+str(data[obs,1]),fontsize=5) # title each individual chart
    if ((row == 0) and (col == 0)):
      plt.title(str(data[obs,0])+"/"+str(data[obs,1]),fontsize=5) # title each individual chart
    if ((row == 0) and (col != 0)):
      plt.title("./"+str(data[obs,1]),fontsize=5) # title each individual chart
    if ((row != 0) and (col == 0)):
      plt.title(str(data[obs,0])+"/.",fontsize=5) # title each individual chart
    donut = plt.Circle((0,0),0.70,fc='white') #this and the next line put a donut hole in the chart
    plt.gca().add_artist(donut)

  plt.suptitle("SpCOOPERATION"+str(tstates)+"s"+str(rop)+"r (R/P)") #label entire figure, eliminate for final figs
  plt.show() #doesn't show if PS is invoked
  plt.savefig("sparseCOOPERATE"+str(tstates)+"s"+str(rop)+"r") #create a PS file of the fig
  plt.clf() #clear the plot
"""
