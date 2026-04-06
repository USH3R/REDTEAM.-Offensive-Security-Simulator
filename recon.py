#!/usr/bin/env python3
"""
recon.py - Reconnaissance Module for Red Team Offensive Security Simulator
Description: Scans targets for open ports and performs active service fingerprinting.
"""

import socket
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Default ports to scan if none specified in settings.yaml
DEFAULT_PORTS = [22, 80, 443, 3306, 8080]

def scan_port(target, port, timeout=1):
    """
    Attempts to connect to a TCP port to determine if it is open.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            return result == 0
    except Exception as e:
        logger.error(f"Network error scanning port {port} on {target}: {e}")
        return False

def fingerprint_service(target, port):
    """
    Performs active service fingerprinting by sending a probe and reading the banner.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2) # Slightly longer for the response
            s.connect((target, port))
            
            # Send a generic probe to trigger a response from web/ssh/ftp services
            s.send(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            
            # Use 'ignore' to prevent crashes on non-text binary data
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            
            if banner:
                # Return the first line of the banner (usually contains the version)
                return banner.splitlines()[0]
            return "No banner response"
    except Exception:
        return "Service detected (No banner)"

def scan_target(target, settings):
    """
    Orchestrates the recon phase for a specific target.
    Returns a dictionary mapping {port: service_info}.
    """
    ports_to_scan = settings.get("ports", DEFAULT_PORTS)
    timeout = settings.get("scan_timeout", 1)

    logger.info(f"Starting recon on {target} (Timeout: {timeout}s)")

    open_ports = {}
    for port in ports_to_scan:
        if scan_port(target, port, timeout):
            service = fingerprint_service(target, port)
            open_ports[port] = service
            logger.info(f"[OPEN] Port {port} - {service}")
        else:
            logger.debug(f"[CLOSED] Port {port}")

    if not open_ports:
        logger.warning(f"Recon complete: No open ports discovered on {target}")

    return open_ports
