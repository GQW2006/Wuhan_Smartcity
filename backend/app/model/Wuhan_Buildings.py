import json

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db

class Wuhan_Buildings(db.Model):
    __tablename__ = 'Wuhan_Buildings'
    id: Mapped[int] = mapped_column(primary_key=True)
    geom: Mapped[Geometry] = mapped_column(Geometry('POLYGON', dimension=3, srid=4326))
    Elevation: Mapped[float] = mapped_column()

    @property
    def geojson(self):
        """把 geom 转成 GeoJSON 字符串，供 Wuhan_BuildingsOutSchema.geojson 输出"""
        return json.dumps(to_shape(self.geom).__geo_interface__)

    def __repr__(self):
        return f'<Wuhan_Buildings(id={self.id}, Elevation={self.Elevation})>'
