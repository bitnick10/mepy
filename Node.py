import maya.mel as mel
import maya.cmds as cmds

class Node(object):
    def __init__(self):
        self.name = ""

    @property
    def Name(self):
        return self.name

    @Name.setter
    def Name(self,value):
        self.name = value

    def Rename(self,newName):
        mel.eval('rename "{0}" "{1}"'.format(self.Name, newName))
        self.Name = newName
