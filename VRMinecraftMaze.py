import random
import time
import math
import mcpi.minecraft as minecraft
import mcpi.block as block
mc = minecraft.Minecraft.create()

#create blank maze
maze=[]

def rngWalls(xRand,yRand):
    grrr=2**31-1
    xRand=(14389*xRand*grrr+2342051)%(grrr)
    xRand = xRand/(grrr)
    yRand=(234125161*yRand*grrr+9880027)%(grrr)
    yRand = yRand/(grrr)
    return xRand,yRand

def MoveDirection(sx,sy,x,y):  #checks where to dig next
    move=[]
    # up = 0, right = 1, down = 2, left = 3
    #check up
    if not y <=1:
        if maze[y-2][x]==0:
            move.append(0)
    #check right
    if not x >= sx-2:
        if maze[y][x+2]==0:
            move.append(1)
    #check down
    if not y >= sy-2:
        if maze[y+2][x]==0:
            move.append(2)
    #check left
    if not x <= 1:
        if maze[y][x-2]==0:
            move.append(3)
    if len(move)>0:
        randMove=int(len(move)*random.random())%len(move) #note: len(move)=/=0
        randMove=move[randMove]
    else:
        randMove=-1
    return [len(move),randMove]

def BridgeCheck(sx,sy,x,y):
    # up = 0, right = 1, down = 2, left = 3
    bridge=-1
    #check up
    if not y < 1:
        if maze[y-1][x]==1:
            bridge=0
    #check right
    if not x > sx-2:
        if maze[y][x+1]==1:
            bridge=1
    #check down
    if not y > sy-2:
        if maze[y+1][x]==1:
            bridge=2
    #check left
    if not x < 1:
        if maze[y][x-1]==1:
            bridge=3
    return bridge

# get dimensions of maze (not including walls)
width = input("Width? ")
height = input("Height? ")

w = int(width)
h = int(height)
    
for i in range(h*2+1):
    row = []
    for j in range((w*2+1)):
        row.append(0)
    maze.append(row)

startx=w-3+w%2
starty=h-3+h%2

w=w*2+1
h=h*2+1

for i in range(5):
    for j in range(w):
        if j<startx-2 or j>=startx+7:
            maze[i+starty][j]=9
        
for i in range(h):
    for j in range(5):
        if i<starty-2 or i>=starty+7:
            maze[i][j+startx]=9
        
for i in range(5):
    for j in range(5):
        maze[i+starty][j+startx]=3
        
#set lever positions in each corner of the maze in the matrix
maze[1][1]=5
maze[2][1]=6
maze[h-3][1]=6
maze[h-2][1]=5
maze[1][w-2]=5
maze[2][w-2]=6
maze[h-3][w-2]=6
maze[h-2][w-2]=5
        
maze[starty][startx]=3
startx=startx+2

digx = startx
digy = starty

#exitList=[]

complete = 0
oof = 0
while complete < 1 :
    randDirect=MoveDirection(w,h,digx,digy)
    if randDirect[1]==-1: #or randDirect[0]==0
        #move backwards and try again
        BridgeDirect=BridgeCheck(w,h,digx,digy)
        #insert exit code
        #Find direction to move backwards and mark trail
        #bridge values: up = 0, right = 1, down = 2, left = 3
        if BridgeDirect == 0 or BridgeDirect == 2:
            if maze[digy+1][digx]+ maze[digy-1][digx]+ maze[digy][digx-1]+ maze[digy][digx+1]==1:
                maze[digy][digx]=4
                #exitList.append([digy,digx])
            else:
                maze[digy][digx]=2
            maze[digy+(BridgeDirect-1)][digx]=2
            digy=digy+2*(BridgeDirect-1)
        elif BridgeDirect == 1 or BridgeDirect == 3:
            if maze[digy+1][digx]+ maze[digy-1][digx]+ maze[digy][digx-1]+ maze[digy][digx+1]==1:
                maze[digy][digx]=4
                #exitList.append([digy,digx])
            else:
                maze[digy][digx]=2
            maze[digy][digx-(BridgeDirect-2)]=2
            digx=digx-2*(BridgeDirect-2)
        else:
            #you are at the start of the maze and have completed the maze
            complete = 1
    else:
        #direction values: up = 0, right = 1, down = 2, left = 3
        if randDirect[1]==0 or randDirect[1]==2:
            maze[digy+(randDirect[1]-1)][digx]=1
            maze[digy+(2*(randDirect[1]-1))][digx]=1
            digy=digy+(2*(randDirect[1]-1))
        else:
            maze[digy][digx-(randDirect[1]-2)]=1
            maze[digy][digx-(2*(randDirect[1]-2))]=1
            digx=digx-(2*(randDirect[1]-2))

breakwalls = int(int(width)*int(height)/10)
#print(breakwalls)
broken=0
xrandom=random.random()
yrandom=random.random()
#print(xrandom,yrandom)
while broken < breakwalls:
    bw=int(1+(w-2)*xrandom) #LOWER_BOUNDRY + UPPER_BOUNDRY*RAND()
    bh=int(1+(h-2)*yrandom) #LOWER_BOUNDRY + UPPER_BOUNDRY*RAND()
    xrandom,yrandom=rngWalls(xrandom,yrandom)
    #print(xrandom,yrandom)
    #print(bw,bh)
    if maze[bh][bw]== 0 and bh!=0 and bw!=0 and bh!=w and bh!=h:
        if not(maze[bh-1][bw]==3 or maze[bh][bw-1]==3 or maze[bh+1][bw]==3 or maze[bh][bw+1]==3) or maze[h-3][w-3]:
            maze[bh][bw] = 2
            broken=broken+1
            #eliminate any dead ends
            if maze[bh-1][bw]== 4:
                maze[bh-1][bw] = 2
            if maze[bh][bw-1]== 4:
                maze[bh][bw-1] = 2
            if maze[bh+1][bw]== 4:
                maze[bh+1][bw] = 2
            if maze[bh][bw+1]== 4:
                maze[bh][bw+1] = 2

for i in range(h):
    print(maze[i])

maze[h-3][w-3]=0 #prevents water from destroying lever
#declare blocks
#GAP = 0 #block.AIR.id

noooooo=input("type a number i guess")

stonebrick = 98
slab = 44#[5]
sealantern=169

lava=10
netherbrick=112

sand=12
sandstone=24
torch=50

glass=95 #black is [15]
barrier = 166
bookshelf = 47
#lamp = 124
glowstone = 89
#redstoneblock = 152
fence = 191

water = 8
prismarine = 168 #dark [2]


lever = 69
redstone=55
redtorch=76
gold = 41

pos = mc.player.getTilePos()
xx = pos.x
yy = pos.y
zz = pos.z

xx=xx-3*startx
zz=zz-3*starty-6

lavaheight=1
counter = 0

for i in range(h):
    for j in range(w):
        if counter > 200:
            report=int(i/h*100)
            print("Percent complete: ",report)
            time.sleep(4)
            counter=0
        counter=counter+1
        if i==0 or i==h-1 or j==0 or j==w-1 or maze[i][j]==9:
            mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+3,zz+1+3*i,stonebrick)
        elif i<starty: #top half
            if j<startx-2: #top-left lava <------------------------------------------------
                if maze[i][j]==0:
                    mc.setBlock(xx+3*j,yy+lavaheight+1,zz+3*i,lava)
                    lavaheight=(lavaheight+1)%3
                    mc.setBlocks(xx-1+3*j,yy-1,zz-1+3*i,xx+1+3*j,yy-1,zz+1+3*i,0)
                    mc.setBlocks(xx-1+3*j,yy+4,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,netherbrick) #ceiling
                elif maze[i][j]==5:#redstone behind switch
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,gold)
                    mc.setBlock(xx+3*j,yy+2,zz+3*i,redtorch,4)
                    mc.setBlock(xx+3*j,yy+3,zz-1+3*i,redtorch,4)
                    mc.setBlock(xx+3*j,yy+4,zz+3*i,redtorch,3)
                    mc.setBlock(xx+3*j,yy+5,zz+1+3*i,redtorch,3)
                elif maze[i][j]==6:
                    mc.setBlock(xx+3*j,yy+2,zz-1+3*i,lever,3)
                #insert stuff for switch and redstone
                else:
                    mc.setBlocks(xx-1+3*j,yy-1,zz-1+3*i,xx+1+3*j,yy-1,zz+1+3*i,netherbrick) #floor
                    mc.setBlocks(xx-1+3*j,yy+4,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,netherbrick) #ceiling
            elif j>startx+2: #top-right sand <--------------------------------------------------
                if maze[i][j]==2 or maze[i][j]==4:
                    mc.setBlocks(xx-1+3*j,yy-1,zz-1+3*i,xx+1+3*j,yy-1,zz+1+3*i,sand)#floor
                    if i%2!=0:
                        if j%2==0:
                            mc.setBlock(xx-1+3*j,yy,zz-1+3*i,sand)
                            mc.setBlock(xx-1+3*j,yy,zz+3*i,sand)
                            mc.setBlock(xx+3*j,yy,zz+3*i,sand)
                            mc.setBlock(xx+3*j,yy,zz-1+3*i,sand)
                            mc.setBlock(xx+3*j,yy+1,zz-1+3*i,sand)
                            mc.setBlock(xx+1+3*j,yy,zz+3*i,sand)
                            mc.setBlock(xx+1+3*j,yy,zz+1+3*i,sand)
                        else:
                            mc.setBlock(xx+3*j,yy,zz-1+3*i,sand)
                            mc.setBlock(xx+3*j,yy,zz+3*i,sand)
                            mc.setBlock(xx+3*j,yy+1,zz+3*i,sand)
                            mc.setBlock(xx+1+3*j,yy,zz-1+3*i,sand)
                            mc.setBlock(xx+3*j,yy,zz+3*i,sand)
                            mc.setBlock(xx-1+3*j,yy,zz+3*i,sand)
                            mc.setBlock(xx-1+3*j,yy,zz+1+3*i,sand)
                    else:
                        mc.setBlock(xx+1+3*j,yy,zz-1+3*i,sand)
                        mc.setBlock(xx+1+3*j,yy,zz+3*i,sand)
                        mc.setBlock(xx+1+3*j,yy+1,zz+3*i,sand)
                        mc.setBlock(xx-1+3*j,yy,zz-1+3*i,sand)
                        mc.setBlock(xx-1+3*j,yy+1,zz-1+3*i,sand)
                        mc.setBlock(xx+3*j,yy,zz+3*i,sand)
                        mc.setBlock(xx+3*j,yy,zz+1+3*i,sand)
                elif maze[i][j]==0:
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,sandstone)
                    mc.setBlock(xx-1+3*j,yy+3,zz+3*i,torch)
                    mc.setBlock(xx+1+3*j,yy+3,zz+3*i,torch)
                    mc.setBlock(xx+3*j,yy+3,zz-1+3*i,torch)
                    mc.setBlock(xx+3*j,yy+3,zz+1+3*i,torch)
                elif maze[i][j]==5:#redstone behind switch
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,gold)
                    mc.setBlock(xx+3*j,yy+2,zz+3*i,redtorch,4)
                    mc.setBlock(xx+3*j,yy+3,zz-1+3*i,redtorch,4)
                    mc.setBlock(xx+3*j,yy+4,zz+3*i,redtorch,3)
                    mc.setBlock(xx+3*j,yy+5,zz+1+3*i,redtorch,3)
                elif maze[i][j]==6:
                    mc.setBlock(xx+3*j,yy+2,zz-1+3*i,lever,3)
        elif i>starty+4: #bottom half
            if j<startx-2: #bottem-left invisible <-------------------------------------------
                mc.setBlocks(xx-1+3*j,yy-1,zz-1+3*i,xx+1+3*j,yy-1,zz+1+3*i,glass,15)#floor
                mc.setBlocks(xx-1+3*j,yy-6,zz-1+3*i,xx+1+3*j,yy-6,zz+1+3*i,stonebrick)#floor
                mc.setBlocks(xx-1+3*j,yy-2,zz-1+3*i,xx+1+3*j,yy-5,zz+1+3*i,0)
                if maze[i][j]==2:
                    mc.setBlock(xx+3*j,yy-6,zz+3*i,glowstone)
                    mc.setBlock(xx+3*j,yy+4,zz+3*i,glowstone)
                    #mc.setBlock(xx+3*j,yy-7,zz+3*i,redstoneblock)
                    #mc.setBlock(xx+3*j,yy+5,zz+3*i,redstoneblock)
                elif maze[i][j]==0:
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+3,zz+1+3*i,barrier)#wall
                    mc.setBlocks(xx-1+3*j,yy-5,zz-1+3*i,xx+1+3*j,yy-5,zz+1+3*i,slab,5)
                elif maze[i][j]==5:#redstone behind switch
                    mc.setBlocks(xx-1+3*j,yy-5,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,gold)
                    mc.setBlock(xx+3*j,yy+2,zz+3*i,redtorch,3)
                    mc.setBlock(xx+3*j,yy+3,zz+1+3*i,redtorch,3)
                    mc.setBlock(xx+3*j,yy+4,zz+3*i,redtorch,4)
                    mc.setBlock(xx+3*j,yy+5,zz-1+3*i,redtorch,4)
                elif maze[i][j]==6:
                    mc.setBlock(xx+3*j,yy+2,zz+1+3*i,lever,4)
                    mc.setBlock(xx+3*j,yy-4,zz+1+3*i,lever,4)
                if i%2==0 and j%2==0:
                    mc.setBlocks(xx+3*j,yy-5,zz+3*i,xx+3*j,yy+5,zz+3*i,48)#moss
            elif j>startx+2: #bottom-right water <---------------------------------------------------
                mc.setBlocks(xx-1+3*j,yy+4,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,prismarine,2)
                if maze[i][j]==0:
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,prismarine)
                    mc.setBlock(xx-1+3*j,yy+2,zz+3*i,sealantern)
                    mc.setBlock(xx+1+3*j,yy+2,zz+3*i,sealantern)
                    mc.setBlock(xx+3*j,yy+2,zz-1+3*i,sealantern)
                    mc.setBlock(xx+3*j,yy+2,zz+1+3*i,sealantern)
                elif maze[i][j]==5:#redstone behind switch
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+4,zz+1+3*i,gold)
                    mc.setBlock(xx+3*j,yy+2,zz+3*i,redtorch,3)
                    mc.setBlock(xx+3*j,yy+3,zz+1+3*i,redtorch,3)
                    mc.setBlock(xx+3*j,yy+4,zz+3*i,redtorch,4)
                    mc.setBlock(xx+3*j,yy+5,zz-1+3*i,redtorch,4)
                elif maze[i][j]==6:
                    #mc.setBlocks(xx-1+3*j,yy+1,zz-1+3*i,xx+1+3*j,yy+3,zz+1+3*i,0)
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy,zz+1+3*i,prismarine,2)#high floor
                    mc.setBlock(xx+3*j,yy+2,zz+1+3*i,lever,4)     #lever,4)
                elif maze[i][j]==2 or maze[i][j]==4:
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+2,zz+1+3*i,water)
                if i==h-4 and j==w-2:
                    mc.setBlocks(xx-1+3*j,yy,zz-1+3*i,xx+1+3*j,yy+3,zz+1+3*i,0)
print("redstone time")
for i in range(2,int(h/2)):#top
        mc.setBlock(xx+3*1,yy+5,zz-1+3*i,redstone)
        mc.setBlock(xx+3*1,yy+5,zz+3*i,gold)
        mc.setBlock(xx+3*1,yy+5,zz+1+3*i,redtorch,3)
        mc.setBlock(xx+3*(w-2),yy+5,zz-1+3*i,redstone)
        mc.setBlock(xx+3*(w-2),yy+5,zz+3*i,gold)
        mc.setBlock(xx+3*(w-2),yy+5,zz+1+3*i,redtorch,3)
for i in range(h-3,int(h/2),-1):#bottom
        mc.setBlock(xx+3*1,yy+5,zz-1+3*i,redtorch,4)
        mc.setBlock(xx+3*1,yy+5,zz+3*i,gold)
        mc.setBlock(xx+3*1,yy+5,zz+1+3*i,redstone)
        mc.setBlock(xx+3*(w-2),yy+5,zz-1+3*i,redtorch,4)
        mc.setBlock(xx+3*(w-2),yy+5,zz+3*i,gold)
        mc.setBlock(xx+3*(w-2),yy+5,zz+1+3*i,redstone)
#middle stuff (left side)
mc.setBlock(xx+3*1,yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx+3*1,yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx+3*1,yy+5,zz+1+3*(int(h/2)),redstone)
mc.setBlock(xx+1+3*1,yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx+1+3*1,yy+5,zz+1+3*(int(h/2)),redstone)
mc.setBlock(xx+2+3*1,yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx+2+3*1,yy+5,zz+1+3*(int(h/2)),redstone)
mc.setBlock(xx+3+3*1,yy+5,zz-1+3*(int(h/2)),gold)
mc.setBlock(xx+3+3*1,yy+5,zz+1+3*(int(h/2)),gold)
mc.setBlock(xx+4+3*1,yy+5,zz-1+3*(int(h/2)),redtorch,1)
mc.setBlock(xx+4+3*1,yy+5,zz+1+3*(int(h/2)),redtorch,1)
mc.setBlock(xx+4+3*1,yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx+5+3*1,yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx+6+3*1,yy+5,zz+3*(int(h/2)),redstone)
#middle stuff (right side)
mc.setBlock(xx+3*(w-2),yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx+3*(w-2),yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx+3*(w-2),yy+5,zz+1+3*(int(h/2)),redstone)
mc.setBlock(xx-1+3*(w-2),yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx-1+3*(w-2),yy+5,zz+1+3*(int(h/2)),redstone)
mc.setBlock(xx-2+3*(w-2),yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx-2+3*(w-2),yy+5,zz+1+3*(int(h/2)),redstone)
mc.setBlock(xx-3+3*(w-2),yy+5,zz-1+3*(int(h/2)),gold)
mc.setBlock(xx-3+3*(w-2),yy+5,zz+1+3*(int(h/2)),gold)
mc.setBlock(xx-4+3*(w-2),yy+5,zz-1+3*(int(h/2)),redtorch,2)
mc.setBlock(xx-4+3*(w-2),yy+5,zz+1+3*(int(h/2)),redtorch,2)
mc.setBlock(xx-4+3*(w-2),yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx-5+3*(w-2),yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx-6+3*(w-2),yy+5,zz+3*(int(h/2)),redstone)
#connect the two in the very middle
for j in range(3,w-3):
    if j<int(w/2):
        mc.setBlock(xx-1+3*j,yy+5,zz+3*(int(h/2)),redstone)
        mc.setBlock(xx+3*j,yy+5,zz+3*(int(h/2)),gold)
        mc.setBlock(xx+1+3*j,yy+5,zz+3*(int(h/2)),redtorch,1)
    elif j>int(w/2):
        mc.setBlock(xx+1+3*j,yy+5,zz+3*(int(h/2)),redstone)
        mc.setBlock(xx+3*j,yy+5,zz+3*(int(h/2)),gold)
        mc.setBlock(xx-1+3*j,yy+5,zz+3*(int(h/2)),redtorch,2)

#exit
mc.setBlock(xx-1+3*(int(w/2)),yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx+1+3*(int(w/2)),yy+5,zz+3*(int(h/2)),redstone)
mc.setBlock(xx-1+3*(int(w/2)),yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx+1+3*(int(w/2)),yy+5,zz-1+3*(int(h/2)),redstone)
mc.setBlock(xx-1+3*(int(w/2)),yy+5,zz-2+3*(int(h/2)),gold)
mc.setBlock(xx+1+3*(int(w/2)),yy+5,zz-2+3*(int(h/2)),gold)
mc.setBlock(xx-1+3*(int(w/2)),yy+5,zz-3+3*(int(h/2)),redtorch,4)
mc.setBlock(xx+1+3*(int(w/2)),yy+5,zz-3+3*(int(h/2)),redtorch,4)
mc.setBlock(xx+3*(int(w/2)),yy+5,zz-3+3*(int(h/2)),redstone)
mc.setBlock(xx+3*(int(w/2)),yy+5,zz-4+3*(int(h/2)),redstone)
mc.setBlock(xx+3*(int(w/2)),yy+5,zz-6+3*(int(h/2)),0)
mc.setBlock(xx+3*(int(w/2)),yy+5,zz-5+3*(int(h/2)),29,2)
mc.setBlock(xx+3*(int(w/2)),yy+4,zz-7+3*(int(h/2)),0)
mc.setBlock(xx+3*(int(w/2)),yy+6,zz-7+3*(int(h/2)),0)
mc.setBlock(xx+3*(int(w/2)),yy+7,zz-7+3*(int(h/2)),water)
mc.setBlock(xx+1+3*(int(w/2)),yy,zz-7+3*(int(h/2)),120)
mc.setBlock(xx+3*(int(w/2)),yy,zz+1-7+3*(int(h/2)),120)
mc.setBlock(xx+3*(int(w/2)),yy,zz-1-7+3*(int(h/2)),120)
mc.setBlock(xx-1+3*(int(w/2)),yy,zz-7+3*(int(h/2)),120)
#light at start
for i in range(-7,8):
    for j in range(-7,8):
        if 6<=math.sqrt(i**2+j**2)<=9:
            mc.setBlock(pos.x+i,yy-1,pos.z+j,glowstone)

mc.setBlocks(xx+3*(startx+2),yy,zz+3*(starty+4),xx+3*(startx+2),yy,zz+3*(starty+4)+7,prismarine)
mc.setBlocks(xx+3*(startx+2),yy,zz+3*(starty+4),xx+3*(startx+2)+7,yy,zz+3*(starty+4),prismarine)
