from Transform import Transform
from Mesh import Mesh

class Roof:
    _transform = Transform()

    @property
    def Transform(self):
        return self._transform

    @Transform.setter
    def Transform(self,value):
        self._transform = value

    Vertexs = []
    outOffset = 0
    def __init__(self):
        self.Transform.Name = "roof"
        mesh = Mesh()
        mesh.Name = self.Transform.Name + "Shape"
        positions = mesh.GetVertexsPos()
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

    def GetNearestVertex(self, pos, tileLength):
        # out of the roof top
        topVertex = self.Vertexs[len(self.Vertexs) - 1]
        if (topVertex.z > pos.z or topVertex.DistanceYZ(pos) < tileLength):
            ret = self.Vertexs[len(self.Vertexs) - 1].GetOneCopy()
            self.outOffset += tileLength * 1.5
            ret.z -= self.outOffset
            return ret
        self.outOffset = 0
        distances = []
        for v in self.Vertexs:
            if v.z < pos.z:
                distances.append(pos.DistanceYZ(v))
            else:
                distances.append(tileLength * 999) # this should be very max
            
            # print "pos=",pos.ToString(),"v=",v.ToString(),"d="
            # ,pos.DistanceYZ(v),"tile=",tile.length
        for i in range(len(distances)):
            distances[i] -= tileLength
            if distances[i] < 0:
                distances[i] *= -1
        i = distances.index(min(distances))
        # print "distance i " ,i
        return self.Vertexs[i]