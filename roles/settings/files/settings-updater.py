#!/usr/bin/env python3
"""

    #########################################################################
    # Title:         Settings Updater Script                                #
    # Author(s):     l3uddz                                                 #
    # URL:           https://github.com/cloudbox/cloudbox                   #
    # Description:   Adds variables to settings.yml.                        #
    # --                                                                    #
    #         Part of the Cloudbox project: https://cloudbox.works          #
    #########################################################################
    #                   GNU General Public License v3.0                     #
    #########################################################################

"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from ruamel import yaml
from ruamel.yaml.comments import CommentedMap

############################################################
# INIT
############################################################


log = None


def init_logging(playbook_path):
    """Initializes the logging for the script.

    Sets up a logger that outputs to both the console and a log file.

    Args:
        playbook_path (str): The path to the playbook directory, where the log
            file will be created.

    Returns:
        logging.Logger: A logger instance.
    """
    # log settings
    log_format = '%(asctime)s - %(levelname)-10s - %(name)-35s - %(funcName)-35s - %(message)s'
    log_file_path = os.path.join(playbook_path, "settings-updater.log")
    log_level = logging.DEBUG

    # init root_logger
    log_formatter = logging.Formatter(log_format)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # init console_logger
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    # init file_logger
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=1024 * 1024 * 5,
        backupCount=5
    )
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    # Set chosen logging level
    root_logger.setLevel(log_level)

    # Get logger
    return root_logger.getChild("settings-updater")


############################################################
# UPDATER
############################################################

def load_settings(file_to_load):
    """Loads a YAML file.

    Args:
        file_to_load (str): The path to the YAML file to load.

    Returns:
        CommentedMap or None: The loaded YAML data as a CommentedMap, or None
            if an error occurred.
    """
    settings = None
    try:
        settings = yaml.round_trip_load(open(file_to_load, "r"), preserve_quotes=True)
    except Exception:
        log.exception("Exception loading %s: ", file_to_load)
    return settings


def dump_settings(settings, file_to_dump):
    """Dumps data to a YAML file.

    Args:
        settings (CommentedMap): The data to dump to the file.
        file_to_dump (str): The path to the YAML file to dump to.

    Returns:
        bool: True if the dump was successful, False otherwise.
    """
    dumped = False
    try:
        with open(file_to_dump, 'w') as fp:
            yaml.round_trip_dump(settings, fp, indent=2, block_seq_indent=2,
                                 explicit_start=True, default_flow_style=False)
        dumped = True
    except Exception:
        log.exception("Exception dumping upgraded %s: ", file_to_dump)
    return dumped


def _inner_upgrade(settings1, settings2, key=None, overwrite=False):
    """Recursively merges two settings dictionaries.

    This function recursively merges `settings1` into `settings2`. It adds
    keys from `settings1` that are not in `settings2`.

    Args:
        settings1 (dict or list): The source settings.
        settings2 (dict or list): The destination settings to merge into.
        key (str, optional): The current key being processed. Used for logging.
            Defaults to None.
        overwrite (bool, optional): Whether to overwrite existing values in
            `settings2`. Defaults to False.

    Returns:
        tuple: A tuple containing the merged settings and a boolean indicating
            whether an upgrade was performed.
    """
    sub_upgraded = False
    merged = settings2.copy()

    if isinstance(settings1, dict):
        for k, v in settings1.items():
            # missing k
            if k not in settings2:
                merged[k] = v
                sub_upgraded = True
                if not key:
                    log.info("Added %r setting: %s", str(k), str(v))
                else:
                    log.info("Added %r to setting %r: %s", str(k), str(key), str(v))
                continue

            # iterate children
            if isinstance(v, dict) or isinstance(v, list):
                merged[k], did_upgrade = _inner_upgrade(settings1[k], settings2[k], key=k,
                                                                overwrite=overwrite)
                sub_upgraded = did_upgrade if did_upgrade else sub_upgraded
            elif settings1[k] != settings2[k] and overwrite:
                merged = settings1
                sub_upgraded = True
    elif isinstance(settings1, list) and key:
        for v in settings1:
            if v not in settings2:
                merged.append(v)
                sub_upgraded = True
                log.info("Added to setting %r: %s", str(key), str(v))
                continue

    return merged, sub_upgraded

def upgrade_settings(defaults, currents):
    """Upgrades the current settings with values from the default settings.

    Args:
        defaults (CommentedMap): The default settings.
        currents (CommentedMap): The current settings.

    Returns:
        tuple: A tuple containing a boolean indicating whether an upgrade was
            performed and the upgraded settings.
    """
    upgraded_settings, upgraded = _inner_upgrade(defaults, currents)
    return upgraded, upgraded_settings

############################################################
# MAIN
############################################################

if __name__ == "__main__":
    # get playbook dir
    if not len(sys.argv) >= 4:
        print("3 arguments must be supplied, playbook_dir default_settings current_settings")
        sys.exit(1)
    playbook_dir = sys.argv[1]
    default_file = sys.argv[2]
    current_file = sys.argv[3]

    # init logging
    log = init_logging(playbook_dir)

    # load settings
    default_settings = load_settings(os.path.join(playbook_dir, default_file))
    if not default_settings:
        log.error("Failed loading \'%s\'. Aborting...", default_file)
        sys.exit(1)

    current_settings = load_settings(os.path.join(playbook_dir, current_file))
    if not current_settings:
        log.error("Failed loading \'%s\'. Aborting...", current_file)
        sys.exit(1)

    # compare/upgrade settings
    did_upgrade, upgraded_settings = upgrade_settings(default_settings, current_settings)
    if not did_upgrade:
        log.info("There were no settings changes to apply.")
        sys.exit(0)
    else:
        if not dump_settings(upgraded_settings, os.path.join(playbook_dir, current_file)):
            log.error("Failed dumping updated \'%s\'.", current_file)
            sys.exit(1)
        log.info("Successfully upgraded: \'%s\'.", current_file)
        sys.exit(2)
