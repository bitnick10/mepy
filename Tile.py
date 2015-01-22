import maya.mel as mel
import maya.cmds as cmds
from Polygon import Polygon

class Tile(Polygon):
    rigidBodyName = ""
    def __init__(self):
        mel.eval("select - r tile")
        name = mel.eval("duplicate - rr")
        self.Name = name[0]