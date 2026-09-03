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
            for layer in Wuhan_Buildings:
                for feature in layer['features']:
                    if feature['id'] == id:
                        return ok(feature)
            return fail(msg='id not found',http=404)
        return ok(Wuhan_Buildings)
        
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
            "id":str(len(Wuhan_Buildings[0]['features'])+1)
        }
        Wuhan_Buildings[0]['features'].append(feature)
        return ok(Wuhan_Buildings)
    def delete(self,id=None):
        if id:
            for layer in Wuhan_Buildings:
                for feature in layer['features']:
                    if feature['id'] == id:
                        layer['features'].remove(feature)
                        return ok(Wuhan_Buildings)
            return fail(msg='id not found',http=404)
        return ok(Wuhan_Buildings)

Wuhan_Buildings_bp.add_url_rule("/", view_func=Wuhan_BuildinsView.as_view("Wuhan_Buildings"))
