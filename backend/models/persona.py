import base64

from flask_restful.reqparse import Namespace

from db import db, BaseModel


class PersonaModel(BaseModel):
    __tablename__ = 'persona'

    id = db.Column(db.BigInteger, primary_key=True)
    documento = db.Column(db.String(50))
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(30))


    def __init__(self, id, documento, nombre, apellido, ciudad, direccion, telefono, email):
        self.id = id
        self.documento = documento
        self.nombre = nombre
        self.apellido = apellido
        self.ciudad = ciudad
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def json(self, jsondepth=0):
        json = {
            'id': self.id,
            'documento': self.documento,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
        }

        
        return json

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

