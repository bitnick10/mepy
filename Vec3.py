import math

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