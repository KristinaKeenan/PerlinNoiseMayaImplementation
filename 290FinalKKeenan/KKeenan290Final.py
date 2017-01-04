import maya.cmds
import random

from random import shuffle

class Perlin():
    def __init__(self,x,y):


#permutation table that 
        self.p = [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
    88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
    77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
    102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
    135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
    5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
    223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
    129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
    251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
    49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

        #x and y of point you're working with
        self.x = x
        self.y = y

        #situates point within a unit cube
        self.xi = self.x & 255
        self.yi = self.y & 255

        #creates fade values
        self.xf = self.x-self.x
        self.yf = self.y-self.y

        
    #returns gradient vector based on unit cube
    def gradient(self,h,x,y):
        hashedValue = h & 15
        u = x if h < 8 else y

        if(h < 4):
            v = y
        else:
            v = x

        return (u if (h&1) == 0 else (7*u)/8)+(v if (h&2) == 0 else (7*v)/8)


    #fade function
    def fade(self,t):
        return t * t * t * (t * (t * 6 - 15) + 10)


    #generates gradient based on hashed values and 
    def genGradients(self):
        self.gradient1 = self.gradient(self.aa,self.x,self.y)
        self.gradient2 = self.gradient(self.ba,self.x-1,self.y)
        self.gradient3 = self.gradient(self.ab,self.x,self.y-1)
        self.gradient4 = self.gradient(self.bb,self.x-1,self.y-1)

    #interpolates dot products to find influence value    
    def pointInterpolation(self):

        self.u = self.fade(self.xf)
        self. v = self.fade(self.yf)

        
        x1 = self.lerp(self.gradient1,self.gradient2,self.u)
        x2 = self.lerp(self.gradient3,self.gradient4,self.u)

        self.lerpValue = (self.lerp(x1,x2,self.v))

        return self.lerpValue

        

    #interpolates values with fade values
    def lerp(self,val1,val2,fadeVal):
        return val1+fadeVal*(val2-val1)
        

    #hashes all four edge points, comes up with an integer value between 0 and 255
    def hashFunction(self):
        self.aa = self.p[self.p[self.xi]+self.yi]
        self.ab = self.p[self.p[self.xi]+(self.yi+1)]
        self.bb = self.p[self.p[(self.xi + 1)]+ (self.yi)]
        self.ba = self.p[self.p[(self.xi+1)]+(self.yi+1)]



    #returns interpolated values
    def getLerpValue(self):
        return self.lerpValue
               
#draws the blocks
def drawBlocks(height,width,pointList,textureList,maximum):
    #sets all blocks that are to be filled to equal 1
    for i in range(height):
        for j in range(width):
            for k in range((int(pointList[i][j]/4 + 5))):
                textureList[k][i][j] = 1
    
    #draws all blocks that are to be filled, determines texture based on Perlin value
    for k in range(maximum):
        for i in range(height):
            for j in range(width):
                if(textureList[k][i][j] == 1):
                    if((int(pointList[i][j]/4 + 5))<=6):
                        cube = "water"
                    elif((int(pointList[i][j]/4 + 5))>6 and (int(pointList[i][j]/4 + 5))<=8):
                        cube = "sand"
                    elif((int(pointList[i][j]/4 + 5))>8 and (int(pointList[i][j]/4 + 5))<=10):
                        randNum = random.randrange(1,10)
                        
                        if(randNum <= 7 or textureList[k+1][i][j]==0):
                        
                            cube = "stone"
                        else:
                            randNum = random.randrange(1,4)
                            if(randNum == 1):
                                cube = "emerald"
                            elif(randNum == 2):
                                cube = "tin"
                            elif(randNum == 3):
                                cube = "gold"
                            else:
                                cube = "diamond"
                    else:
                        if(k == maximum - 1):
                           cube = "grass"

                        else: 
                            if(textureList[k+1][i][j]==0):
                                cube = "grass"

                            else:
                                cube = "dirt"
                    cmds.select(cube)
                    cmds.duplicate(cube)
                    cmds.move((10-i),10-k,10+j)
                    

def main():
    #dimensions of the base of the scene
    height = 30
    width = 15

    #creates 2D array for the points
    pointList = [[0 for x in range(width)] for y in range(height)]

    
    maximum = 0

    #calls the Perlin functions for every point in the base
    for i in range(height):
        for j in range(width):
            #creates Perlin object
            perlinNoise = Perlin(i,j)
            #hashes values
            perlinNoise.hashFunction()
            #generates gradients
            perlinNoise.genGradients()
            #interpolates points 
            pointList[i][j] = perlinNoise.pointInterpolation()
            #adds blocks to bottom of influence values to create chunk
            if(int((pointList[i][j]/4)+5)>maximum):
                maximum = int((pointList[i][j]/4)+5)

    #creates 3D array that handles block placement
    textureList = [[[0 for x in range(width)] for y in range(height)] for z in range(maximum)]

    #initializes all blocks to be empty
    for k in range(maximum):
        for i in range(height):
            for j in range(width):
                textureList[k][i][j] = 0
   

    #calls function that draws the blocks
    drawBlocks(height,width,pointList,textureList,maximum)

main()

