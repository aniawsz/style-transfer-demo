import os

from flask import Flask, flash, g, render_template
# from flask_sock import Sock

# sock = Sock()
from app.audio import create_audio_engine

def get_audio_engine(input_wav, model):
    if 'audio_engine' not in g:
        g.audio_engine = create_audio_engine(input_wav, model)

    return g.audio_engine

# @sock.route('/echo')
# def echo(ws):
#     while True:
#         data = ws.receive()
#         print("data received: ", data)
#         ws.send(data)

# @sock.route('/audiostream')
# def audiostream(ws):
#     ws.send(0)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # sock.init_app(app)

    if test_config is None:
        app.config.from_pyfile('application.cfg', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def main():
        audio_engine = get_audio_engine(
            app.config['INPUT_WAV'],
            app.config['MODEL'],
        )
        audio_engine.start()

        return render_template("main.html")
        # return render_template("test.html")

    return app

    @app.teardown_appcontext
    def teardown_audio_engine(exception):
        audio_engine = g.pop('audio_engine', None)

        if audio_engine is not None:
            audio_engine.stop.set()
