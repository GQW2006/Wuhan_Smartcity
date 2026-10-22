import json

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db

class Wuhan_roads(db.Model):
    __tablename__ = 'Wuhan_roads'
    id: Mapped[int] = mapped_column(primary_key=True)
    geom: Mapped[Geometry] = mapped_column(Geometry('LINESTRING', srid=4326))
    name: Mapped[str] = mapped_column()
    osm_id: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column()

    @property
    def geojson(self):
        """把 geom 转成 GeoJSON 字符串，供 Wuhan_roadsOutSchema.geojson 输出"""
        return json.dumps(to_shape(self.geom).__geo_interface__)

    def __repr__(self):
        return f'<Wuhan_roads(id={self.id}, name={self.name}, osm_id={self.osm_id}, type={self.type})>'
