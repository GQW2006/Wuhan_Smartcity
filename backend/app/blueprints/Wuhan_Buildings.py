from flask_smorest import Blueprint
from flask.views import MethodView
from sqlalchemy import func
from shapely.geometry import shape
from geoalchemy2.shape import from_shape

from extensions import db
from ..model import Wuhan_Buildings
from schemas import Wuhan_BuildingsOutSchema, Wuhan_BuildingsQuerySchema, Wuhan_BuildingsInSchema
from utils.respones import ok, fail, ok_geojson

Wuhan_Buildings_bp = Blueprint('Wuhan_Buildings', __name__, url_prefix='/api/Wuhan_Buildings')


class Wuhan_BuildingsView(MethodView):
    @Wuhan_Buildings_bp.arguments(Wuhan_BuildingsQuerySchema, location="query")
    def get(self, args, id=None):
        query = Wuhan_Buildings.query
        if id is not None:
            query = query.filter(Wuhan_Buildings.id == id)
        if args.get('Elevation') is not None:
            query = query.filter(Wuhan_Buildings.Elevation == args['Elevation'])
        return ok_geojson(query.all(), Wuhan_BuildingsOutSchema)

    @Wuhan_Buildings_bp.arguments(Wuhan_BuildingsInSchema, location="json")
    def post(self, data):
        geom = from_shape(shape(data['geom']), srid=4326)
        max_id = db.session.query(func.max(Wuhan_Buildings.id)).scalar() or 0
        record = Wuhan_Buildings(id=max_id + 1, Elevation=data['Elevation'], geom=geom)
        db.session.add(record)
        db.session.commit()
        return ok(Wuhan_BuildingsOutSchema().dump(record))

    def delete(self, id):
        record = Wuhan_Buildings.query.get(id)
        if not record:
            return fail(msg='id not found', http=404)
        db.session.delete(record)
        db.session.commit()
        return ok({'deleted': id})


Wuhan_Buildings_bp.add_url_rule("/", view_func=Wuhan_BuildingsView.as_view("Wuhan_Buildings_list"))
Wuhan_Buildings_bp.add_url_rule("/<int:id>", view_func=Wuhan_BuildingsView.as_view("Wuhan_Buildings_detail"))
