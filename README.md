# Password Weakness Analyzer

This Python script analyzes passwords from a CSV export of Bitwarden (or similar password managers) and reports weak passwords based on length and complexity criteria. It generates both a `.txt` and an `.html` report for easier viewing and analysis.

Unlike Bitwarden's premium Weak Passwords Analyzer, this open-source script allows you to easily analyze and report weak passwords from your exported CSV files without any cost.

## Features

- Detects weak passwords based on a user-defined length threshold.
- Allows hiding the password column in the HTML report.
- Generates statistics on the number of weak passwords by their length.
- The HTML report includes sortable tables for easier analysis.
- The website URLs are clickable and open in a new window.

## Requirements

- Python 3.x

## How to Use

1. Place your Bitwarden CSV export in the same directory as the script (`analyze_passwords.py`).
2. Run the script using Python:

    ```bash
    python analyze_passwords.py
    ```

By default, passwords shorter than 14 characters will be considered weak.

### Command-line Options

- `--length=<value>`: Set a custom threshold for password length. For example:

    ```bash
    python analyze_passwords.py --length=16
    ```

    This will consider passwords shorter than 16 characters as weak.

- `--no-passwords`: Hide the "Password" column in the HTML report. For example:

    ```bash
    python analyze_passwords.py --no-passwords
    ```

## Output

- `result_<filename>.txt`: A text report with weak passwords in the format:

`password length` - `domain` - `username` - `password`
  
- `result_<filename>.html`: An HTML report with a sortable table. URLs in the "Website" column are clickable and open in a new window.

## Example

If you run the script with the following command:

```bash
python analyze_passwords.py --length=14 --no-passwords
```
