import datetime
import json
import logging
import os
import sys
from decimal import Decimal
from importlib import import_module
from pathlib import Path
from werkzeug.utils import secure_filename
import api.system.opt_locking.opt_locking as opt_locking
import database.models as models
from database.models import *
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import DeclareRule, Rule, LogicBank
from logic_bank.rule_bank.rule_bank import Singleton, RuleBank
from security.system.authorization import Grant, Security
from logic.load_verify_rules import load_verify_rules

app_logger = logging.getLogger(__name__)
declare_logic_message = "ALERT:  *** No Rules Yet ***"  # printed in api_logic_server.py


def declare_logic():
    ''' Declarative multi-table derivations and constraints, extensible with Python.
 
    Brief background: see readme_declare_logic.md
    
    Your Code Goes Here - Use code completion (Rule.) to declare rules
    '''
    app_logger.error("Starting declare_logic.py! \n")
    load_verify_rules()
        
    from logic.logic_discovery.auto_discovery import discover_logic
    discover_logic()

    def handle_all(logic_row: LogicRow):  # #als: TIME / DATE STAMPING, OPTIMISTIC LOCKING
        """
        This is generic - executed for all classes.

        Invokes optimistic locking, and checks Grant permissions.

        Also provides user/date stamping.

        Args:
            logic_row (LogicRow): from LogicBank - old/new row, state
        """
        if logic_row.is_updated() and logic_row.old_row is not None and logic_row.nest_level == 0:
            opt_locking.opt_lock_patch(logic_row=logic_row)

        Grant.process_updates(logic_row=logic_row)

    Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all)

    app_logger.debug("..logic/declare_logic.py (logic == rules + code)")

