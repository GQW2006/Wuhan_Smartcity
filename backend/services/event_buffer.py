"""
services/event_buffer.py - 事故点缓冲区分析服务

对目标事故点生成指定半径（米）的缓冲区，并判断缓冲区内是否存在其他事故点。
计算全部下沉到 PostGIS 完成，不把空间数据拉到 Python 里算：
- ST_Buffer(geom::geography, 距离)  地理缓冲区：直接按米计算，避免投影变形，再转回 4326 输出
- ST_DWithin(geom::geography, ...)  判断其他事故点是否落在缓冲区范围内（含边界）
- ST_Distance(geom::geography, ...) 按距离由近到远排序
"""
import json

from sqlalchemy import text

from app.model import Wuhan_events


def get_event_buffer(session, event_id, distance):
    """计算目标事故点的缓冲区及圈内其他事故点。

    Args:
        session: SQLAlchemy Session（蓝图传 db.session 即可）
        event_id: 目标事故点 id（String PK）
        distance: 缓冲区半径（米）

    Returns:
        dict: {
            "buffer": 缓冲区面 Feature（含目标点信息），
            "events": 圈内其他事故点 FeatureCollection，
            "count":  圈内其他事故点数量，
        }

    Raises:
        ValueError: 目标事故点不存在（由蓝图转为 404）
    """
    # 0. 目标事故点必须存在
    target = session.get(Wuhan_events, event_id)
    if target is None:
        raise ValueError(f"事故点 {event_id} 不存在")

    # 1. 生成缓冲区面（geography 缓冲按米计算，结果转回 4326 供前端展示）
    # 注意：表名 Wuhan_events 含大写字母，裸 SQL 需双引号引用，否则被折叠成小写报表不存在
    buffer_sql = text(
        'SELECT ST_AsGeoJSON(ST_Buffer(geom::geography, :distance)::geometry) '
        'FROM "Wuhan_events" WHERE id = :event_id'
    )
    buffer_geojson = session.execute(
        buffer_sql, {"distance": distance, "event_id": event_id}
    ).scalar()

    # 2. 圈内其他事故点（排除目标自身，按距离由近到远排序）
    within_sql = text(
        """
        SELECT id, name, level, car_num, phone, event_num, area,
               ST_AsGeoJSON(geom) AS geojson
        FROM "Wuhan_events"
        WHERE ST_DWithin(
                geom::geography,
                (SELECT geom FROM "Wuhan_events" WHERE id = :event_id)::geography,
                :distance
              )
          AND id != :event_id
        ORDER BY ST_Distance(
                geom::geography,
                (SELECT geom FROM "Wuhan_events" WHERE id = :event_id)::geography
              )
        """
    )
    rows = session.execute(
        within_sql, {"distance": distance, "event_id": event_id}
    ).mappings()

    features = []
    for row in rows:
        properties = {k: v for k, v in row.items() if k != "geojson"}
        geometry = json.loads(row["geojson"])
        features.append({"type": "Feature", "properties": properties, "geometry": geometry})

    buffer_feature = {
        "type": "Feature",
        "properties": {
            "id": target.id,
            "name": target.name,
            "level": target.level,
            "distance": distance,
        },
        "geometry": json.loads(buffer_geojson) if buffer_geojson else None,
    }

    return {
        "buffer": buffer_feature,
        "events": {"type": "FeatureCollection", "features": features},
        "count": len(features),
    }
