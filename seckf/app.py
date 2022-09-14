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
import logging
import sys

from flask import Flask, Blueprint
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate

from seckf import settings
from seckf.api.chatbot.endpoints.chatbot_question import ns as chatbot_namespace
from seckf.api.checklist.endpoints.checklist_item import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_item_delete import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_item_new import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_item_question import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_item_update import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_items import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_items_questions import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_question_correlation_update import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_type_create import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_type_delete import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_type_item import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_type_items import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_type_items_with_filter import ns as checklist_namespace
from seckf.api.checklist.endpoints.checklist_type_update import ns as checklist_namespace
from seckf.api.checklist_category.endpoints.checklist_category_create import ns as checklist_category
from seckf.api.checklist_category.endpoints.checklist_category_delete import ns as checklist_category
from seckf.api.checklist_category.endpoints.checklist_category_item import ns as checklist_category
from seckf.api.checklist_category.endpoints.checklist_category_items import ns as checklist_category
from seckf.api.checklist_category.endpoints.checklist_category_update import ns as checklist_category
from seckf.api.code.endpoints.checklist_kb_code_items import ns as code_namespace
from seckf.api.code.endpoints.checklist_kb_code_items_delete import ns as code_namespace
from seckf.api.code.endpoints.checklist_kb_code_items_new import ns as code_namespace
from seckf.api.code.endpoints.code_item import ns as code_namespace
from seckf.api.code.endpoints.code_item_delete import ns as code_namespace
from seckf.api.code.endpoints.code_item_update import ns as code_namespace
from seckf.api.code.endpoints.code_items import ns as code_namespace
from seckf.api.code.endpoints.code_items_new import ns as code_namespace
from seckf.api.kb.endpoints.kb_item import ns as kb_namespace
from seckf.api.kb.endpoints.kb_item_delete import ns as kb_namespace
from seckf.api.kb.endpoints.kb_item_new import ns as kb_namespace
from seckf.api.kb.endpoints.kb_item_update import ns as kb_namespace
from seckf.api.kb.endpoints.kb_items import ns as kb_namespace
from seckf.api.labs.endpoints.lab_code_item_sol import ns as lab_namespace
from seckf.api.labs.endpoints.lab_code_items import ns as lab_namespace
from seckf.api.labs.endpoints.lab_code_verify import ns as lab_namespace
from seckf.api.labs.endpoints.lab_delete import ns as lab_namespace
from seckf.api.labs.endpoints.lab_deployments import ns as lab_namespace
from seckf.api.labs.endpoints.lab_items import ns as lab_namespace
from seckf.api.labs_code.endpoints.lab_code_random_item import ns as lab_code_namespace
from seckf.api.labs_code.endpoints.lab_code_verify_answer import ns as lab_code_namespace
from seckf.api.projects.endpoints.project_delete import ns as project_namespace
from seckf.api.projects.endpoints.project_item import ns as project_namespace
from seckf.api.projects.endpoints.project_items import ns as project_namespace
from seckf.api.projects.endpoints.project_new import ns as project_namespace
from seckf.api.projects.endpoints.project_stats import ns as project_namespace
from seckf.api.projects.endpoints.project_update import ns as project_namespace
from seckf.api.questions.endpoints.question_item import ns as questions_namespace
from seckf.api.questions.endpoints.question_item_delete import ns as questions_namespace
from seckf.api.questions.endpoints.question_item_new import ns as questions_namespace
from seckf.api.questions.endpoints.question_item_update import ns as questions_namespace
from seckf.api.questions.endpoints.question_items import ns as questions_namespace
from seckf.api.questions.endpoints.question_store import ns as questions_namespace
from seckf.api.restplus import api
from seckf.api.search.endpoints.search_checklist import ns as search_namespace
from seckf.api.search.endpoints.search_code import ns as search_namespace
from seckf.api.search.endpoints.search_kb import ns as search_namespace
from seckf.api.search.endpoints.search_lab import ns as search_namespace
from seckf.api.search.endpoints.search_project import ns as search_namespace
from seckf.api.sprints.endpoints.sprint_delete import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_item import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_new import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_results import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_results_delete import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_results_export import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_results_export_external import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_results_update import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_stats import ns as sprints_namespace
from seckf.api.sprints.endpoints.sprint_update import ns as sprints_namespace
from seckf.api.user.endpoints.user_activate import ns as users_namespace
from seckf.api.user.endpoints.user_create import ns as users_namespace
from seckf.api.user.endpoints.user_list import ns as users_namespace
from seckf.api.user.endpoints.user_listprivileges import ns as users_namespace
from seckf.api.user.endpoints.user_login import ns as users_namespace
from seckf.api.user.endpoints.user_login_skip import ns as users_namespace
from seckf.api.user.endpoints.user_manage import ns as users_namespace
from seckf.database import db


def create_app(config_object="seckf.settings"):
    """Create application factory, as explained here: https://flask.palletsprojects.com/en/2.2.x/config/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)

    return app


def register_blueprints(app):
    """Initialize the seckf app."""
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
    api.add_namespace(chatbot_namespace)
    app.register_blueprint(blueprint)


def register_extensions(app):
    """Register Flask Extensions"""
    CORS(app, resources={r"/api/*": {"origins": settings.ORIGINS}})
    Bcrypt(app)
    Migrate(app)
    db.init_app(app)
    return None


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
