from Roof import Roof
from Tile import Tile
from Vec3 import Vec3
import math
from Transform import Transform

class TongRoofWorker(object):
    """Tong Roof Worker"""
    #SourceUpperTile = Tile()
    def __init__(self):
        self.roof = Roof()
        self.NumberOfTileY = 0
        self.NumberOfTileX = 0
        self.SourceUpperTile = Tile()
        self.OffsetRotateX = 0

    def DuplicateTile(self):
        for x in range(1,self.NumberOfTileX + 1):
            for y in range(1,self.NumberOfTileY + 1):
                newTile = self.SourceUpperTile.Duplicate()
                pos = Vec3(x * self.SourceUpperTile.GetWidth() * 1.5,0,-y * self.SourceUpperTile.GetLength() * 1.5)
                newTile.Transform.Translate = pos
                newTile.Transform.Rename(self.get_tile_name(x,y))

    def get_tile_name(self, x, y):
        name = "{0}{1}_{2}".format(self.SourceUpperTile.Transform.Name,x,y)
        return name

    def layout_one_column_tiles(self,xn,offsetX):
        positions = []
        for i in range(self.NumberOfTileY):
            if (i == 0):
                contact = self.roof.Vertexs[0].GetOneCopy()
            else :
                contact = positions[i - 1].GetOneCopy()
            pos = self.roof.GetNearestVertex(contact,self.SourceUpperTile.GetLength()).GetOneCopy()
            pos.x += (xn - 1) * offsetX
            positions.append(pos)
        for i,p in enumerate(positions):
            y = i + 1
            tileTransform = Transform()
            tileTransform.Name = self.get_tile_name(xn,y)
            tileTransform.Translate = p

        for i in range(self.NumberOfTileY):
            y = i + 1
            if y != 1:
                tileTransform = Transform()
                tileTransform.Name = self.get_tile_name(xn,y)
                beforeTransform = Transform()
                beforeTransform.Name = self.get_tile_name(xn,i)
                h = tileTransform.Translate.y - beforeTransform.Translate.y
                v = h / self.SourceUpperTile.GetLength()
                rotateX = -(math.asin(v) / math.pi * 180)
                rotateX += self.OffsetRotateX
                tileTransform.Rotate = Vec3(rotateX,0,0)

    def LayoutTiles(self):
        for i in range(self.NumberOfTileX):
            self.layout_one_column_tiles(i + 1, self.SourceUpperTile.GetWidth() * (1 + self.TileXSpace))
