from flask import Flask

from controller.mission_controller import mission_blueprint
from controller.target_controller import target_blueprint

app = Flask(__name__)

app.register_blueprint(blueprint=mission_blueprint, url_prefix='/api')
app.register_blueprint(blueprint=target_blueprint, url_prefix='/api')

if __name__ == '__main__':
    print('hi')
    # main_seed()
    app.run(debug=True, use_reloader=False)


