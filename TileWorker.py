import maya.mel as mel
import maya.cmds as cmds
import random
import math

from Vec3 import Vec3
from Polygon import Polygon
from Tile import Tile

class TileInfo:
    length = 3.2 # maya
    width = 2.4  # from AI
    height = 0.8 # from AI
class Roof(Polygon):
    Vertexs = []
    outOffset = 0
    def __init__(self):
        Polygon.__init__(self)
        self.Name = "roof"
        positions = self.GetVertexsPos()
        positions.sort(key = lambda v:v.x)
        positions = positions[:len(positions) / 2]
        positions.sort(key = lambda v:v.z,reverse = True)
        self.Vertexs = positions
        # vertexs.sort(key = lambda v:(v.x,v.z))
        # for i in range(len(self.Vertexs)):
        #     print i, self.Vertexs[i].ToString()

    # not finished
    def get_direction(self, points):
        positions.sort(key = lambda v:v.y)

    def GetNearestVertex(self, pos):
        # out of the roof top
        topVertex = self.Vertexs[len(self.Vertexs) - 1]
        if (topVertex.z > pos.z or topVertex.DistanceYZ(pos) < TileInfo.length):
            ret = self.Vertexs[len(self.Vertexs) - 1].GetOneCopy()
            self.outOffset += TileInfo.length * 1.5
            ret.z -= self.outOffset
            return ret
        self.outOffset = 0
        distances = []
        for v in self.Vertexs:
            if v.z < pos.z:
                distances.append(pos.DistanceYZ(v))
            else:
                distances.append(TileInfo.length * 999) # this should be very max
            
            # print "pos=",pos.ToString(),"v=",v.ToString(),"d="
            # ,pos.DistanceYZ(v),"tile=",tile.length
        for i in range(len(distances)):
            distances[i] -= TileInfo.length
            if distances[i] < 0:
                distances[i] *= -1
        i = distances.index(min(distances))
        # print "distance i " ,i
        return self.Vertexs[i]

class TileWorker:
    roof = Roof()
    tileInfo = Tile()
    NumberOfTileY = 0
    NumberOfTileX  = 0
    currentTime = 0
    ExposeDistanceRange = [0,0]
    RotateYRange = [0,0]
    def __init__(self):
        pass

    def create_one_column_tiles(self,xn,offsetX):
        positions = []
        for i in range(self.NumberOfTileY):
            #tile = Tile()
            #tile.row = i + 1
            #tile.column = columnNum
            if (i == 0):
                contact = self.roof.Vertexs[0].GetOneCopy()
            else :
                contact = positions[i - 1].GetOneCopy()
                exposeDistance = random.uniform(self.ExposeDistanceRange[0],self.ExposeDistanceRange[1])
                contact.z += TileInfo.length - exposeDistance
            # print positions[i - 1].ToString()," contact ",contact.ToString()
            pos = self.roof.GetNearestVertex(contact).GetOneCopy()
            pos.x += (xn - 1) * offsetX
            positions.append(pos)
        for i,p in enumerate(positions):
            n = i + 1
            tile = Tile()
            rotateY = random.uniform(self.RotateYRange[0],self.RotateYRange[1])
            tile.Translate = p
            tile.Rotate = Vec3(0,rotateY,0)
            tile.Rename("tile{0}_{1}".format(xn,n))

    def CreateTiles(self):
        for i in range(self.NumberOfTileX):
        # for i in range(2):
            self.create_one_column_tiles(i + 1, TileInfo.width * 1.5)

    def CreatePassiveRigidBody(self, yNum):
        for i in range(self.NumberOfTileX):
            x = i + 1
            name = self.get_tile_name(x,yNum)
            mel.eval("select -r " + name)
            mel.eval("rigidBody -passive -m 1 -dp 0 -sf 1 -df 1 -b 0 -l 0 -tf 200 -iv 0 0 0 -iav 0 0 0 -c 0 -pc 0 -i 0 0 0 -imp 0 0 0 -si 0 0 0 -sio none")
    
    def CreateHingeConstrain(self, yNum):
        for i in range(self.NumberOfTileX):
            x = i + 1
            name = self.get_tile_name(x,yNum)
            mel.eval("connectDynamic - f gravityField1 " + name) 
            mel.eval("select -r " + name)
            mel.eval("constrain - hinge - o 0 90 0")
            move_z = 0.5 * TileInfo.length * -1 
            mel.eval("move - r 0 0 " + str(move_z))

    def RemoveAllRigidBody(self):
        names = mel.eval("ls -type rigidBody")
        for name in names:
            mel.eval("delete " + name)

    def SimulateTileFall(self):
        self.currentTime += 10
        mel.eval("currentTime " + str(self.currentTime))

    def Simulate(self):
        print "Simulate Begin"
        mel.eval("currentTime 1")
        mel.eval("gravity - pos 0 0 0 - m 9.8 - att 0 - dx 0 - dy - 1 - dz 0  - mxd - 1  - vsh none - vex 0 - vof 0 0 0 - vsw 360 - tsr 0.5")
        mel.eval('setAttr "gravityField1.magnitude" 100')
        for i in range(1,self.NumberOfTileY):
            self.CreatePassiveRigidBody(i)
            self.CreateHingeConstrain(i + 1)
            self.SimulateTileFall()
            self.RemoveAllRigidBody()
        mel.eval("delete gravityField1")

    def CreateBelowTile(self):
        for i in range(self.RowLen * self.ColumnLen):
            n = i + 1
            objectName = "tile" + str(n)
            x = cmds.getAttr(objectName + ".translateX")
            y = cmds.getAttr(objectName + ".translateY")
            z = cmds.getAttr(objectName + ".translateZ")
            translate = Vec3(x,y,z)
            rotateX = cmds.getAttr(objectName + ".rotateX")
            rotateY = cmds.getAttr(objectName + ".rotateY")
            rotateZ = cmds.getAttr(objectName + ".rotateZ")
            tile = Tile()
            rotateX *= -1
            translate.y -= TileInfo.height * 2
            translate.x -= TileInfo.width * (2.0 / 3)
            mel.eval("rotate -r -os " + str(rotateX) + " 0 180")
            mel.eval("move -r " + translate.ToString())

    def get_rigidbody_name(self, xNum, isFirstRow):
        name = "rigidBody"
        if isFirstRow:
            return name + str(xNum)
        else:
            return name + str(xNum + self.NumberOfTileY)

    def get_tile_name(self, x, y):
        name =  "tile{0}_{1}".format(x,y)
        return name

