# ==========================================
# Global Settings for Red Team Simulator
# ==========================================

# Scan Configuration
scan_depth: 100              # Number of targets or ports to scan (used if relevant)
scan_timeout: 30             # Timeout in seconds for each scan attempt
user_agent: "Mozilla/5.0 (compatible; RedTeamSim/1.0)"

# Module Flags
modules:
  enable_brute_force: false  # Toggle brute-force exploitation module
  stealth_mode: true         # Reduce logging/noise for stealth simulations
  verify_ssl: false          # Whether to verify SSL certificates during web exploits

# Output & Reporting
output_format: "html"         # Can be 'html' or 'pdf'
report_directory: "./reports" # Directory to save generated reports
log_level: "INFO"             # Logging level (DEBUG, INFO, WARNING, ERROR)

# Simulation Parameters
max_retries: 3               # Max retries for failed tasks
delay_between_tasks: 1.5     # Delay in seconds between each task
ports: [22, 80, 443, 3306]  # Default ports to scan if not overridden per target
