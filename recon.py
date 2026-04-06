#!/usr/bin/env python3
"""
recon.py - Reconnaissance Module for Red Team Offensive Security Simulator
Author: Your Name
Description: Scans targets for open ports and performs basic service fingerprinting.
"""

import socket
import logging

# Configure logger (reuse same format as main.py)
logger = logging.getLogger(__name__)

# Default ports to scan if none specified in settings
DEFAULT_PORTS = [22, 80, 443, 3306]

def scan_port(target, port, timeout=1):
    """
    Attempts to connect to a TCP port to determine if it is open.
    Returns True if port is open, False otherwise.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                return True
            else:
                return False
    except Exception as e:
        logger.error(f"Error scanning port {port} on {target}: {e}")
        return False

def fingerprint_service(target, port):
    """
    Performs a basic service fingerprint by reading the banner.
    Returns a string describing the service if available.
    """
    try:
        with socket.socket() as s:
            s.settimeout(1)
            s.connect((target, port))
            banner = s.recv(1024).decode().strip()
            return banner if banner else "Unknown Service"
    except Exception:
        return "Unknown Service"

def scan_target(target, settings):
    """
    Scans a target for open ports and fingerprints services.
    Returns a dictionary {port: service} for open ports.
    """
    ports_to_scan = settings.get("ports", DEFAULT_PORTS)
    timeout = settings.get("scan_timeout", 1)

    logger.info(f"Starting recon on {target} with ports: {ports_to_scan}")

    open_ports = {}
    for port in ports_to_scan:
        if scan_port(target, port, timeout):
            service = fingerprint_service(target, port)
            open_ports[port] = service
            logger.info(f"Port {port} open on {target} - Service: {service}")
        else:
            logger.debug(f"Port {port} closed on {target}")

    if not open_ports:
        logger.warning(f"No open ports found on {target}")

    return open_ports
