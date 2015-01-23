import maya.mel as mel
import maya.cmds as cmds
from Transform import Transform

class Tile:
    transform = Transform()
    @property
    def Transform(self):
        return self.transform

    @Transform.setter
    def Transform(self,value):
        transform = value;

    def __init__(self):
        mel.eval("select - r tile")
        name = mel.eval("duplicate - rr")
        self.Transform.Name = name[0]