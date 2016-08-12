#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from flask import (Flask,
                   render_template
                   )
from info import INFO_API
from spider import SPIDER_API


def create_app():
    app = Flask(__name__, template_folder='static')
    app.register_blueprint(INFO_API)
    app.register_blueprint(SPIDER_API)
    return app

app = create_app()


@app.route('/<page>.html', methods=['GET'])
def index(page):
    return render_template('html/{}.html'.format(page))

# app.run(debug=True)