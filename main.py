from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String, Float, Numeric, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.seed import main_seed
# from controller.mission_controller import mission_buleprint

app = Flask(__name__)

# app.register_blueprint(blueprint=mission_buleprint, url_prefix='/api')

if __name__ == '__main__':
    print('hi')
    main_seed()
    app.run(debug=True, use_reloader=False)


