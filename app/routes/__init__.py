from flask import Flask

def init_app(app: Flask) -> None:
    
  from .api_blueprint import bp_api
  app.register_blueprint(bp_api)