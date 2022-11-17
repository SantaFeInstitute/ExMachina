#JHM 21June2018 
#does data analysis/graphing for simple commerce sweep runs
#these procedures are closely tied to how the data is output, so be careful with changes either
#here or at the program level!

#this should be run in the Output directory

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

""" 
dim = data.shape #dimensions of the data array
states = np.unique(data[:,0]) #find the unique values of states
rounds = np.unique(data[:,1]) #find the unique values of rounds

  grid = GridSpec(len(Bvalues),len(Dvalues))
  labels = '00','alt','11' #labels for the pie chart
  colors = ['limegreen','yellow','tomato'] #colors for the chart
  for obs in range(0,dim[0]): #for each observationo
    row = len(Bvalues)-1 - Bvalues.tolist().index(data[obs,0]) #find the B index and reverse the y-axis presentation
    col = Dvalues.tolist().index(data[obs,1]) #find the D index
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

  plt.suptitle("COOPERATIONSTAG"+str(tstates)+"s"+str(rop)+"r (b/d)") #label entire figure, eliminate for final figs
  plt.show() #doesn't show if PS is invoked
  plt.savefig("COOPERATESTAG"+str(tstates)+"s"+str(rop)+"r") #create a PS file of the fig
  plt.clf() #clear the plot
"""
