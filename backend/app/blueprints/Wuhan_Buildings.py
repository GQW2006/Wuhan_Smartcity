from flask import Blueprint,request
from flask.views import MethodView

from utils.respones import ok,fail

Wuhan_Buildings_bp = Blueprint('Wuhan_Buildings', __name__, url_prefix='/Wuhan_Buildings')


import json
import os

BasePath = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

with open(os.path.join(BasePath,"data","Wuhan_Buildings.json"),encoding='utf-8') as f:
    data = json.load(f)
    Wuhan_Buildings = data

class Wuhan_BuildinsView(MethodView):
    def get(self,id=None):
        if id:
            for feature in Wuhan_Buildings['features']:
                    if str(feature['id']) == str(id):
                        return ok(feature)
            return fail(msg='id not found',http=404)
        return ok(Wuhan_Buildings)
        
    def post(self):
        data = request.get_json(silent=True) or {}
        coordinates = (data.get('geometry' or {}).get('coordinates'))
        if not coordinates:
            return fail(msg='coordinates is empty',http=400)
        features = Wuhan_Buildings['features']
        # 取出类型伟int的id，过滤掉非int的id
        ids = [int(feature['id']) for feature in features if isinstance(feature.get('id'),int)]
        new_id = str(max(ids)+1) if ids else str(len(features)+1)
        feature = {
            "type":"Feature",
            "geometry":{
                "type":"Point",
                "coordinates":coordinates
            },
            "properties":data.get('properties',{}),
            "id":new_id
        }
        features.append(feature)
        return ok(feature)
    def delete(self,id=None):
        features = Wuhan_Buildings['features']
        for i,feature in enumerate(features):
            if str(feature.get('id')) == str(id):
                    del features[i]
                    return ok(feature)
        return fail(msg='id not found',http=404)


Wuhan_Buildings_bp.add_url_rule("/", view_func=Wuhan_BuildinsView.as_view("Wuhan_Buildings_list"))
Wuhan_Buildings_bp.add_url_rule("/<int:id>", view_func=Wuhan_BuildinsView.as_view("Wuhan_Buildings_detail"))

