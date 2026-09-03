from flask import Blueprint,request
from flask.views import MethodView

from utils.respones import ok,fail

Wuhan_roads_bp = Blueprint('Wuhan_roads', __name__, url_prefix='/Wuhan_roads')


import json
import os

BasePath = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

with open(os.path.join(BasePath,"data","Wuhan_roads.json"),encoding='utf-8') as f:
    data = json.load(f)
    Wuhan_roads = data

class Wuhan_roadsView(MethodView):
    def get(self,id=None):
          if id:
            for layer in Wuhan_roads:
                for feature in layer['features']:
                    if feature['id'] == id:
                        return ok(feature)
            return fail(msg='id not found',http=404)
          return ok(Wuhan_roads)
        
    def post(self):
        data = request.json
        if not data:
            return fail(msg='data is empty',http=400)
        feature = {
            "type":"Feature",
            "geometry":{
                "type":"Point",
                "coordinates":data['geometry']['coordinates']
            },
            "properties":data['properties'],
            "id":str(len(Wuhan_roads[0]['features'])+1)
        }
        Wuhan_roads[0]['features'].append(feature)
        return ok(Wuhan_roads)
    def delete(self,id=None):
        if id:
            for layer in Wuhan_roads:
                for feature in layer['features']:
                    if feature['id'] == id:
                        layer['features'].remove(feature)
                        return ok(Wuhan_roads)
            return fail(msg='id not found',http=404)
        return ok(Wuhan_roads)

Wuhan_roads_bp.add_url_rule("/", view_func=Wuhan_roadsView.as_view("Wuhan_roads_list"))
Wuhan_roads_bp.add_url_rule("/<int:id>", view_func=Wuhan_roadsView.as_view("Wuhan_roads_detail"))
