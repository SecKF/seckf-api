from seckf.api.security import log
from seckf.database.checklists_kb import ChecklistKB
from seckf.database.code_items import CodeItem
from seckf.database.kb_items import KBItem
from seckf.database.lab_items import LabItem
from seckf.database.project_sprints import ProjectSprint


def search_kb(search_string):
    log("User requested search of kb items", "LOW", "PASS")
    search = "%{}%".format(search_string)
    return KBItem.query.filter(KBItem.content.like(search)).all()


def search_lab(search_string):
    log("User requested search of lab items", "LOW", "PASS")
    search = "%{}%".format(search_string)
    lab_result = LabItem.query.filter(LabItem.title.like(search)).all()
    return lab_result


def search_code(search_string):
    log("User requested search of kb items", "LOW", "PASS")
    search = "%{}%".format(search_string)
    code_result = CodeItem.query.filter(CodeItem.title.like(search)).all()
    return code_result


def search_checklist(search_string):
    log("User requested search of kb items", "LOW", "PASS")
    search = "%{}%".format(search_string)
    checklist_result = ChecklistKB.query.filter(ChecklistKB.content.like(search)).all()
    return checklist_result


def search_project(search_string):
    log("User requested search of kb items", "LOW", "PASS")
    search = "%{}%".format(search_string)
    project_result = ProjectSprint.query.filter(ProjectSprint.description.like(search)).all()
    return project_result
