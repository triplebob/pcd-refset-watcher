# PCD RefSet Monitor

Automated monitoring for NHS Digital Primary Care Domain (PCD) refset updates.

## Overview

This tool monitors the NHS Digital PCD RefSet Power BI dashboard for new refset releases and automatically creates GitHub issues when updates are detected.

## How It Works

1. **Scheduled Checks**: Runs automatically daily at 7 AM GMT
2. **API Query**: Queries the Power BI dashboard API for the current release version
3. **Change Detection**: Compares against the stored version
4. **Notifications**: Creates a GitHub issue when a new version is detected

## Features

- Lightweight API-based monitoring (no file downloads required)
- Automated GitHub issue creation for notifications
- Version tracking with commit history
- Manual workflow trigger capability

## Configuration

### Workflow Schedule

Default schedule: Daily at 7 AM GMT
To modify, edit the cron expression in `.github/workflows/pcd-monitor.yml`

## Manual Execution

Trigger the workflow manually via GitHub Actions:
1. Go to the **Actions** tab
2. Select **PCD RefSet Monitor**
3. Click **Run workflow**

## Monitored Resource

**Power BI Dashboard**: [PCD RefSet Portal](https://app.powerbi.com/view?r=eyJrIjoiNDRmYjEwMzQtZGE3MS00ZGE5LTgwMTUtNjQ2NGE1NTZiYmEzIiwidCI6IjM3YzM1NGIyLTg1YjAtNDdmNS1iMjIyLTA3YjQ4ZDc3NGVlMyJ9)

## Files

- `check_powerbi_api.py`: Power BI API client for version checking
- `.github/workflows/pcd-monitor.yml`: GitHub Actions workflow
- `stored_version.txt`: Current tracked version (auto-updated)

## Requirements

- Python 3.11+
- `requests` library

## License

This tool is for monitoring NHS Digital public data releases.
