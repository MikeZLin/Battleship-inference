from scipy.signal import convolve2d
import numpy as np
import matplotlib.pyplot as plt
# 3 Storage channels:
# Grid
# Ships
# Hit/Miss/Sunk, encoded -> hit = 1, miss = -1, sunk = (ship Length)
class ships:

    def __init__(self,grid):
        y,x = grid.shape
        self.grid = np.zeros([y,x])
        self.ships = []
        self.omap = grid
        


    def add_ship(self,x,y,l,isVertical = True):
        nship = {}
        nship.idx = len(self.ships) + 1
        #map + grid = the combined map to check for collisions
        combi = self.omap + self.grid
        isCollide = False
        yn = y
        xn = x
        for i in range(l):
            if combi[yn][xn] != 0:
                isCollide = True
                break
            if isVertical:
                yn += 1
            else:
                xn += 1

        #if everything is fine then add to data
        if not isCollide:
            nship.l = l
            nship.sunk = False
            #populate ship grid
            for i in range(l):
                self.grid[y][x] = nship.idx
                if isVertical:
                    y += 1
                else:
                    x += 1
            self.ships.append(nship)

        else:
            print("Could Not add ship due to collision")


        
    def get_map():
        return self.grid


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

def proc_Hitgrid(gmap,gHit,gmask,hitweight = 5):
    gmap = np.array(gmap)
    gHit = np.array(gHit)
    mask = np.array(np.ones([gmask,1]))

    #overlay the hit mask with the grid mask
    grid = gmap + (gHit * hitweight)

    #vertical and horizontal
    res = np.where(convolve2d(grid,mask,"full") == np.sum(mask),1,0)
    res = res[(mask.shape[0] - 1):,(mask.shape[1] - 1):]
    mask2 = np.transpose(mask)
    res2 = np.where(convolve2d(grid,mask2,"full") == np.sum(mask2),1,0)
    res2 = res2[(mask2.shape[0] - 1):,(mask2.shape[1] - 1):]

    final = res + res2

    #remove the original Hitmask
    remHit = np.where(np.array(gHit) == 1,0,1)
    
    
    return np.multiply(remHit, final)


def Checkhit(x,y,gmap,ghit,ships,gship):
    # if the ship exists
    if gship[y][x] != 0:
        ghit[y][x] = 1
        
    
    pass
    



def visGrid(grid):
    plt.figure()
    plt.imshow(grid,cmap='gray')
    plt.grid(True,color='blue')
    plt.draw()
    

#def hitgrid(activehit,)
grid = [[0, 1, 0, 0],
        [1, 1, 1, 1], 
        [1, 1, 1, 1], 
        [1, 0, 1, 1]]
res = sum([positional_grid(grid,i) for i in range(2,6)])
visGrid(res)


plt.show()
