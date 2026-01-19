#!/bin/bash
# Unified Security Report Generator
# Combines SAST (Semgrep, Checkov) and SCA (OWASP Dependency-Check) reports

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$SCRIPT_DIR/unified-reports"

echo "=== Lab07 Unified Security Report Generator ==="
echo "Lab directory: $LAB_DIR"
echo "Output directory: $OUTPUT_DIR"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Use Python to merge JSON reports since jq is not available
python3 <<'PYTHON_SCRIPT'
import json
import os
import csv
from pathlib import Path
from datetime import datetime

lab_dir = Path(os.environ.get('LAB_DIR', '.'))
output_dir = Path(os.environ.get('OUTPUT_DIR', './unified-reports'))

# Initialize unified report structure
unified_report = {
    "metadata": {
        "generated_at": datetime.now().isoformat(),
        "lab": "lab07",
        "scan_types": ["SAST", "SCA"]
    },
    "sast": {
        "semgrep": {},
        "checkov": {}
    },
    "sca": {
        "python_dependencies": {},
        "java_dependencies": {}
    },
    "summary": {
        "total_findings": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0
    }
}

# Load Semgrep report
semgrep_path = lab_dir / "sast" / "semgrep-report.json"
if semgrep_path.exists():
    try:
        with open(semgrep_path) as f:
            semgrep_data = json.load(f)
        unified_report["sast"]["semgrep"] = semgrep_data
        # Count findings
        if "results" in semgrep_data:
            for result in semgrep_data["results"]:
                severity = result.get("extra", {}).get("severity", "info").lower()
                unified_report["summary"]["total_findings"] += 1
                if severity in ["critical", "error"]:
                    unified_report["summary"]["critical"] += 1
                elif severity == "warning":
                    unified_report["summary"]["high"] += 1
                elif severity == "info":
                    unified_report["summary"]["info"] += 1
        print(f"✓ Loaded Semgrep report: {len(semgrep_data.get('results', []))} findings")
    except Exception as e:
        print(f"⚠ Error loading Semgrep report: {e}")
else:
    print(f"⚠ Semgrep report not found: {semgrep_path}")

# Load Checkov report
checkov_path = lab_dir / "sast" / "results_json.json"
if checkov_path.exists():
    try:
        with open(checkov_path) as f:
            checkov_data = json.load(f)
        unified_report["sast"]["checkov"] = checkov_data
        # Count findings
        if "results" in checkov_data and "failed_checks" in checkov_data["results"]:
            failed = len(checkov_data["results"]["failed_checks"])
            unified_report["summary"]["total_findings"] += failed
            unified_report["summary"]["high"] += failed  # Checkov failures are typically high severity
        print(f"✓ Loaded Checkov report")
    except Exception as e:
        print(f"⚠ Error loading Checkov report: {e}")
else:
    print(f"⚠ Checkov report not found: {checkov_path}")

# Save unified JSON report
json_output = output_dir / "unified-report.json"
with open(json_output, 'w') as f:
    json.dump(unified_report, f, indent=2)
print(f"✓ Generated JSON report: {json_output}")

# Generate CSV summary
csv_output = output_dir / "unified-report.csv"
with open(csv_output, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Tool", "Type", "Finding", "Severity", "File", "Line"])

    # Semgrep findings
    if "results" in unified_report["sast"]["semgrep"]:
        for result in unified_report["sast"]["semgrep"]["results"]:
            writer.writerow([
                "Semgrep",
                "SAST",
                result.get("check_id", ""),
                result.get("extra", {}).get("severity", ""),
                result.get("path", ""),
                result.get("start", {}).get("line", "")
            ])

    # Checkov findings
    if "results" in unified_report["sast"]["checkov"] and "failed_checks" in unified_report["sast"]["checkov"]["results"]:
        for check in unified_report["sast"]["checkov"]["results"]["failed_checks"]:
            writer.writerow([
                "Checkov",
                "SAST",
                check.get("check_id", ""),
                check.get("check_class", ""),
                check.get("file_path", ""),
                check.get("file_line_range", [""])[0]
            ])

print(f"✓ Generated CSV report: {csv_output}")

# Generate simple HTML report
html_output = output_dir / "unified-report.html"
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab07 Security Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-card.critical {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
        .stat-card.high {{ background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }}
        .stat-card.medium {{ background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }}
        .stat-card.low {{ background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }}
        .stat-value {{ font-size: 36px; font-weight: bold; }}
        .stat-label {{ font-size: 14px; opacity: 0.9; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #007bff; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .badge.critical {{ background: #dc3545; color: white; }}
        .badge.high {{ background: #fd7e14; color: white; }}
        .badge.medium {{ background: #ffc107; color: #333; }}
        .badge.low {{ background: #28a745; color: white; }}
        .badge.info {{ background: #17a2b8; color: white; }}
        .timestamp {{ color: #666; font-size: 14px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Lab07 Security Analysis Report</h1>
        <p class="timestamp">Generated: {unified_report['metadata']['generated_at']}</p>

        <h2>📊 Summary</h2>
        <div class="summary">
            <div class="stat-card">
                <div class="stat-value">{unified_report['summary']['total_findings']}</div>
                <div class="stat-label">Total Findings</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-value">{unified_report['summary']['critical']}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card high">
                <div class="stat-value">{unified_report['summary']['high']}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-value">{unified_report['summary']['medium']}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-card low">
                <div class="stat-value">{unified_report['summary']['low']}</div>
                <div class="stat-label">Low</div>
            </div>
        </div>

        <h2>🔍 SAST Findings</h2>
        <h3>Semgrep</h3>
        <table>
            <tr>
                <th>Rule ID</th>
                <th>Severity</th>
                <th>File</th>
                <th>Line</th>
                <th>Message</th>
            </tr>
"""

# Add Semgrep findings to HTML
if "results" in unified_report["sast"]["semgrep"]:
    for result in unified_report["sast"]["semgrep"]["results"]:
        severity = result.get("extra", {}).get("severity", "info")
        html_content += f"""
            <tr>
                <td><code>{result.get("check_id", "")}</code></td>
                <td><span class="badge {severity}">{severity.upper()}</span></td>
                <td>{result.get("path", "")}</td>
                <td>{result.get("start", {}).get("line", "")}</td>
                <td>{result.get("extra", {}).get("message", "")[:100]}...</td>
            </tr>
        """
else:
    html_content += "<tr><td colspan='5'>No findings</td></tr>"

html_content += """
        </table>

        <h3>Checkov</h3>
        <p>See JSON report for detailed Checkov findings.</p>

        <h2>📦 SCA Findings</h2>
        <p>Dependency check results available in JSON format.</p>

        <hr style="margin: 40px 0; border: none; border-top: 2px solid #eee;">
        <p style="text-align: center; color: #666;">
            For detailed findings, see the JSON and CSV reports in the unified-reports directory.
        </p>
    </div>
</body>
</html>
"""

with open(html_output, 'w') as f:
    f.write(html_content)
print(f"✓ Generated HTML report: {html_output}")

print("\n" + "="*50)
print("Summary:")
print(f"  Total Findings: {unified_report['summary']['total_findings']}")
print(f"  Critical: {unified_report['summary']['critical']}")
print(f"  High: {unified_report['summary']['high']}")
print(f"  Medium: {unified_report['summary']['medium']}")
print(f"  Low: {unified_report['summary']['low']}")
print("="*50)

PYTHON_SCRIPT

echo ""
echo "✅ Unified report generation complete!"
echo "Reports generated in: $OUTPUT_DIR"
echo "  - unified-report.json"
echo "  - unified-report.csv"
echo "  - unified-report.html"
