# IMPORT STATEMENTS

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from multiprocessing import Process, Queue
from psychopy import locale_setup, visual, core, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import csv
import sys # to get file system encoding
import random
from pylsl import StreamInlet, resolve_stream

#######  LSL Streaming
print("looking for an EEG stream...")
streams = resolve_stream('type','EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

print("Found it!")
#####Getting the CSV File ready

#Make sure you are in the correct directory
os.chdir('/home/sydney/Brainlock')


#####



#IMPORT CUSTOM MODULES
#from Password_Setup import *

#PRE-LOAD STIMS

knownA= range(10)
unknowA= range(10)


#### Acronym List #######
with open('acr.csv','r') as acr:

    reader=csv.reader(acr)
    knownA = reader.next()
    unknownA= reader.next()


##### Create a CSV with the person's name. This is the person's ID
usern = raw_input("Enter your username:")
lSize = raw_input("Enter your sample Size")
lSize =int(lSize)
#####


#Create the List of Acronyms with known and Unknown
#for i in range(len(knownA)):
#    if i % 2 == 0:
#        acrL[i]=knownA[i]
#    else:
#        acrL[i]=unknownA[i]
######

#acrL=range(len(knownA))    

####Create a Random List of Acronyms/ ####Change Size based on what you need 

#acrLknown = random.sample(knownA,(lSize/2))        

acrLknown = [knownA[i] for i in sorted(random.sample(xrange(len(knownA)), int(lSize/2))) ]
acrlunknown = [unknownA[i] for i in sorted(random.sample(xrange(len(unknownA)), int(lSize/2))) ]

#indices = random.sample(range(len(knownA)), int(lSize/2))
#[knownA[i] for i in sorted(indices)]

#print knownA

acrLknown.extend(acrlunknown)
acrL=acrLknown
print acrL

random.shuffle(acrL)

#if lSize is not 0:
#    acrL=acrL[:lSize]
######/end Acronym List ##############



#INTRO SCREEN
win = visual.Window(size=(1366, 768), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )

#CREATE NONTEXT OBJECTS 


fixation = visual.GratingStim(win=win, mask='cross', size=0.5, pos=[0,0], sf=0.1)

sync = visual.ShapeStim(win, units='', lineWidth=1.5, lineColor='white', 
    lineColorSpace='rgb', fillColor='white', fillColorSpace='rgb', 
    vertices=((0.8, 0.9), (0.9, 0.9), (0.9, 0.8), (0.8,0.8)),
    closeShape=True, pos=(0, 0), size=1, ori=0.0, opacity=1.0, 
    contrast=1.0, depth=0, interpolate=True, name=None, 
    autoLog=None, autoDraw=False)



####Variables For the Loop#####
clock=core.Clock()
stim= True
acrdone= False
psydone= False
#i= 0
#j=0

###/End of Variables For the Loop#####

def fix(val1,val2):
    var=True
    if val1==0:
        return var
    if val1==1:
       var=val2
       print var


def lsl(q):   
    with open(usern+'.csv','wb') as f:
        writer = csv.writer(f)
        power=1
        stim= "+"
        #if not q.empty():
        #   power,stim =q.get() 
            
        while power==1:    
            if q.empty():
                sample,timestamp = inlet.pull_sample()
                data=[stim,timestamp]
                data.extend(sample)
                writer.writerow(data)
            else:
                power,stim =q.get()



###Code Below is all the  Main Loop #####

if __name__ == "__main__":    
    q= Queue()
#    q.put([1,"+"])
    l= Process(target=lsl,args=(q,))
    l.start()
    for k in range(len(acrL)):
        word = visual.TextStim(win=win, ori=0, name='word',
        text=acrL[k],font=u'Arial',
        pos=[0, 0], height=0.5, wrapWidth=300,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)
        #i=k                      
        for frameN in range(180):
            win.flip()
            if frameN ==0:
                q.put([1,"+"])            
            if 0 <= frameN < 60:	   	
##                print("0-60: Time - %f",(clock.getTime()))
                fixation.draw()
                
            if frameN == 60:
                q.put([1,acrL[k]])
            if 60 <= frameN < 180:
                word.draw()
##                print("60-180: Time - %f",(clock.getTime()))
            
    q.put([0,""])
    l.terminate()            
    win.close()    
               

