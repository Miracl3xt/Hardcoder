import os
import re
import json
import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import partial

# Define ANSI escape codes for colors
RED = "\033[91m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Define command-line arguments
parser = argparse.ArgumentParser(description="Search for patterns in files using a JSON file")
parser.add_argument("--json", required=True, help="Path to the JSON file containing patterns")
parser.add_argument("--directory", required=True, help="Directory to search for files")
args = parser.parse_args()

# Validate and load the JSON data from the specified file
try:
    with open(args.json, 'r') as json_file:
        json_content = json.load(json_file)
except FileNotFoundError:
    print(f"JSON file not found: {args.json}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
    exit(1)

# Compile regex patterns
compiled_patterns = {key: re.compile(pattern) for key, pattern in json_content.items()}
#print(compiled_patterns)

# Function to search for the pattern in a file and print results with colored text
def search_file_for_patterns(file_path, patterns):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.readlines()
        results = []
        for line_number, line in enumerate(content, 1):
            for key, pattern in patterns.items():
                matches = pattern.finditer(line)
                for match in matches:
                    result = (
                        f'{YELLOW}File:{file_path}{RESET}- '
                        f'{RED}Line:{line_number}{RESET}- '
                        f'{BLUE}Key: {key} {RESET}: {GREEN}{match.group()}{RESET}'
                    )
                    results.append(result)
        return results

# Define allowed file extensions
allowed_extensions = {'.php', '.asp', '.html', '.js', '.txt', '.md', '.pem', '.log','.json'}

def process_directory(root, files, patterns):
    for file in files:
        if file.endswith(tuple(allowed_extensions)):
            file_path = os.path.join(root, file)
            results = search_file_for_patterns(file_path, patterns)
            for result in results:
                print(result)

if __name__ == '__main__':
    # Set the number of processes to a range of 10-20
    min_workers = 10
    max_workers = 20
    num_workers = min(max_workers, max(min_workers, os.cpu_count() or 1))
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for root, dirs, files in os.walk(args.directory):
            executor.submit(process_directory, root, files, compiled_patterns)
