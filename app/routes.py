from flask import Blueprint

routes = Blueprint("routes", __name__)

@routes.route("/health")
def health():
    return {"status": "ok"}
