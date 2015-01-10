import maya.mel as mel
import maya.cmds as cmds
import random
import math

roofTiles = RoofTiles()
roofTiles.ExposeDistanceRange = [1.2,2.5]
roofTiles.RotateYRange = [-2,2]
roofTiles.CreateTiles()
roofTiles.Simulate()

class Vec3:
    x = 0
    y = 0
    z = 0

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def ToString(self):
        return '{0} {1} {2}'.format(self.x,self.y,self.z)

    def DistanceYZ(self, pos):
        return math.sqrt(pow(self.y - pos.y,2) + pow(self.z-pos.z,2))

    def GetOneCopy(self):
        copy = Vec3(0,0,0)
        copy.x = self.x;
        copy.y = self.y;
        copy.z = self.z;
        return copy
class TileInfo:
    length = 3.2 # maya
    width = 2.4  # from AI
    height = 0.8 # from AI

class Tile:
    name = ""
    pos = Vec3(0,0,0)
    column = 1
    row = 1  
    def __init__(self):
        pass

    def CreateAt(self,pos,rotateY):
        cmd = "move -r " + pos.ToString();
        mel.eval("select - r tile")
        mel.eval("duplicate - rr")
        mel.eval(cmd)
        r = Vec3(0,0,0)
        r.y = rotateY
        mel.eval("rotate -r -os " + r.ToString())
    def Create(self):
        cmd = "move -r " + self.pos.ToString();
        mel.eval("select - r tile")
        mel.eval("duplicate - rr")
        mel.eval(cmd)

    def GetTileName(self,x,y):
    	return 

class Roof:
    Vertexs = []
    outOffset = 0
    def __init__(self):
        positions = self.GetVertexsPos("roofShape")
        positions.sort(key = lambda v:v.x)
        positions = positions[:len(positions)/2]
        positions.sort(key = lambda v:v.z,reverse = True)
        self.Vertexs = positions
        # vertexs.sort(key = lambda v:(v.x,v.z))
        for i in range(len(self.Vertexs)):
            print i, self.Vertexs[i].ToString()

    def GetNearestVertex(self, pos, tile):
        # out of the roof top 
        topVertex = self.Vertexs[len(self.Vertexs)-1]
        if (topVertex.z > pos.z or topVertex.DistanceYZ(pos) < TileInfo.length):
            ret = self.Vertexs[len(self.Vertexs)-1].GetOneCopy()
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
            
            # print "pos=",pos.ToString(),"v=",v.ToString(),"d=" ,pos.DistanceYZ(v),"tile=",tile.length
        for i in range(len(distances)):
            distances[i] -= TileInfo.length
            if distances[i] < 0:
                distances[i] *= -1;
        i = distances.index(min(distances))
        # print "distance i " ,i
        return self.Vertexs[i]


    # copied from
    # http://www.fevrierdorian.com/blog/post/2011/09/27/Quickly-retrieve-vertex-positions-of-a-Maya-mesh-(English-Translation)
    def getVtxPos(self, shapeNode):
        vtxWorldPosition = [] # will contain positions un space of all object vertex
        vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )
        for i in vtxIndexList :
            curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
            vtxWorldPosition.append( curPointPosition )
        return vtxWorldPosition

    def GetVertexsPos(self,shapeNode):
        vertexs = []
        poses = self.getVtxPos(shapeNode)
        for pos in poses:
            v = Vec3(pos[0],pos[1],pos[2])
            vertexs.append(v)
        return vertexs

class RoofTiles:
    roof = Roof()
    tileInfo = Tile()
    columnLen = 25
    rowLen = 20
    currentTime = 0
    ExposeDistanceRange = [0,0]
    RotateYRange = [0,0]
    def __init__(self):
        pass

    def create_one_column_tiles(self,columnNum,offsetX):
        positions = []
        for i in range(self.columnLen):
            tile = Tile()
            tile.row = i + 1
            tile.column = columnNum
            if (i == 0):
                contact = self.roof.Vertexs[0].GetOneCopy()
            else :
                contact = positions[i - 1].GetOneCopy()
                exposeDistance = random.uniform(self.ExposeDistanceRange[0],self.ExposeDistanceRange[1])
                contact.z += TileInfo.length - exposeDistance
            # print positions[i - 1].ToString()," contact ",contact.ToString()
            pos = self.roof.GetNearestVertex(contact, tile).GetOneCopy()
            pos.x += (columnNum - 1) * offsetX
            positions.append(pos)
        for p in positions:
            tile = Tile()
            rotateY = random.uniform(self.RotateYRange[0],self.RotateYRange[1])
            tile.CreateAt(p,rotateY)

    def CreateTiles(self):
        for i in range(self.rowLen):
        # for i in range(2):
            self.create_one_column_tiles(i + 1, TileInfo.width * 1.5)

    def CreatePassiveRigidBody(self, rNum):
        for i in range(self.rowLen):
            n = i + 1
            name = self.get_tile_name(rNum,n)
            mel.eval("select -r " + name);
            mel.eval("rigidBody -passive -m 1 -dp 0 -sf 1 -df 1 -b 0 -l 0 -tf 200 -iv 0 0 0 -iav 0 0 0 -c 0 -pc 0 -i 0 0 0 -imp 0 0 0 -si 0 0 0 -sio none")
    
    def CreateHingeConstrain(self, rNum):
        for i in range(self.rowLen):
            n = i + 1
            name = self.get_tile_name(rNum,n)
            mel.eval("connectDynamic - f gravityField1 " + name) 
            mel.eval("select -r " + name);
            mel.eval("constrain - hinge - o 0 90 0")
            move_z = 0.5 * TileInfo.length * -1 
            mel.eval("move - r 0 0 " + str(move_z))

    def RemoveRigidBodyTowRow(self, rNum):
        for i in range(self.rowLen):
            n = i + 1
            tileName = self.get_tile_name(rNum,n)
            rigidBodyName = self.get_rigidbody_name(n, True)
            mel.eval("select - r " + tileName )
            mel.eval("delete " + rigidBodyName)
            mel.eval("delete rigidHingeConstraint" + str(n))
        for i in range(self.rowLen):
            n = i + 1
            tileName = self.get_tile_name(rNum + 1,n)
            rigidBodyName = self.get_rigidbody_name(n, False)
            mel.eval("select - r " + tileName )
            mel.eval("delete " + rigidBodyName)

    def SimulateTileFall(self):
        self.currentTime += 10
        mel.eval("currentTime " + str(self.currentTime));

    def Simulate(self):
        mel.eval("currentTime 1");
        mel.eval("gravity - pos 0 0 0 - m 9.8 - att 0 - dx 0 - dy - 1 - dz 0  - mxd - 1  - vsh none - vex 0 - vof 0 0 0 - vsw 360 - tsr 0.5")
        mel.eval('setAttr "gravityField1.magnitude" 100')
        for i in range(1,self.columnLen):
            self.CreatePassiveRigidBody(i)
            self.CreateHingeConstrain(i+1)
            self.SimulateTileFall()
            self.RemoveRigidBodyTowRow(i)
        mel.eval("delete gravityField1")

    def get_rigidbody_name(self, cNum, isFirstRow):
        name = "rigidBody"
        if isFirstRow:
            return name + str(cNum)
        else:
            return name + str(cNum + self.rowLen)

    def get_tile_name(self, r, c):
        cc = c - 1
        suffix = r + cc * self.columnLen
        name = "tile" + str(suffix)
        return name

