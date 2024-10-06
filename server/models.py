from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)


    # add relationship
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # add serialization rules
    serialize_only = ('id', 'name', 'super_name')  # Limit serialized fields

    def __repr__(self):
        return f'<Hero {self.id}>'



class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.validate_power(description)    
    # add relationship
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    # add serialization rules
    serialize_only = ('id', 'name', 'description') 
    # add validation
    @staticmethod
    def validate_power(description):
        if len(description)<20:
            raise ValueError("validation errors")


    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    def __init__(self,strength,hero_id,power_id):
        self.strength=strength
        self.hero_id=hero_id
        self.power_id=power_id
        self.validate_hero_power(strength)
    # add relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    # add serialization rules
    serialize_only = ('id', 'strength', 'hero_id', 'power_id')

   
    # add validation
    @staticmethod
    def validate_hero_power(strength):
        if strength not in [ 'Strong', 'Weak', 'Average']:
            raise ValueError("validation errors")
        return
    def __repr__(self):
        return f'<HeroPower {self.id}>'

