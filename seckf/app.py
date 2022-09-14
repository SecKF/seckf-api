#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
    Security Knowledge Framework is an expert system application
    that uses OWASP Application Security Verification Standard, code examples
    and helps developers in development.
    Copyright (C) 2021 Glenn ten Cate, Riccardo ten Cate
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import logging.config

from flask import Flask, Blueprint
from flask_cors import CORS

from seckf import settings
from seckf.api.checklist.endpoints.checklist_items_questions import ns as checklist_namespace
from seckf.api.checklist_category.endpoints.checklist_category_update import ns as checklist_category
from seckf.api.code.endpoints.checklist_kb_code_items import ns as code_namespace
from seckf.api.kb.endpoints.kb_item_new import ns as kb_namespace
from seckf.api.labs.endpoints.lab_delete import ns as lab_namespace
from seckf.api.labs_code.endpoints.lab_code_verify_answer import ns as lab_code_namespace
from seckf.api.projects.endpoints.project_item import ns as project_namespace
from seckf.api.questions.endpoints.question_store import ns as questions_namespace
from seckf.api.restplus import api
from seckf.api.search.endpoints.search_project import ns as search_namespace
from seckf.api.sprints.endpoints.sprint_results_update import ns as sprints_namespace
from seckf.api.user.endpoints.user_listprivileges import ns as users_namespace
from seckf.chatbot_tools import init_dataset
from seckf.database import db
from seckf.db_tools import clean_db, update_db, init_db


def create_app():
    flask_app = Flask(__name__)
    configure_app(flask_app)
    initialize_app(flask_app)
    db.init_app(flask_app)
    return flask_app


def configure_app(flask_app):
    """Configure the SKF app."""
    # cannot use SERVER_NAME because it will mess up the routing
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['TESTING'] = settings.TESTING
    flask_app.config['FLASK_DEBUG'] = settings.FLASK_DEBUG
    flask_app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    # flask_app.config['RABBIT_MQ_CONN_STRING'] = settings.RABBIT_MQ_CONN_STRING
    # flask_app.config['RABBIT_MQ_DEPLOYMENT_WORKER'] = settings.RABBIT_MQ_DEPLOYMENT_WORKER
    # flask_app.config['RABBIT_MQ_DELETION_WORKER'] = settings.RABBIT_MQ_DELETION_WORKER


def initialize_app(flask_app):
    """Initialize the SKF app."""
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(lab_namespace)
    api.add_namespace(lab_code_namespace)
    api.add_namespace(kb_namespace)
    api.add_namespace(code_namespace)
    api.add_namespace(users_namespace)
    api.add_namespace(project_namespace)
    api.add_namespace(sprints_namespace)
    api.add_namespace(checklist_namespace)
    api.add_namespace(checklist_category)
    api.add_namespace(questions_namespace)
    api.add_namespace(search_namespace)
    flask_app.register_blueprint(blueprint)


app = create_app()

# TO DO FIX WILDCARD ONLY ALLOW NOW FOR DEV
cors = CORS(app, resources={r"/api/*": {"origins": settings.ORIGINS}})
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


@app.cli.command('cleandb')
def cleandb_command():
    """Delete DB and creates a new database with all the Markdown files."""
    clean_db()
    log.info("cleaned the database.")


@app.cli.command('initdb')
def initdb_command():
    """Delete DB and creates a new database with all the Markdown files."""
    init_db()
    log.info("Created the database.")


@app.cli.command('initdataset')
def initdataset_command():
    """Creates the datasets needed for the chatbot."""
    init_dataset()
    log.info("Initialized the datasets.")


@app.cli.command('updatedb')
def updatedb_command():
    """Update the database with the markdown files."""
    update_db()
    log.info("Database updated with the markdown files.")
