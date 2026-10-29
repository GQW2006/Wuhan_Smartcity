"""空间查询蓝图：GET /api/spatial/bbox"""
from flask_smorest import Blueprint
from flask.views import MethodView

from schemas import SpatialBboxQuerySchema
from services.spatial_query import query_by_bbox
from utils.respones import ok_geojson, fail

spatial_bp = Blueprint('spatial', __name__, url_prefix='/api/spatial')


class SpatialBboxView(MethodView):
    """bbox 范围查询：返回落在矩形内的要素（FeatureCollection）"""

    @spatial_bp.arguments(SpatialBboxQuerySchema, location="query")
    def get(self, args):
        if args['minx'] >= args['maxx'] or args['miny'] >= args['maxy']:
            return fail(msg='bbox 不合法：需满足 minx < maxx 且 miny < maxy', http=400)

        bbox = (args['minx'], args['miny'], args['maxx'], args['maxy'])
        records, schema = query_by_bbox(args['layer'], bbox, args['limit'])
        return ok_geojson(records, schema)


spatial_bp.add_url_rule("/bbox", view_func=SpatialBboxView.as_view("spatial_bbox"))
