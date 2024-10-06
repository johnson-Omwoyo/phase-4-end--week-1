#!/usr/bin/env python3

from flask import Flask, request, make_response,jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
from sqlalchemy.orm.exc import NoResultFound
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
@app.route('/heroes')
def get_heroes():
    heroes=Hero.query.all()
    return make_response(jsonify([hero.to_dict() for hero in heroes]),200)

#fetching a specific hero
@app.route('/heroes/<int:id>')
def get_heroe(id):
    hero = Hero.query.filter(Hero.id == id).one_or_none()

    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_dictionary = hero.to_dict()
 

    hero_power = HeroPower.query.filter(HeroPower.hero_id == hero.id).all()
    hero_dictionary["hero_powers"] = []
    for single_power in [h_p.to_dict() for h_p in hero_power]:
        power=Power.query.filter(single_power["power_id"]==Power.id).one()
        single_power["power"]=power.to_dict()
        hero_dictionary["hero_powers"].append(single_power)

   
    return make_response(jsonify(hero_dictionary),200)


@app.route('/powers')
def get_powers():
    return make_response( jsonify([power.to_dict() for power in Power.query.all()]),200)

@app.route('/powers/<int:id>')
def get_power(id):
    try:
        power = Power.query.filter(Power.id == id).one()
        return make_response(jsonify(power.to_dict()), 200)
    except NoResultFound:
        return make_response(jsonify({"error": "Power not found"}), 404)





@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def update_power(id):
    data = request.json

    try:
        power = Power.query.filter(Power.id == id).one()

        if request.method == 'PATCH':
            try:
                Power.validate_power(data.get("description"))
                power.description = data.get("description")
                db.session.commit()
                return make_response(jsonify(power.to_dict()), 200)
            except ValueError as ve:
                return make_response(jsonify({"errors": [str(ve)]}), 400)
        
        return make_response(jsonify(power.to_dict()), 200)

    except NoResultFound:
        return make_response(jsonify({"error": "Power not found"}), 404)


@app.route('/hero_powers',methods=["POST"])
def create_hero():
    data = request.json

    try:
        HeroPower.validate_hero_power(data.get("strength"))
        new_hero_power = HeroPower(
            strength=data.get("strength"),
            power_id=data.get("power_id"),
            hero_id=data.get("hero_id")
        )
        
        db.session.add(new_hero_power)
        db.session.commit()

        new_hero_power_dict = new_hero_power.to_dict()

        hero = Hero.query.filter(Hero.id == data.get("hero_id")).one()
        power = Power.query.filter(Power.id == data.get("power_id")).one()

        new_hero_power_dict["hero"] = hero.to_dict()
        new_hero_power_dict["power"] = power.to_dict()
        
        return make_response(jsonify(new_hero_power_dict), 200)
    except ValueError as erra:
        return make_response(jsonify({"errors": [str(erra)]}), 400)
    except NoResultFound:
        return make_response(jsonify({"error": "Hero or Power not found."}), 404)



if __name__ == '__main__': 
    app.run(port=5555, debug=True) 
 
 

 
 