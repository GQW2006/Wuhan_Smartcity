from flask_smorest import Blueprint
from flask.views import MethodView
import uuid

from shapely.geometry import shape
from geoalchemy2.shape import from_shape

from extensions import db
from ..model import Wuhan_events
from schemas import (
    Wuhan_eventsOutSchema,
    Wuhan_eventsInSchema,
    Wuhan_eventsQuerySchema,
    Wuhan_eventsBufferQuerySchema,
)
from services.event_buffer import get_event_buffer
from utils.respones import ok, fail, ok_geojson

Wuhan_events_bp = Blueprint('Wuhan_events', __name__, url_prefix='/api/Wuhan_events')


class Wuhan_eventsView(MethodView):
    @Wuhan_events_bp.arguments(Wuhan_eventsQuerySchema, location="query")
    def get(self, args, id=None):
        query = Wuhan_events.query
        if id is not None:
            query = query.filter(Wuhan_events.id == id)
        if args.get('name') is not None:
            query = query.filter(Wuhan_events.name == args['name'])
        if args.get('level') is not None:
            query = query.filter(Wuhan_events.level == args['level'])
        if args.get('car_num') is not None:
            query = query.filter(Wuhan_events.car_num == args['car_num'])
        if args.get('phone') is not None:
            query = query.filter(Wuhan_events.phone == args['phone'])
        if args.get('event_num') is not None:
            query = query.filter(Wuhan_events.event_num == args['event_num'])
        if args.get('area') is not None:
            query = query.filter(Wuhan_events.area == args['area'])
        return ok_geojson(query.all(), Wuhan_eventsOutSchema)

    @Wuhan_events_bp.arguments(Wuhan_eventsInSchema, location="json")
    def post(self, data):
        geom = from_shape(shape(data['geom']), srid=4326)
        record = Wuhan_events(
            id=str(uuid.uuid4()),
            name=data['name'],
            level=data['level'],
            car_num=data['car_num'],
            phone=data['phone'],
            event_num=data['event_num'],
            area=data['area'],
            geom=geom,
        )
        db.session.add(record)
        db.session.commit()
        return ok(Wuhan_eventsOutSchema().dump(record))

    def delete(self, id):
        record = Wuhan_events.query.get(id)
        if not record:
            return fail(msg='id not found', http=404)
        db.session.delete(record)
        db.session.commit()
        return ok({'deleted': id})


class Wuhan_eventsBufferView(MethodView):
    """缓冲区分析：GET /api/Wuhan_events/<id>/buffer?distance=1000"""

    @Wuhan_events_bp.arguments(Wuhan_eventsBufferQuerySchema, location="query")
    def get(self, args, id):
        distance = args.get('distance', 1000)
        try:
            result = get_event_buffer(db.session, id, distance)
        except ValueError as e:
            return fail(msg=str(e), http=404)
        return ok(result)


Wuhan_events_bp.add_url_rule("/", view_func=Wuhan_eventsView.as_view("Wuhan_events_list"))
Wuhan_events_bp.add_url_rule("/<id>", view_func=Wuhan_eventsView.as_view("Wuhan_events_detail"))
Wuhan_events_bp.add_url_rule(
    "/<id>/buffer",
    view_func=Wuhan_eventsBufferView.as_view("Wuhan_events_buffer"),
)
