import base64
import logging
from datetime import datetime

from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.persona import PersonaModel
from utils import restrict, check, paginated_results


class Persona(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('documento', type=str)
    parser.add_argument('nombre', type=str)
    parser.add_argument('apellido', type=str)
    parser.add_argument('ciudad', type=str)
    parser.add_argument('direccion', type=str)
    parser.add_argument('telefono', type=str)
    parser.add_argument('email', type=str)

    # @jwt_required()
    # @check('persona_get')
    @swag_from('../swagger/persona/get_persona.yaml')
    def get(self, id):
        persona = PersonaModel.find_by_id(id)
        if persona:
            return persona.json()
        return {'message': 'No se encuentra Persona'}, 404

    # @jwt_required()
    # @check('persona_update')
    @swag_from('../swagger/persona/put_persona.yaml')
    def put(self, id):
        persona = PersonaModel.find_by_id(id)
        if persona:
            newdata = Persona.parser.parse_args()
            PersonaModel.from_reqparse(persona, newdata)
            persona.save_to_db()
            return persona.json()
        return {'message': 'No se encuentra Persona'}, 404

    # @jwt_required()
    # @check('persona_delete')
    @swag_from('../swagger/persona/delete_persona.yaml')
    def delete(self, id):
        persona = PersonaModel.find_by_id(id)
        if persona:
            persona.delete_from_db()

        return {'message': 'Se ha borrado Persona'}


class PersonaList(Resource):

    # @jwt_required()
    # @check('persona_list')
    @swag_from('../swagger/persona/list_persona.yaml')
    def get(self):
        query = PersonaModel.query
        return paginated_results(query)

    # @jwt_required()
    # @check('persona_insert')
    @swag_from('../swagger/persona/post_persona.yaml')
    def post(self):
        data = Persona.parser.parse_args()

        id = data.get('id')

        if id is not None and PersonaModel.find_by_id(id):
            return {'message': "Ya existe un persona con id '{}'.".format(id)}, 400

        persona = PersonaModel(**data)
        try:
            persona.save_to_db()
        except Exception as e:
            logging.error('Ocurrió un error al crear Cliente.', exc_info=e)
            return {"message": "Ocurrió un error al crear Persona."}, 500

        return persona.json(), 201


class PersonaSearch(Resource):

    # @jwt_required()
    # @check('persona_search')
    @swag_from('../swagger/persona/search_persona.yaml')
    def post(self):
        query = PersonaModel.query
        if request.json:
            filters = request.json
            query = restrict(query, filters, 'id', lambda x: PersonaModel.id == x)
            query = restrict(query, filters, 'documento', lambda x: PersonaModel.documento.contains(x))
            query = restrict(query, filters, 'nombre', lambda x: PersonaModel.nombre.contains(x))
            query = restrict(query, filters, 'apellido', lambda x: PersonaModel.apellido.contains(x))
            query = restrict(query, filters, 'ciudad', lambda x: PersonaModel.ciudad.contains(x))
            query = restrict(query, filters, 'direccion', lambda x: PersonaModel.direccion.contains(x))
            query = restrict(query, filters, 'telefono', lambda x: PersonaModel.telefono.contains(x))
            query = restrict(query, filters, 'email', lambda x: PersonaModel.email.contains(x))
        return paginated_results(query)
