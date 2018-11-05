from scipy.signal import convolve2d
import numpy as np
import matplotlib.pyplot as plt
from random import randint
# 3 Storage channels:
# Grid
# Ships Container
# Hit Grid
class Ships:

    def __init__(self,grid):
        grid = np.array(grid)
        y,x = grid.shape
        self.grid = np.zeros([y,x])
        self.ships = []
        self.omap = np.where(grid ==0 ,1,0)
        
    def rand_ship(self,l):
        n = 0
        my, mx = self.omap.shape 
        mx -= 1
        my -= 1
        
        x = randint(0,mx)
        y = randint(0,my)
        o = randint(0,1)
        while not self.add_ship(x,y,l,o):
            n += 1
            x = randint(0,mx)
            y = randint(0,my)
            o = randint(0,1)
            if n > 100:
                print("error")
                break
    def add_ship(self,x,y,l,isVertical = True,verbose = False):
        nship = {}
        nship["idx"] = len(self.ships) + 1
        #map + grid = the combined map to check for collisions
        combi =self.omap + self.grid
        isCollide = False
        yn = y
        xn = x
        print(x,",",y)
        try:
            for i in range(l):
                if combi[xn][yn] != 0:
                    isCollide = True
                    break
                if isVertical:
                    yn += 1
                else:
                    xn += 1
        except:
            return False
        #if everything is fine then add to data
        if not isCollide:
            nship["l"] = l
            nship["sunk"] = False
            #populate ship grid
            for i in range(l):
                self.grid[y][x] = nship["idx"]
                if isVertical:
                    y += 1
                else:
                    x += 1
            x
            self.ships.append(nship)
            return True
        else:
            if verbose:
                print("Could Not add ship due to collision")
            return False

    def get_mask(self):
        #Generator function to return a dynamic mask
        return [i.l for i in self.ships if not i.sunk]

    def checkHit(self,x,y,testonly=False):
        if self.grid[y][x] != 0:
            #Its a hit.
            if not testonly:
                self.grid[y][x] = 0
                self.updateShipfromgrid()
            return True
        else:
            return False
            
    def updateShipfromgrid(self):
        for i in self.ships:
            if i.sunk:
                continue
            if np.sum(np.where(self.grid == i.l,1,0)) == 0:
                i.sunk = True

    def get_map(self):
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


def Checkhit(x,y,gmap,ghit):
    # if the ship exists
    if Lships.checkHit(x,y):
        ghit[y][x] = 1
        
    



def visGrid(grid):
    plt.figure()
    plt.imshow(grid,cmap='gray')
    plt.grid(True,color='blue')
    plt.draw()
    
#def hitgrid(activehit,)
grid = [[0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1]]

Lships = Ships(grid)
Lships.rand_ship(1)
visGrid(Lships.get_map())
print(len(Lships.ships))
visGrid(grid)
plt.show()