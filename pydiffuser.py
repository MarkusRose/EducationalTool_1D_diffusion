'''
PyDiffuser
2016-07-09 Markus Rose

This is a 1-dimensional diffusion simulation.
'''


''' Import needed packages
'import <package> as <name-user-can-assign>'
'''
import numpy as np   #Numpy is a scientific package to help with array computations
import matplotlib.pyplot as plt #Plotting package
import matplotlib.animation as animation
import random    #collection of random number generators
import math      #get pi





''' Initial Global Variables '''
track = []    #Get initial track as an empy list. I will hold the positions over time
stepstaken = [] #remember step sizes for convenience
steptime = 0.03  #Time in s; What is the duration of a step going to be?
D = 15.         #Diffusion coefficient
totaltime = 100  #in seconds. How long should this simulation run? Total number of step = totaltime/steptime





''' Begin the simulation  '''
#Start the track with initial positions
def makeSimulation():
    position = 0
    time = 0
    print("Starting Simulation Now!")
    track.append([time,position])
    while time < totaltime:
        #increase time by one timestep
        time += steptime
        #create a spatial step
     
        '''Here the random number generator creates a step. 
        We can choose which type of distribution we want.'''
        #step = random.randint(-1,1)
        step = random.gauss(0,np.sqrt(2*D*steptime))
        #step = 0.1
     
        #append to stepsizes
        stepstaken.append(step)
        #add step to position
        position += step
        #add new position to track
        track.append([time,position])
    return

'''  Done with the simulation part  '''






'''  Analysis  '''
def makePlots():
    #prepare data to be plotted
    track = plot_track()
    stepdist = plot_step_size_distribution(3)  #Create the step size distribution for different lag times
    msdlen = 100 #how many steps should be considered for the MSD?
    msd = plot_MSD(msdlen) #Do the Mean Squared Displacement

    
    #Create three figures
    fig1, (ax1,ax2,ax3) = plt.subplots(1,3)
    #Read in the track data
    ax1.plot(track[0],track[1],'-b')
    #Configure the plot
    ax1.set_title("Track")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Position")
    #Read in the Step size distribution Data
    ax3.hist(stepdist,bins=20,range=None,histtype='bar',align='left',
             label=['lag time = {:}s'.format(1*steptime),
                    'lag time = {:}s'.format(2*steptime),
                    'lag time = {:}s'.format(3*steptime)])
    ax3.legend()
    #Configure Plot
    ax3.set_title("Step size distribution")
    ax3.set_xlabel("Stepsize")
    ax3.set_ylabel("Occurences")
    #Read in The MSD data
    ax2.errorbar(msd[0],msd[1],yerr=msd[2])
    ax2.plot(np.arange(msdlen)*steptime,2*D*np.arange(msdlen)*steptime,'r-')
    #Configure Plot
    ax2.set_title("Mean Squared Displacement")
    ax2.set_xlabel("Lag-Time [s]")
    ax2.set_ylabel("MSD")
    #Try to make plot look good. If this fails, please adjust manually
    try:
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.tight_layout()
    except:
        print("Please adjust window manually! Automated adjustment failed.")
    #Finally: Show the plot

       
    #Animate Diffusion:
    fig1 = plt.figure()
    im = plt.imshow(makeImage(track[1][0]), cmap=plt.get_cmap('Greys_r'), vmin=0, vmax=255,extent=[-50,50,-5,5])
    # function to update figure
    def updatefig(j):
        # set the data in the axesimage object
        im.set_array(makeImage(track[1][j]))
        # return the artists set
        return im,
    # kick off the animation
    ani = animation.FuncAnimation(fig1, updatefig, frames=range(len(track[1])), interval=steptime*1000, blit=True, repeat=False)
    plt.xlabel("Position")
    plt.show()
    return
'''Done Analysis'''





''' Analysis Helper Functions '''
#Track
def plot_track():
    #get numpy to help with the track array
    tr = np.array(track)
    #transpose track, so time and position is more accessible
    transposed = tr.transpose()
    #Plot the track: Time vs Position
    return transposed

#Stepsize Distribution   
def plot_step_size_distribution(lag):
    #We already have stepstaken for lagtime = 1*steptime
    #We can look at lagtime = lag * time
    stepsmultilag = []
    if lag > 1:
        for i in xrange(lag):
            stepsmultilag.append([])
    stepsmultilag[0] = list(stepstaken)
    for i in xrange(len(stepstaken)):
        for j in xrange(len(stepsmultilag)):
            #ignore original steps
            if j == 0:
                continue
            #make sure element in list exists
            elif i < j:
                continue
            else:
                sum = 0
                for k in xrange(i-j,i+1):
                    sum += stepstaken[k]
                stepsmultilag[j].append(sum)
    #Plot histogram
    return stepsmultilag

#Mean squared displacement
def plot_MSD(maxsteps):
    #Calculate the mean squared displacement
    msd = []
    #make sure input makes sense
    if maxsteps > len(track):
        maxsteps = len(track)
    #Calculate msd for each time point
    for i in xrange(maxsteps):
        summed = 0
        count = 0
        for j in xrange(i,len(track)):
            summed += (track[j][1]-track[j-i][1])**2
            count += 1
        mean = summed * 1.0/count
        error = 0
        for j in xrange(i,len(track)):
            error += (mean - (track[j][1]-track[j-i][1])**2)**2
        msd.append([i*steptime,mean,np.sqrt(error/(count*(count-1)))])
    #Plot the MSD:
    msd = np.array(msd)
    msdtransposed = msd.transpose()
    return msdtransposed


#Create Images for the simulation video
def makeImage(position):
    def gauss(i,j,posx,posy,intensity,sig):
        return math.exp(-(((i)-posx)**2+((j)-posy)**2)/(2.0*sig))*intensity
    posx= 50
    posy = round(position*10) + 500
    data = np.zeros((101,1000))
    border = 40
    px = int(posx)
    py = int(posy)
    for i in xrange(max(0,px-border),min(len(data)-1,px+border),1):
        for j in xrange(max(0,py-border),min(len(data[i]-1),py+border),1):
            msig = gauss(i,j,px,py,255,50)
            if msig >= 2**8:
                msig = 2**8-1
            elif msig < 0:
                msig = 0
            data[i][j] = msig
    return data


#Script itself:
if __name__=="__main__":
    makeSimulation()
    makePlots()
    raw_input("Press Enter to Exit.")
    
