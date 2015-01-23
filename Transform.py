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
        self.set_attr("translateX",value.x)
        self.set_attr("translateY",value.y)
        self.set_attr("translateZ",value.z)

    @property
    def Rotate(self):
        pass

    @Rotate.setter
    def Rotate(self,value):
        mel.eval("select - r " + self.Name)
        mel.eval("rotate -r -os " + value.ToString())

    def set_attr(self,attrName,attrValue):
        mel.eval("setAttr {0}.{1} {2}".format(self.Name,attrName,attrValue))