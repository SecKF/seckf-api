# -*- coding: utf-8 -*-
"""Create an application instance."""
import logging.config

from seckf.app import create_app
from seckf.chatbot_tools import init_dataset
from seckf.database import db
from seckf.db_tools import clean_db, init_db, update_db

app = create_app()

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


@app.cli.command('cleandb')
def cleandb_command():
    """Delete DB and creates a new database with all the Markdown files."""
    clean_db(db)
    log.info("cleaned the database.")


@app.cli.command('initdb')
def initdb_command():
    """Delete DB and creates a new database with all the Markdown files."""
    init_db(db)
    log.info("Created the database.")


@app.cli.command('initdataset')
def initdataset_command():
    """Creates the datasets needed for the chatbot."""
    init_dataset(db)
    log.info("Initialized the datasets.")


@app.cli.command('updatedb')
def updatedb_command():
    """Update the database with the markdown files."""
    update_db(db)
    log.info("Database updated with the markdown files.")
