#!/usr/bin/env python3

from flask import Flask, request, make_response,jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

##fetching all the heroes
@app.get('/heroes')
def get_heroes():
    heroes=Hero.query.all()
    return make_response(jsonify([hero.to_dict() for hero in heroes]),201)

#fetching a specific hero
@app.get('/heroes/<int:id>')
def get_heroe(id):
    hero=Hero.query.filter(id==Hero.id).one()
    hero_dictionary=hero.to_dict()
    hero_power=HeroPower.query.filter(hero_dictionary['id']==HeroPower.hero_id).one()
    power=Power.query.filter(hero_power.to_dict()['power_id']==Power.id).one()
    hero_dictionary['power']=power.to_dict()
    hero_dictionary["hero_powers"]=hero_power.to_dict() 
    return make_response(jsonify([hero_dictionary]),201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)




