#JHM 4Feb2019
#not the most beautiful code, but...
#graphs of actions for full game, plus strats and actions  during each epoch transition
#these procedures are closely tied to how the data is output, so be careful with changes either
#here or at the program level!

#run directly in the directory with the .idx, .dat., etc files

import glob #used to grab all the file names 
import matplotlib #include for postscript output
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

#save the plot as a jpg file
def finalizePlot(plt,file):
  #plt.show() #doesn't show if PS is invoked
  plt.savefig(file+".jpg",format="jpg") #create a file of the fig given format
  plt.clf() #clear the plot
  return;

#plot out the strategies during a transition
def plotTrans(data,legend,generations,popnum,finalize):
  data = np.asarray(data) #convert to np arrays for processing and plotting
  data = np.transpose(data) #data needs to be by generation versus strategy
  generations = np.asarray(generations)
  plt.ylim(0,40) #set the y-axis range  *** Assumes pop size of 40!
  for p in range(41): #0...40 used to list strategies from largest to smallest max attained
    for d in range(0, len(legend)-1): #each strategy observed in transition period
      if max(data[:,d]) == (40-p): #maximum pop size attained for strategy d 
        plt.plot(generations[:], data[:,d], label=legend[d])
  plt.xlabel('Generation') #label the axes
  plt.ylabel('Population Size')
  plt.title('Population '+popnum) 
  plt.subplots_adjust(right=0.5) #reduce the width so we can fit the legend
  plt.legend(loc='center left', bbox_to_anchor=(1,0.5)) #put the legend on outside, right
  if finalize: #save to a file
    finalizePlot(plt,'epochP'+popnum+'-'+str(genstart)+'-'+str(genend))
  return plt;

#plot out the actions by generation, assumes 4! possible action pairings
def plotActions(data,legend,genstart,genend,finalize): 
  plt.ylim(0.0,1.0) #set the y-axis range
  for p in range(1, 5): #each possible action pairing
    plt.plot(data[genstart-1:genend,0], data[genstart-1:genend,p], label=legend[p])
  plt.xlabel('Generation') #label the axes
  plt.ylabel('Proportion')
  plt.title('') #eliminate for final figs
  #width works at 0.75 below, but use 0.5 to align with transiton graphs
  plt.subplots_adjust(right=0.5) #reduce the width so we can fit the legend
  plt.legend(loc='center left', bbox_to_anchor=(1,0.5)) #put the legend on outside, right
  if finalize: #save to a file
    finalizePlot(plt,'gameplay'+str(genstart)+'-'+str(genend))
  return;

header = "" #will hold the appropriate header for files in the directory
files = glob.glob('*') #get the files
for fname in files:
  temp = fname.split('.') #split up file name by .
  if (temp[1] == 'idx'): #.idx is the index file program creates, so header is the right one
    header = temp[0]

#print out the observed actions during the generations
#*** Assumes 4 possible actions!!! *** easy to modify...

print('making action plot across all generations')
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
    actdata.append([int(newdata[0]),newdata[1],newdata[2],newdata[3],newdata[4]])
actdata = np.asarray(actdata) #convert to np arrays for processing and plotting
plotActions(actdata,actlegend,int(actdata[0,0]),int(actdata[-1,0]),True) #plot the actions for every generation

print('making epoch plots')
#now plot out the strategies in the epochs
files = glob.glob('*') #get the files
for fname in files: #identify the epoch files
  title = fname.split('.') #split up file name by .
  key = title[1]
  if (key[:5] == 'Epoch') and (key[:6] != 'Epochs'): #we have an individual epoch file
    fh = open(fname)
    flag0 = False #flags used to keep track of what data we are getting
    flag1 = False
    pop0line = []
    pop1line = []
    for line in fh: #each line in the epoch file
      if line[:22] == 'Compact Analysis (BEAs':  #at the correct panel of data in the file
        temp = line.split() #find the generations in the data
        genstart = int(temp[10]) #starting gen of this transition
        genend = int(temp[15]) #ending gen
        print('Epoch from:',genstart,'to',genend)
        flag0 = True #first panel has pop0 data
      if line[:5] == 'Pop 1' and flag0 == True: #start of second panel with pop1 data
        flag0 = False
        flag1 = True
      if line[:5] == 'Perce': #end of second panel
        flag0 = False
        flag1 = False
      if flag0 or flag1:
        if line[:3] == 'bea': #a line of strategy data
          if flag0: #in pop0 panel of data
            pop0line.append(line) 
          if flag1: #in pop1 panel of data
            pop1line.append(line)
    legend0 = [] #grab the legend
    data0 = []
    legend1 = [] #grab the legend
    data1 = []
    generations = []
    for x in pop0line: #get the pop 0 data that we need for the plots
      breakit = x.split()
      legend0.append(breakit[-1]) #last item in the list is the strategy description
      data0.append([int(x) for x in breakit[2:-2]]) #convert the list from 2nd item to 2nd from last to ints
    for x in pop1line: #get the pop 1 data that we need for the plots
      breakit = x.split()
      legend1.append(breakit[-1])
      data1.append([int(x) for x in breakit[2:-2]]) #convert the list to ints
    for x in range(genstart,genend+1): #create the generations data
      generations.append(x)
    plt0 = plotTrans(data0,legend0,generations,'0',True); #plot pop0 strategies
    plt1 = plotTrans(data1,legend1,generations,'1',True); #plot pop1 strategis
    plta = plotActions(actdata,actlegend,genstart,genend,True)# plot actons observed over the transition gens

    #put it all on one graph--- not working
"""
    grid = GridSpec(3,1, hspace = 0.5)
    plt = plt0.subplot(grid[0,0])
    plt = plt1.subplot(grid[1,0])
    plt = plta.subplot(grid[2,0])
"""

print('Program terminated normally...')
