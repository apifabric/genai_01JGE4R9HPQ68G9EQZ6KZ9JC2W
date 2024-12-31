import json
import logging
import os
import sys
import safrs
import subprocess
import time
from importlib import import_module
from pathlib import Path
from werkzeug.utils import secure_filename
from database.models import *
from logic_bank.logic_bank import DeclareRule, Rule, LogicBank
from colorama import Fore, Style, init


app_logger = logging.getLogger(__name__)
declare_logic_message = "ALERT:  *** No Rules Yet ***"  # printed in api_logic_server.py

rule_import_template = """
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
{rule_code}
"""

MANAGER_PATH = "/opt/webgenai/database/manager.py"
EXPORT_JSON_PATH = "./docs/export/export.json"

def set_rule_status(rule_id, status):
    """
    Call the manager.py script to set the status of a rule
    
    (if the status is "active", the manager will remove the rule error)
    """
    subprocess.run([
            "python", MANAGER_PATH, 
            "-R", rule_id,
            "--rule-status", status],
            cwd="/opt/webgenai")


def set_rule_error(rule_id, error):
    """
    Call the manager.py script to set the error of a rule
    """
    subprocess.run([
                "python", MANAGER_PATH, 
                "-R", rule_id,
                "--rule-error", error],
                cwd="/opt/webgenai")


def get_exported_rules(rule_code_dir):
    """
    Read the exported rules from export.json and write the code to the 
    rule_code_dir
    """
    export_file = Path(EXPORT_JSON_PATH)
    if not export_file.exists():
        app_logger.info(f"{export_file.resolve()} does not exist")
        return

    try:
        with open(export_file) as f:
            export = json.load(f)
        rules = export.get("rules", [])
    except Exception as exc:
        app_logger.warning(f"Failed to load rules from {export_file}: {exc}")
        return []

    for rule in rules:
        if rule["status"] == "rejected":
            continue
        rule_file = rule_code_dir / f"{secure_filename(rule['name'])}.py"
        try:
            # write current rule to rule_file
            # (we can't use eval, because logicbank uses inspect)
            with open(rule_file, "w") as temp_file:
                rule_code = "\n".join([f"  {code}" for code in rule["code"].split("\n")])
                temp_file.write(rule_import_template.format(rule_code=rule_code))
                temp_file_path = temp_file.name
            # module_name used to import current rule
            module_name = Path(temp_file_path).stem
            rule["module_name"] = module_name
        except Exception as exc:
            app_logger.warning(f"Failed to write rule code to {rule_file}: {exc}")
            
    return rules

def verify_rules(rule_code_dir, rule_type="accepted"):
    """
    Verify the rules from export.json and activate them if they pass verification
    
    write the rule code to a temporary file and import it as a module
    """
    rules = get_exported_rules(rule_code_dir)
    
    for rule in rules:
        if not rule["status"] == rule_type:
            continue
        module_name = rule["module_name"]
        app_logger.info(f"\n{Fore.BLUE}Verifying rule {rule['name']} - {rule['id']}{Style.RESET_ALL}")
        try:
            rule_module = import_module(module_name)
            rule_module.init_rule()
            LogicBank.activate(session=safrs.DB.session, activator=rule_module.init_rule)
            if rule["status"] != "active":
                set_rule_status(rule["id"], "active")
            app_logger.info(f"\n{Fore.GREEN}Activated rule {rule['id']}{Style.RESET_ALL}")
        except Exception as exc:
            set_rule_error(rule["id"], f"{type(exc).__name__}: {exc}")
            app_logger.warning(f"{Fore.RED}Failed to verify rule code\n{rule['code']}\n{Fore.YELLOW}{type(exc).__name__}: {exc}{Style.RESET_ALL}")


def load_active_rules(rule_code_dir):
    rules = get_exported_rules(rule_code_dir)
    for rule in rules:
        if not rule["status"] == "active":
            continue
        module_name = rule["module_name"]
        app_logger.info(f"{Fore.GREEN}Loading Rule Module {module_name}{Style.RESET_ALL}")
        rule_module = import_module(module_name)
        rule_module.init_rule()


def get_project_id():
    if os.environ.get("PROJECT_ID"):
        return os.environ.get("PROJECT_ID")
    
    return Path(os.getcwd()).name

def load_verify_rules():
    
    log_dir = Path("./logs/") # in the project root
    log_dir.mkdir(parents=True, exist_ok=True)
    # Add FileHandler to app_logger
    log_file = log_dir / "verify.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)
    
    rule_code_dir = Path("./logic/wg_rules") # in the project root
    rule_code_dir.mkdir(parents=True, exist_ok=True)
    sys.path.append(f"{rule_code_dir}")
    
    app_logger.info(f"Loading rules from {rule_code_dir.resolve()}")
    
    if os.environ.get("VERIFY_RULES") == "True":
        verify_rules(rule_code_dir, rule_type="active")
    else:
        try:
            load_active_rules(rule_code_dir)
        except Exception as exc:
            app_logger.warning(f"{Fore.RED}Failed to load active exported rules: {exc}{Style.RESET_ALL}")
            
    if os.environ.get("VERIFY_RULES") == "True":
        verify_rules(rule_code_dir, rule_type="accepted")
        
    app_logger.removeHandler(file_handler)