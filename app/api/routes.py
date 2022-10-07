import json
from lib2to3.pgen2 import token
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Game, game_schema, games_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/games', methods = ['POST'])
@token_required
def create_game(current_user_token):
    title = request.json['title']
    system = request.json['system']
    genre = request.json['genre']
    beaten = request.json['beaten']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token}')

    game = Game(title, system, genre, beaten, user_token=user_token)

    db.session.add(game)
    db.session.commit()

    response = game_schema.dump(game)
    return jsonify(response)


@api.route('/games', methods = ['GET'])
@token_required
def get_game(current_user_token):
    a_user = current_user_token.token
    games = Game.query.filter_by(user_token = a_user).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/games/<id>', methods = ['GET'])
@token_required
def get_single_game(current_user_token, id):
    game = Game.query.get(id)
    response = game_schema.dump(game)
    return jsonify(response)


@api.route('/games/<id>', methods = ['POST', 'PUT'])
@token_required
def update_game(current_user_token, id):
    game = Game.query.get(id)
    game.title = request.json['title']
    game.system = request.json['system']
    game.genre = request.json['genre']
    game.beaten = request.json['beaten']
    game.user_token = current_user_token.token

    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/games/<id>', methods = ['DELETE'])
@token_required
def delete_game(current_user_token, id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)