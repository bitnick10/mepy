import maya.mel as mel
import maya.cmds as cmds
from Vec3 import Vec3
from Node import Node

class Transform(Node):
    def __init__(self):
        pass

    @property
    def Translate(self):
        return Vec3(0,0,0)

    @Translate.setter
    def Translate(self,value):
        mel.eval("select - r " + self.Name)
        cmd = "move -r " + value.ToString()
        mel.eval(cmd)

    @property
    def Rotate(self):
        pass

    @Rotate.setter
    def Rotate(self,value):
        mel.eval("select - r " + self.Name)
        mel.eval("rotate -r -os " + value.ToString())

    # copied from
    # http://www.fevrierdorian.com/blog/post/2011/09/27/Quickly-retrieve-vertex-positions-of-a-Maya-mesh-(English-Translation)
    def getVtxPos(self, shapeNode):
        vtxWorldPosition = [] # will contain positions un space of all object vertex
        vtxIndexList = cmds.getAttr(shapeNode + ".vrts", multiIndices=True)
        for i in vtxIndexList :
            curPointPosition = cmds.xform(str(shapeNode) + ".pnts[" + str(i) + "]", query=True, translation=True, worldSpace=True)    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
            vtxWorldPosition.append(curPointPosition)
        return vtxWorldPosition

    def GetVertexsPos(self):
        vertexs = []
        poses = self.getVtxPos(self.Name + "Shape")
        for pos in poses:
            v = Vec3(pos[0],pos[1],pos[2])
            vertexs.append(v)
        return vertexs