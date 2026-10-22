import json

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Mapped, mapped_column
from extensions import db

class Wuhan_events(db.Model):
    __tablename__ = 'Wuhan_events'
    id: Mapped[str] = mapped_column(primary_key=True)
    geom: Mapped[Geometry] = mapped_column(Geometry('POINT', srid=4326))
    name: Mapped[str] = mapped_column()
    level: Mapped[int] = mapped_column()
    car_num: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    event_num: Mapped[str] = mapped_column()
    area: Mapped[str] = mapped_column()

    @property
    def geojson(self):
        """把 geom 转成 GeoJSON 字符串，供 Wuhan_eventsOutSchema.geojson 输出"""
        return json.dumps(to_shape(self.geom).__geo_interface__)

def __repr__(self):
    return f'<Wuhan_events(id={self.id}, name={self.name}, level={self.level}, car_num={self.car_num}, phone={self.phone}, event_num={self.event_num}, area={self.area})>'
