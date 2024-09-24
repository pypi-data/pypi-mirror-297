from flask import Blueprint
from app.dbutil import DBController
from app.routes.base import Route

class DBRoute(Route):
    url_prefix = "/db"
    blueprint = Blueprint("db", __name__)

    @blueprint.route("clientes")
    def cliente():
        return DBController.all("usuarios")
