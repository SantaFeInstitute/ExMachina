#JHM 4Feb2019
#graphics of actions and strats during epoch transitions
#Takes an individual run and generates some key graphics
#these procedures are closely tied to how the data is output, so be careful with changes either
#here or at the program level!

#run in the directory with the .idx, .dat., etc files

import glob #used to grab all the file names 
import matplotlib #include for postscript output
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

def finalizePlot(plt,file):
  #plt.show() #doesn't show if PS is invoked
  plt.savefig(file+".jpg",format="jpg") #create a file of the fig given format
  plt.clf() #clear the plot
  return;

def plotTrans(data,legend,generations,popnum):
  data = np.asarray(data) #convert to np arrays for processing and plotting
  data = np.transpose(data)
  #print(max(data[:,1])) #highest number attained in pop for 1
  generations = np.asarray(generations)
  plt.ylim(0,40) #set the y-axis range
  for p in range(41): #0...40
    for d in range(0, len(legend)-1):
      if max(data[:,d]) == (40-p): 
        plt.plot(generations[:], data[:,d], label=legend[d])
  plt.xlabel('Generation') #label the axes
  plt.ylabel('Population Size')
  plt.title('Population '+popnum) #eliminate for final figs
  plt.subplots_adjust(right=0.5) #reduce the width so we can fit the legend
  plt.legend(loc='center left', bbox_to_anchor=(1,0.5)) #put the legend on outside, right
  finalizePlot(plt,'epochP'+popnum+'-'+str(genstart)+'-'+str(genend))
  return;

def plotActions(data,legend,genstart,genend): 
  plt.ylim(0.0,1.0) #set the y-axis range
  for p in range(1, 5):
    plt.plot(data[genstart-1:genend,0], data[genstart-1:genend,p], label=legend[p])
  plt.xlabel('Generation') #label the axes
  plt.ylabel('Proportion')
  plt.title('') #eliminate for final figs
  plt.subplots_adjust(right=0.75) #reduce the width so we can fit the legend
  plt.legend(loc='center left', bbox_to_anchor=(1,0.5)) #put the legend on outside, right
  finalizePlot(plt,'gameplay'+str(genstart)+'-'+str(genend))
  return;

header = "" #will hold the appropriate header for files in the directory
files = glob.glob('*') #get the files
for fname in files:
  temp = fname.split('.') #split up file name by .
  if (temp[1] == 'idx'):
    header = temp[0]

#print out the observed actions during the generations
#*** Assumes 4 possible actions!!! *** easy to modify...

actdata = [] #holds the data 
actlegend = [] #holds the legend 
fh = open(header+'.processed.txt')
lc = 0 #line count
for line in fh: #each line in the processed.txt file 
  lc = lc +1
  if (lc == 2):
    actlegend = line.split() #splits by words separated by any number of spaces
    if (actlegend[0] != 'Gen'):
      print('Unexpected input *** DO NOT USE ***')
  if (lc > 2):
    newdata = [float(x) for x in line.split()] #convert the list to floats
    if ((lc-2) != int(newdata[0])):
      print('Unexpected Generation *** DO NOT USE ***')
#    if (int(newdata[0]) >= genstart) and (int(newdata[0]) <= genend): 
    actdata.append([int(newdata[0]),newdata[1],newdata[2],newdata[3],newdata[4]])
actdata = np.asarray(actdata) #convert to np arrays for processing and plotting
plotActions(actdata,actlegend,int(actdata[0,0]),int(actdata[-1,0]))# every generation

print('making epoch plots')
#now plot out the strategies in the epochs
files = glob.glob('*') #get the files
for fname in files: #identify the epoch files
  title = fname.split('.') #split up file name by .
  key = title[1]
  if (key[:5] == 'Epoch') and (key[:6] != 'Epochs'): #we have an epoch file
    fh = open(fname)
    flag0 = False
    flag1 = False
    pop0line = []
    pop1line = []
    for line in fh: #each line in the epoch file
      if line[:22] == 'Compact Analysis (BEAs': 
        temp = line.split() #find the generations in the data
        genstart = int(temp[10])
        genend = int(temp[15]) 
        print('Epoch from: ',genstart,genend)
        flag0 = True
      if line[:5] == 'Pop 1' and flag0 == True:
        flag0 = False
        flag1 = True
      if line[:5] == 'Perce':
        flag0 = False
        flag1 = False
      if flag0 or flag1:
        if line[:3] == 'bea':
          if flag0: 
            pop0line.append(line) 
          if flag1:
            pop1line.append(line)
    legend0 = [] #grab the legend
    data0 = []
    legend1 = [] #grab the legend
    data1 = []
    generations = []
    for x in pop0line:
      breakit = x.split()
      legend0.append(breakit[-1])
      data0.append([int(x) for x in breakit[2:-2]]) #convert the list to ints
    for x in pop1line:
      breakit = x.split()
      legend1.append(breakit[-1])
      data1.append([int(x) for x in breakit[2:-2]]) #convert the list to ints
    for x in range(genstart,genend+1):
      generations.append(x)
    plotTrans(data0,legend0,generations,'0');
    plotTrans(data1,legend1,generations,'1');
    plotActions(actdata,actlegend,genstart,genend)# generations of transitons
 
print('end')
