from app.blueprints import Wuhan_Buildings
from flask import Blueprint,request
from flask.views import MethodView

from utils.respones import ok,fail

Wuhan_events_bp = Blueprint('Wuhan_events', __name__, url_prefix='/Wuhan_events')


import json
import os

BasePath = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

with open(os.path.join(BasePath,"data","Wuhan_events.json"),encoding='utf-8') as f:
    data = json.load(f)
    Wuhan_events = data

class Wuhan_eventsView(MethodView):
    def get(self,id=None):
          if id:
            for layer in Wuhan_events:
                for feature in layer['features']:
                    if feature['id'] == id:
                        return ok(feature)
            return fail(msg='id not found',http=404)
          return ok(Wuhan_events)
        
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
            "id":str(len(Wuhan_events[0]['features'])+1)
        }
        Wuhan_events[0]['features'].append(feature)
        return ok(Wuhan_events)
    def delete(self,id=None):
        if id:
            for layer in Wuhan_events:
                for feature in layer['features']:
                    if feature['id'] == id:
                        layer['features'].remove(feature)
                        return ok(Wuhan_events)
            return fail(msg='id not found',http=404)
        return ok(Wuhan_events)

Wuhan_events_bp.add_url_rule("/", view_func=Wuhan_eventsView.as_view("Wuhan_events"))
