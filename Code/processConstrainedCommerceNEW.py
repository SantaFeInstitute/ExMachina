#JHM 24June2018 
#does data analysis/graphing on a directory of separate ConstrainedCommerce runs
#these procedures are closely tied to how the data is output, so be careful with changes either
#here or at the program level!

#run in the Output directory

import glob #used to grab all the file names 

#imports for plotting (for ps output, include next two lines and line near end of file
import matplotlib #include for postscript output
matplotlib.use('PS') #include for postscript output, exclude otherwise
import matplotlib.pyplot as plt
#from matplotlib.gridspec import GridSpec
import numpy as np

gstart = 1000 #generation to start collecting data
gend = 4999 

directory = "Output" #directory with the individual run files

dfiles = glob.glob(directory+'/*') #get the directories
for dname in dfiles:
  files = glob.glob(dname+'/*') #get the files in the directory
  for name in files: #for each file in the directory
    adata = [] #holds the data for each run
    bdata = []
    name = name[len(dname)+1:] #remove the directory name and / 
    fh = open(dname+'/'+name+'/'+name+'.txt','r') #open the general info file
    for line in fh: #for each line in the file
      x = line.find("TStates: ") #find total states
      if (x != -1):
        tstates = int(line[x+9:x+12]) #pull off total states---format is important
        print("Tstates",tstates)
      x = line.find("RoundsOfPlay: ") #pull off rounds of play
      if (x != -1):
        rop = int(line[x+14:x+16])
        print("Rounds",rop)
      x = line.find("TAgents: ") #pull off rounds of play
      if (x != -1):
        print(line[x+8:x+4])
        tagents = int(line[x+8:x+12])
        print("Tagents",tagents)
      x = line.find("Endowment:")#get the endowment
      if (x != -1):
        endowment = int(line[11:]) #grab the endowment
        print("endowment",endowment)
    fh.close()

    #get the key data about observed plays for a given generation
    fh = open(dname+'/'+name+'/'+name+'.processed.txt','r') #open the epoch file
    i = 0;
    for line in fh:
      i += 1
      if (i > 2): #ignore the first two lines
        gen = int(line[0:7]) #read off the generation
      else:
        gen = 0;      
      if (gen >= gstart) and (gen <= gend): #gens between (and incl) gstart and gend
#        print(line)
        start = line.find("start ")  #get to the data
        end = line.find("end ");
        dataline = line[start+6:end]
#        print("dline:",dataline)
        splitdata = dataline.split(',')
        for i in range(len(splitdata)-1):
          if i % 2 == 0:
            adata.append(int(splitdata[i]))
          else:
            bdata.append(int(splitdata[i]))
    fh.close()

    #print("adata:",adata)
    #print("bdata:",bdata)

    adata = np.asarray(adata) #convert to np arrays for processing and plotting
    bdata = np.asarray(bdata) #convert to np arrays for processing and plotting

    h = np.zeros((endowment+1,endowment+1)) #h[good 0 0..10, good 1 0..10]
    sum = 0
    for i in range(len(adata)):
      h[adata[i],bdata[i]] += 1
      sum += 1
    for r in range(h.shape[0]):
      for c in range(h.shape[1]):
        h[r,c] = 1.0*h[r,c]/sum
    np.set_printoptions(precision=2, suppress=True)
    #reverse print the matrix to make an edgeworth box?
    for c in range(h.shape[1]):
      print((h.shape[1]-c-1),h[:,(h.shape[1]-c-1)])

#    np.histogram2d(adata,bdata,bins=21,normed=True)

    plt.matshow(h.T, origin="lower",cmap=plt.cm.Reds) #transpose of matrix,
    plt.gca().xaxis.tick_bottom()

    """
    #bins = np.arange(endowment+1) - 0.5
    plt.hist2d(adata,bdata,range=np.array([(0, endowment),(0, endowment)]), cmap=plt.cm.Reds)
    #plt.hist2d(adata,bdata,range=np.array([(bins),(bins)]), cmap=plt.cm.Reds)
    plt.xlim([0,endowment])
    plt.ylim([0,endowment])
    """

    plt.colorbar()
    plt.title("CC"+str(tstates)+"s"+str(rop)+"r"+str(endowment)+"eG"+str(gstart)+"--"+str(gend))
    plt.show() #doesn't show if PS is invoked
    plt.savefig("CCsame"+str(tstates)+"s"+str(rop)+"r"+str(endowment)+"e.jpg",format="jpg") #create a PS file of the fig
    plt.clf() #clear the plot

