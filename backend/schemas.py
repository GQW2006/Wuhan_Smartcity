from marshmallow import Schema, fields, validate, EXCLUDE

#==============GET输出序列化Shema，返回给前端(只读)=====================
class Wuhan_roadsOutSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    id = fields.Int()
    geojson = fields.String()
    osm_id = fields.Int()
    name = fields.String()
    type = fields.String()

class Wuhan_eventsOutSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    id = fields.String()
    geojson = fields.String()
    name = fields.String()
    level = fields.Int()
    car_num = fields.String()
    phone = fields.String()
    event_num = fields.String()
    area = fields.String()

class Wuhan_BuildingsOutSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True  

    id = fields.Int()
    Elevation = fields.Int()
    geojson = fields.String()
#==============POST输入序列化Shema，接收前端数据=====================
class Wuhan_roadsInSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True  

    name = fields.String(required=True)
    osm_id = fields.Int(required=True)
    type = fields.String(required=True)
    geom = fields.Dict(required=True)

class Wuhan_eventsInSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True  

    name = fields.String(required=True)
    level = fields.Int(required=True,validate=validate.Range(min=0,max=5))
    car_num = fields.String(required=True)
    phone = fields.String(required=True)
    event_num = fields.String(required=True)
    area = fields.String(required=True)
    geom = fields.Dict(required=True)

class Wuhan_BuildingsInSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True  

    Elevation = fields.Int(required=True)
    geom = fields.Dict(required=True)

#========Query查询参数（过滤/空间查询）========
class Wuhan_roadsQuerySchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True  
    type = fields.String()
    name = fields.String()

class Wuhan_eventsQuerySchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True   
    name = fields.String()
    level = fields.Int()
    car_num = fields.String()
    phone = fields.String()
    event_num = fields.String()
    area = fields.String()

class Wuhan_eventsBufferQuerySchema(Schema):
    """缓冲区分析查询参数：distance 为缓冲区半径（米），默认 1000"""
    class Meta:
        unknown = EXCLUDE
        ordered = True
    distance = fields.Int(load_default=1000, validate=validate.Range(min=1, max=50000))

class Wuhan_BuildingsQuerySchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True  
    Elevation = fields.Int()



