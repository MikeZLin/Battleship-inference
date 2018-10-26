from scipy.signal import convolve2d
import numpy as np
import matplotlib.pyplot as plt
# 3 Storage channels:
# Grid
# Ships
# Hit/Miss/Sunk, encoded -> hit = 1, miss = -1, sunk = (ship Length)


def positional_grid(gmap,gmask):
    mask = np.ones([gmask,1])
    grid = np.array(gmap)
    mask = np.array(mask)
    res = np.where(convolve2d(grid,mask,"full") == np.sum(mask),1,0)
    res = res[(mask.shape[0] - 1):,(mask.shape[1] - 1):]
    mask2 = np.transpose(mask)
    res2 = np.where(convolve2d(grid,mask2,"full") == np.sum(mask2),1,0)
    res2 = res2[(mask2.shape[0] - 1):,(mask2.shape[1] - 1):]
    return res + res2

def proc_Hitgrid(gmap,gHit,gmask,hitWeight):
    gmap = np.array(gmap)
    gHit = np.where(np.array(gHit) == 1,hitWeight,0)
    gMiss = np.where(np.array(gHit) == -1,hitWeight,0)
    gsunk = np.where(np.array(gHit) == -1,hitWeight,0)
    


    # Hit mask conv by mask


def visGrid(grid):
    plt.figure()
    plt.imshow(grid,cmap='gray')
    plt.grid(True,color='blue')
    plt.draw()
    

#def hitgrid(activehit,)
grid = [[0, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1], [1, 0, 1, 1]]
res = sum([positional_grid(grid,i) for i in range(2,6)])
visGrid(grid)


plt.show()
