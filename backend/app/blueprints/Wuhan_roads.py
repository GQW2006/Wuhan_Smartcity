from flask_smorest import Blueprint
from flask.views import MethodView
from sqlalchemy import func

from shapely.geometry import shape
from geoalchemy2.shape import from_shape

from extensions import db
from ..model import Wuhan_roads
from schemas import Wuhan_roadsOutSchema, Wuhan_roadsInSchema, Wuhan_roadsQuerySchema
from utils.respones import ok, fail, ok_geojson

Wuhan_roads_bp = Blueprint('Wuhan_roads', __name__, url_prefix='/api/Wuhan_roads')


class Wuhan_roadsView(MethodView):
    @Wuhan_roads_bp.arguments(Wuhan_roadsQuerySchema, location="query")
    def get(self, args, id=None):
        query = Wuhan_roads.query
        if id is not None:
            query = query.filter(Wuhan_roads.id == id)
        if args.get('type') is not None:
            query = query.filter(Wuhan_roads.type == args['type'])
        if args.get('name') is not None:
            query = query.filter(Wuhan_roads.name == args['name'])
        return ok_geojson(query.all(), Wuhan_roadsOutSchema)

    @Wuhan_roads_bp.arguments(Wuhan_roadsInSchema, location="json")
    def post(self, data):
        geom = from_shape(shape(data['geom']), srid=4326)
        max_id = db.session.query(func.max(Wuhan_roads.id)).scalar() or 0
        record = Wuhan_roads(
            id=max_id + 1,
            name=data['name'],
            osm_id=data['osm_id'],
            type=data['type'],
            geom=geom,
        )
        db.session.add(record)
        db.session.commit()
        return ok(Wuhan_roadsOutSchema().dump(record))

    def delete(self, id):
        record = Wuhan_roads.query.get(id)
        if not record:
            return fail(msg='id not found', http=404)
        db.session.delete(record)
        db.session.commit()
        return ok({'deleted': id})


Wuhan_roads_bp.add_url_rule("/", view_func=Wuhan_roadsView.as_view("Wuhan_roads_list"))
Wuhan_roads_bp.add_url_rule("/<int:id>", view_func=Wuhan_roadsView.as_view("Wuhan_roads_detail"))
