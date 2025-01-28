import os
import re
import pandas as pd
from jinja2 import Template

def parse_rpm_file(file_path):
    """Parse the RPM file and return a dictionary with package names and versions."""
    package_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(r"^(\S+)-(\d+[^\s]*)\s", line)
            if match:
                package_name = match.group(1)
                version = match.group(2)
                package_data[package_name] = version
    return package_data

def compare_packages(node1_data, node2_data):
    """Compare the packages from two nodes and return a sorted DataFrame."""
    all_packages = set(node1_data.keys()).union(node2_data.keys())

    comparison = []
    for pkg in all_packages:
        version1 = node1_data.get(pkg, 'Absent')
        version2 = node2_data.get(pkg, 'Absent')

        if version1 == 'Absent' or version2 == 'Absent':
            status = 'Absent'
        elif version1 != version2:
            status = 'Different'
        else:
            status = 'Same'

        comparison.append({
            'Package': pkg,
            'Node1_Version': version1,
            'Node2_Version': version2,
            'Result': status
        })

    # Sort by 'Result' to have Absent and Different first
    comparison.sort(key=lambda x: (x['Result'] != 'Absent', x['Result'] != 'Different', x['Package']))
    return pd.DataFrame(comparison)

def generate_html_report(dataframe, output_file):
    """Generate an HTML report using the comparison DataFrame."""
    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Package Comparison Report</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .Absent {
                background-color: #ffcccc;
            }
            .Different {
                background-color: #ffeb99;
            }
            .Same {
                background-color: #ccffcc;
            }
        </style>
    </head>
    <body>
        <h1>Package Comparison Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Package</th>
                    <th>Node1 Version</th>
                    <th>Node2 Version</th>
                    <th>Result</th>
                </tr>
            </thead>
            <tbody>
                {% for row in rows %}
                <tr class="{{ row['Result'] }}">
                    <td>{{ row['Package'] }}</td>
                    <td>{{ row['Node1_Version'] }}</td>
                    <td>{{ row['Node2_Version'] }}</td>
                    <td>{{ row['Result'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """)

    with open(output_file, 'w') as f:
        f.write(template.render(rows=dataframe.to_dict(orient='records')))

def main():
    node1_file = input("Enter the path to the first node's package file: ").strip()
    node2_file = input("Enter the path to the second node's package file: ").strip()

    if not os.path.exists(node1_file) or not os.path.exists(node2_file):
        print("Error: One or both files do not exist.")
        return

    node1_data = parse_rpm_file(node1_file)
    node2_data = parse_rpm_file(node2_file)

    comparison_df = compare_packages(node1_data, node2_data)

    output_file = "package_comparison_report.html"
    generate_html_report(comparison_df, output_file)

    print(f"HTML report generated: {output_file}")

if __name__ == "__main__":
    main()
