import maya.mel as mel
import maya.cmds as cmds
from Transform import Transform
from Mesh import Mesh

class Tile(object):
    @property
    def Transform(self):
        return self.transform

    @Transform.setter
    def Transform(self, value):
        self.transform = value

    @property
    def Name(self):
        return self.Transform.Name

    @Name.setter
    def Name(self, value):
        self.Transform.Name = value
    
    def __init__(self):
        self.transform = Transform()
        self._length = 0
        self._height = 0
        self._width = 0
        
    def Duplicate(self):
        mel.eval("select - r " + self.Transform.Name)
        name = mel.eval("duplicate - rr")
        newTile = Tile()
        newTile.Transform.Name = name[0]
        return newTile

    def caculate_length_height_width(self):
        mesh = Mesh()
        mesh.Name = self.Transform.Name + "Shape"
        vertexs = mesh.GetVertexsPos()
        listX = []
        listY = []
        listZ = []
        for v in vertexs:
            listX.append(v.x)
            listY.append(v.y)
            listZ.append(v.z)
        
        self._length = max(listZ) - min(listZ)
        self._height = max(listY) - min(listY)
        self._width = max(listX) - min(listX)

    def GetLength(self):
        self.caculate_length_height_width()
        return self._length

    def GetHeight(self):
        self.caculate_length_height_width()
        return self._height

    def GetWidth(self):
        self.caculate_length_height_width()
        return self._width

    def PrintInfo(self):
        print "Tile Length = {0}, Width = {1}, Height = {2}".format(self._length, self._width, self._height)