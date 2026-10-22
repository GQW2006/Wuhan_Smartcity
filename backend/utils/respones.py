import json

from flask import jsonify


def ok(data=None):
    return jsonify({'code': 0, 'msg': 'success', 'data': data})


def fail(msg='error', http=404):
    return jsonify({'code': 20001, 'msg': msg, 'data': None}), http


def ok_geojson(records, schema):
    """将 ORM 记录序列化并组装成 GeoJSON FeatureCollection 返回（供 L7 前端直接使用）"""
    items = schema(many=True).dump(records)
    features = []
    for item in items:
        geojson = item.pop('geojson', None)
        geom = json.loads(geojson) if geojson else None
        features.append({"type": "Feature", "properties": item, "geometry": geom})
    return ok({"type": "FeatureCollection", "features": features})
