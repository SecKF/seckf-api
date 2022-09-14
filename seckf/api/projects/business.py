import datetime

from flask import abort

from seckf.api.security import log
from seckf.database import db
from seckf.database.project_sprints import ProjectSprint
from seckf.database.projects import Project


def get_project_items():
    log("User requested list projects", "MEDIUM", "PASS")
    return Project.query.paginate(1, 2500, False)


def new_project(user_id, data):
    log("User created new project", "MEDIUM", "PASS")
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    try:
        project = Project(data.get('name'), data.get('version'), data.get('description'), timestamp)
        db.session.add(project)
        db.session.commit()
    except:
        db.session.rollback()
        return abort(400, 'Project not created')
    result = Project.query.filter(Project.name == data.get('name')).first()
    return {'project_id': result.id, 'message': 'Project successfully created'}


def update_project(id, data):
    log("User requested update a specific project", "LOW", "PASS")
    try:
        project = Project.query.filter(Project.id == id).first()
        project.name = data.get('name')
        project.version = data.get('version')
        project.description = data.get('description')
        db.session.add(project)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    return {'message': 'project successfully updated'}


def delete_project(project_id):
    log("User deleted project", "MEDIUM", "PASS")
    try:
        project = (Project.query.filter(Project.id == project_id).one())
        db.session.delete(project)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return abort(400, 'Project not deleted')
    return {'message': 'Project successfully deleted'}


def get_project_item(project_id):
    log("User requested specific project stats", "MEDIUM", "PASS")
    return Project.query.filter(Project.id == project_id).first()


def stats_project(project_id):
    log("User requested specific project stats", "MEDIUM", "PASS")
    result = (ProjectSprint.query.filter(ProjectSprint.project_id == project_id).all())
    return result
