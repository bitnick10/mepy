from Roof import Roof
from Tile import Tile
from Vec3 import Vec3
import math
from Transform import Transform

class TongRoofWorker(object):
    """Tong Roof Worker"""
    def __init__(self):
        self.roof = Roof()
        self.NumberOfTileY = 0
        self.NumberOfTileX = 0
        self.SourceTile = Tile()
        self.OffsetRotateX = 0
        self.TongTile = Tile()
        self.DrippingTile = Tile()

    def DuplicateTile(self):
        for x in range(1, self.NumberOfTileX + 1):
            for y in range(1, self.NumberOfTileY + 1):
                newTile = self.SourceTile.Duplicate()
                pos = Vec3(x * self.SourceTile.GetWidth() * 1.5,0,-y * self.SourceTile.GetLength() * 1.5)
                newTile.Transform.Translate = pos
                newTile.Transform.Rename(self.get_tile_name(x,y))

    def DuplicateAndLayoutTongTile(self):
        for x in range(1, self.NumberOfTileX + 1):
            newTile = self.TongTile.Duplicate()
            tileTransform = Transform()
            tileTransform.Name = self.get_tile_name(x,1)
            pos = tileTransform.Translate.GetOneCopy();
            pos.z += self.SourceTile.GetLength()
            newTile.Transform.Translate = pos

    #def DuplicateAndLayoutDrippingTile(self):

    def get_tile_name(self, x, y):
        name = "{0}{1}_{2}".format(self.SourceTile.Name,x,y)
        return name

    def layout_one_column_tiles(self,xn,offsetX):
        positions = []
        for i in range(self.NumberOfTileY):
            if (i == 0):
                contact = self.roof.Vertexs[0].GetOneCopy()
            else :
                contact = positions[i - 1].GetOneCopy()
            pos = self.roof.GetNearestVertex(contact,self.SourceTile.GetLength()).GetOneCopy()
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
                v = h / self.SourceTile.GetLength()
                rotateX = -(math.asin(v) / math.pi * 180)
                rotateX += self.OffsetRotateX
                tileTransform.Rotate = Vec3(rotateX,0,0)

    def LayoutTiles(self):
        for i in range(self.NumberOfTileX):
            self.layout_one_column_tiles(i + 1, self.SourceTile.GetWidth() * (1 + self.TileXSpace))
