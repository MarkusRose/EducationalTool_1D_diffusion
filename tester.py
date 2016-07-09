import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

   
hmpf = np.ones([4,4])
print hmpf
hmpf[2][1] = 0
imagelist = [ hmpf*i*255./19. for i in range(20) ]

fig = plt.figure()
im = plt.imshow(imagelist[0], cmap=plt.get_cmap('jet'), vmin=0, vmax=255)
# function to update figure
def updatefig(j):
    # set the data in the axesimage object
    im.set_array(imagelist[j])
    # return the artists set
    return im,
# kick off the animation
ani = animation.FuncAnimation(fig, updatefig, frames=range(20), 
                              interval=500, blit=True)
plt.show()
