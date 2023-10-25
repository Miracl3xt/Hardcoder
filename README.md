# Hardcoder
This tool is designed to find hardcoded secrets in Source code, Logs, or local files. Lightweight, Multithreaded tool to find Secrets, sensitive data in your day to day life

Uses:
Regex Based Search engine
Searching for logs for Sensitive data made Easy
Direct Local file scanner
Find Hardcoded credentials in your SAST, Source code, and LOGS.

CMD:
python3 Securefind.py --json Rules.json --directory sendy/

--json : Include Youre rules.json file here
--Directory: PATH to your local Source code directory.

Also, you can Modify Rules.json according to your regexes
