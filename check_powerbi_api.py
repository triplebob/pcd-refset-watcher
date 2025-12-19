#!/usr/bin/env python3
"""
PCD RefSet Monitor - Power BI API Client

Queries the NHS Digital Power BI dashboard API to retrieve the current
PCD TRUD release version.
"""
import sys
import requests
import re
import json


def get_release_version():
    """
    Query Power BI API for the PCD TRUD release version.

    Returns:
        str: Release date string (e.g., "16 Dec 2025"), or None if failed
    """
    api_url = "https://wabi-uk-south-api.analysis.windows.net/public/reports/querydata?synchronous=true"

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "x-powerbi-resourcekey": "44fb1034-da71-4da9-8015-6464a556bba3",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # Power BI query payload
    payload = {
        "version": "1.0.0",
        "queries": [{
            "Query": {
                "Commands": [{
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [{
                                "Name": "t",
                                "Entity": "TRUD Release",
                                "Type": 0
                            }],
                            "Select": [{
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {"Source": "t"}
                                    },
                                    "Property": "Last_Updated"
                                },
                                "Name": "TRUD Release.Last_Updated",
                                "NativeReferenceName": "Last_Updated"
                            }]
                        },
                        "Binding": {
                            "Primary": {
                                "Groupings": [{"Projections": [0]}]
                            },
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Top": {}}
                            },
                            "Version": 1
                        },
                        "ExecutionMetricsKind": 1
                    }
                }]
            },
            "QueryId": "",
            "ApplicationContext": {
                "DatasetId": "8adf6a1e-cd48-4975-94e3-2f6f01a702e9"
            }
        }],
        "cancelQueries": [],
        "modelId": 3881714
    }

    print("Querying Power BI API...")

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Navigate response structure to extract version
        # Path: results[0].result.data.dsr.DS[0].PH[0].DM0[0].M0
        result_text = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"][0]["M0"]

        print(f"Retrieved: {result_text}")

        # Parse date from format: "Content last updated on: 16 Dec 2025"
        date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4})', result_text)

        if date_match:
            release_date = date_match.group(1)
            print(f"Release date: {release_date}")
            return release_date

        # Fallback: return full text if date parsing fails
        print("Warning: Could not parse date, storing full text")
        return result_text

    except (requests.RequestException, KeyError, IndexError) as e:
        print(f"ERROR: Failed to retrieve version - {e}")
        return None


def main():
    """Main entry point"""
    version = get_release_version()

    if version:
        # Store version for comparison
        with open('last_version.txt', 'w') as f:
            f.write(version)
        print(f"SUCCESS: Version stored - {version}")
        sys.exit(0)
    else:
        print("FAILED: Could not retrieve version")
        sys.exit(1)


if __name__ == "__main__":
    main()
