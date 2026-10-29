"""
services/spatial_query.py - 通用空间查询（bbox）服务

把范围过滤下推到 PostGIS 完成，避免把全量数据取回 Python 再过滤：
- ST_MakeEnvelope(minx, miny, maxx, maxy, 4326) 构造查询矩形
- ST_Intersects(geom, envelope)                  判断要素与矩形是否相交
"""
from sqlalchemy import func

from app.model import Wuhan_events, Wuhan_roads, Wuhan_Buildings
from schemas import (
    Wuhan_eventsOutSchema,
    Wuhan_roadsOutSchema,
    Wuhan_BuildingsOutSchema,
)

# layer 参数 -> (ORM 模型, 输出 Schema)
LAYER_REGISTRY = {
    'events': (Wuhan_events, Wuhan_eventsOutSchema),
    'roads': (Wuhan_roads, Wuhan_roadsOutSchema),
    'buildings': (Wuhan_Buildings, Wuhan_BuildingsOutSchema),
}


def query_by_bbox(layer, bbox, limit=1000):
    """按 bbox 查询指定图层的要素。

    Args:
        layer: 'events' | 'roads' | 'buildings'
        bbox: (minx, miny, maxx, maxy)，WGS84 经纬度
        limit: 最大返回条数

    Returns:
        (records, schema): ORM 记录列表与对应的输出 Schema（由蓝图交给 ok_geojson）
    """
    model, schema = LAYER_REGISTRY[layer]
    minx, miny, maxx, maxy = bbox
    envelope = func.ST_MakeEnvelope(minx, miny, maxx, maxy, 4326)
    records = (
        model.query
        .filter(func.ST_Intersects(model.geom, envelope))
        .limit(limit)
        .all()
    )
    return records, schema
