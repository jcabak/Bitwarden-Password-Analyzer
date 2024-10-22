import csv
import os
import sys
from datetime import datetime

length_threshold = 14


def is_weak_password(password):
    if len(password) < length_threshold:
        return True
    return False

def save_to_txt(weak_passwords, output_file):
    with open(output_file, mode='w', encoding='utf-8') as file:
        for entry in weak_passwords:
            file.write(f"{entry['length']} - {entry['domain']} - {entry['username']} - {entry['password']}\n")

def save_to_html(weak_passwords, output_file, show_passwords=True):
    length_stats = {}
    for entry in weak_passwords:
        length = entry['length']
        length_stats[length] = length_stats.get(length, 0) + 1

    total_passwords = len(weak_passwords)
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, mode='w', encoding='utf-8') as file:
        file.write("<html>\n<head>\n<title>Weak Passwords Report</title>\n")
        file.write("<link rel='stylesheet' href='https://cdn.datatables.net/1.10.24/css/jquery.dataTables.min.css'>\n")
        file.write("<script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>\n")
        file.write("<script src='https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js'></script>\n")
        file.write("<script>\n$(document).ready(function() { $('#passwordTable').DataTable({\"pageLength\": 100}); });\n</script>\n")  # Show 100 entries
        file.write("</head>\n<body>\n")
        file.write(f"<h1>Weak Passwords Report (Generated on {report_time})</h1>\n")

        for length, count in sorted(length_stats.items()):
            file.write(f"Password {length}-character: {count}<br>\n")
        
        file.write("<table id='passwordTable' border='1'>\n")
        file.write("<thead>\n<tr>\n<th>Password Length</th>\n<th>Website</th>\n<th>Username</th>\n")
        
        if show_passwords:
            file.write("<th>Password</th>\n")
        
        file.write("</tr>\n</thead>\n<tbody>\n")

        for entry in weak_passwords:
            file.write(f"<tr>\n<td>{entry['length']}</td>\n")
            file.write(f"<td><a href='{entry['uri']}' target='_blank'>{entry['domain']}</a></td>\n")
            file.write(f"<td>{entry['username']}</td>\n")
            
            if show_passwords:
                file.write(f"<td>{entry['password']}</td>\n")
            
            file.write("</tr>\n")

        file.write("</tbody>\n</table>\n</body>\n</html>\n")

def analyze_csv_file(file_path, show_passwords=True):
    weak_passwords = []
    
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            password = row['login_password']
            if is_weak_password(password):
                domain = row['login_uri'].split("//")[-1].split("/")[0]
                weak_passwords.append({
                    'length': len(password),
                    'domain': domain,
                    'username': row['login_username'],
                    'password': password,
                    'uri': row['login_uri']
                })

    if weak_passwords:
        base_filename = os.path.splitext(os.path.basename(file_path))[0]
        txt_output = f"result_{base_filename}.txt"
        html_output = f"result_{base_filename}.html"

        save_to_txt(weak_passwords, txt_output)
        save_to_html(weak_passwords, html_output, show_passwords)

def analyze_directory(show_passwords=True):
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    
    for csv_file in csv_files:
        print(f"Analyzing {csv_file}...")
        analyze_csv_file(csv_file, show_passwords)

if __name__ == "__main__":
    show_passwords = True

    for arg in sys.argv[1:]:
        if arg.startswith('--length='):
            length_threshold = int(arg.split('=')[1])
        elif arg == '--no-passwords':
            show_passwords = False

    analyze_directory(show_passwords)
