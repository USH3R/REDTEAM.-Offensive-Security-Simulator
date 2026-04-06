#!/usr/bin/env python3
"""
main.py - Hardened Orchestrator for Red Team Offensive Security Simulator
Author: Your Name
Description: Entry point for the Red Team simulator with error handling,
logging, and YAML validation.
"""

import yaml
import sys
import logging
from recon import scan_target
from exploit import run_exploits
from reporting import generate_report

# -------------------
# Logger Configuration
# -------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("redteam.log")
    ]
)
logger = logging.getLogger(__name__)

# -------------------
# YAML Loader with Hardening
# -------------------
def load_yaml(file_path):
    """
    Loads a YAML file and returns a dict.
    Returns empty dict if file is empty.
    Handles file not found and YAML parsing errors.
    """
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}
    except FileNotFoundError:
        logger.critical(f"{file_path} not found. Exiting.")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.critical(f"YAML parsing error in {file_path}: {e}")
        sys.exit(1)

# -------------------
# Main Workflow
# -------------------
def main():
    # Load configuration
    settings = load_yaml("settings.yaml")
    target_data = load_yaml("targets.yaml")
    
    # Target Validation
    targets = target_data.get("targets")
    if not isinstance(targets, list):
        logger.error("The 'targets' key in targets.yaml must be a list. Check formatting.")
        sys.exit(1)

    if not targets:
        logger.warning("No targets defined. Please add IPs or domains to targets.yaml.")
        sys.exit(0)

    logger.info("Red Team Simulator Starting...")

    for target in targets:
        try:
            logger.info(f"Processing target: {target}")

            # Step 1: Recon
            recon_data = scan_target(target, settings)
            logger.info(f"Recon complete for {target}")

            # Step 2: Exploitation
            exploit_results = run_exploits(target, recon_data, settings)
            logger.info(f"Exploitation complete for {target}")

            # Step 3: Reporting
            generate_report(target, exploit_results)
            logger.info(f"Report generated for {target}")

        except Exception as e:
            logger.error(f"Critical error on {target}: {e}", exc_info=True)

    logger.info("Red Team simulation finished.")

# -------------------
if __name__ == "__main__":
    main()
