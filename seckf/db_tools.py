import logging.config
import os

from flask import current_app
from sqlalchemy.exc import IntegrityError

from seckf.database.checklist_category import ChecklistCategory
from seckf.database.code_items import CodeItem
from seckf.database.kb_items import KBItem
from seckf.initial_data import load_initial_data

log = logging.getLogger(__name__)


def clear_db(db):
    log.info("Clearing the database")
    try:
        db.drop_all()
        db.session.commit()
    except:
        log.info("Error occurred clearing the database")
        db.session.rollback()
        raise


def init_db(db):
    """Initializes the database."""
    try:
        log.info("Initializing the database")
        db.create_all()
        prerequisits()
        init_md_code_examples(db)
        init_md_testing_examples(db)
        init_md_knowledge_base(db)
        load_initial_data(db)
    except:
        db.session.remove()
        log.info("Database is already existsing, nothing to do")


def clean_db(db):
    """Clean and Initializes the database."""
    log.info("Clean and Initializing the database")
    clear_db(db)
    db.create_all()
    prerequisits(db)
    init_md_code_examples(db)
    init_md_testing_examples(db)
    init_md_knowledge_base(db)
    load_initial_data(db)
    db.session.commit()


def update_db(db):
    """Update the database."""
    log.info("Update the database")
    KBItem.query.delete()
    CodeItem.query.delete()
    db.session.commit()
    init_md_code_examples(db)
    init_md_knowledge_base(db)


def init_md_knowledge_base(db):
    """Converts markdown knowledge-base items to DB."""
    kb_dir = os.path.join(current_app.root_path, 'markdown/knowledge_base/')
    kb_dir_types = ['web', 'mobile']
    try:
        checklist_category_id = 0
        for kb_type in kb_dir_types:
            checklist_category_id += 1
            for filename in os.listdir(kb_dir + kb_type):
                if filename.endswith(".md"):
                    name_raw = filename.split("-")
                    kb_id = name_raw[0].replace("_", " ")
                    title = name_raw[3].replace("_", " ")
                    file = os.path.join(kb_dir + kb_type, filename)
                    data = open(file, 'r')
                    file_content = data.read()
                    data.close()
                    content = file_content.translate(str.maketrans({"'": r"''", "#": r""}))
                    try:
                        item = KBItem(title, content, kb_id)
                        item.checklist_category_id = checklist_category_id
                        if (kb_id == "1"):
                            item.checklist_category_id = None
                        db.session.add(item)
                        db.session.commit()
                    except IntegrityError as e:
                        raise
        log.info("Initialized the markdown knowledge-base.")
        return True
    except:
        raise


def init_md_code_examples(db):
    """Converts markdown code-example items to DB."""
    kb_dir = os.path.join(current_app.root_path, 'markdown/code_examples/web/')
    code_langs = ['asp-needs-reviewing', 'java-needs-reviewing', 'php-needs-reviewing', 'flask',
                  'django-needs-reviewing', 'go-needs-reviewing', 'ruby-needs-reviewing',
                  'nodejs-express-needs-reviewing']
    try:
        for lang in code_langs:
            for filename in os.listdir(kb_dir + lang):
                if filename.endswith(".md"):
                    name_raw = filename.split("-")
                    title = name_raw[3].replace("_", " ")
                    file = os.path.join(kb_dir + lang, filename)
                    data = open(file, 'r')
                    file_content = data.read()
                    data.close()
                    content_escaped = file_content.translate(str.maketrans({"'": r"''", "-": r"", "#": r""}))
                    try:
                        item = CodeItem(content_escaped, title, lang)
                        item.checklist_category_id = 1
                        db.session.add(item)
                        db.session.commit()
                    except IntegrityError as e:
                        print(e)
                        pass
        log.info("Initialized the markdown code-examples.")
        return True
    except:
        raise


def init_md_testing_examples(db):
    """Converts markdown testing code-example items to DB."""
    kb_dir = os.path.join(current_app.root_path, 'markdown/code_examples/web/')
    code_langs = ['testing']
    try:
        for lang in code_langs:
            for filename in sorted(os.listdir(kb_dir + lang)):
                if filename.endswith(".md"):
                    name_raw = filename.split("-")
                    title = name_raw[3].replace("_", " ")
                    file = os.path.join(kb_dir + lang, filename)
                    data = open(file, 'r')
                    file_content = data.read()
                    data.close()
                    content_escaped = file_content.translate(str.maketrans({"'": r"''", "-": r"", "#": r""}))
                    try:
                        item = CodeItem(content_escaped, title, lang)
                        item.checklist_category_id = 1
                        db.session.add(item)
                        db.session.commit()
                    except IntegrityError as e:
                        print(e)
                        pass
        log.info("Initialized the markdown testing-examples.")
        return True
    except:
        raise


def prerequisits(db):
    try:
        category = ChecklistCategory("Web applications", "category for web collection")
        db.session.add(category)
        db.session.commit()
        category = ChecklistCategory("Mobile applications", "category for mobile collection")
        db.session.add(category)
        db.session.commit()
        category = ChecklistCategory("Custom checklist", "category for custom checklist collection")
        db.session.add(category)
        db.session.commit()
        log.info("Initialized the prerequisits.")
        return True
    except:
        raise
