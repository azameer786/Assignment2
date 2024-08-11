import os
import subprocess
import argparse
import sys

'''
OPS445 Assignment 2 - Winter 2022
Program: duim.py 
Author: "Student Name"
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: A script that uses the 'du' command to display disk usage of directories
             and generates a bar graph representation of disk space usage.

Date: 
'''

def call_du_sub(target_directory):
    """Calls 'du -d 1 <target_directory>' and returns a list of subdirectories with sizes."""
    try:
        result = subprocess.Popen(['du', '-d', '1', target_directory],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = result.communicate()
        output = output.decode().strip()
        lines = output.split('\n')
        return [line.split('\t')[1] for line in lines]
    except Exception as e:
        print(f"Error calling 'du': {e}")
        return []

def percent_to_graph(percent, total_chars):
    """Returns a bar graph string representing the given percentage with a specific length."""
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100")
    if total_chars <= 0:
        raise ValueError("Total chars must be a positive integer")
    
    filled_chars = int(round(percent / 100 * total_chars))
    empty_chars = total_chars - filled_chars
    return '=' * filled_chars + ' ' * empty_chars

def create_dir_dict(dir_list):
    """Converts a list of directories with sizes into a dictionary."""
    dir_dict = {}
    for line in dir_list:
        parts = line.split()
        if len(parts) == 2:
            size, path = parts
            try:
                size = int(size)
                dir_dict[path] = size
            except ValueError:
                print(f"Error parsing size '{size}' for path '{path}'")
    return dir_dict

def parse_command_args():
    """Parses command-line arguments and returns the arguments object."""
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts")
    parser.add_argument('target', nargs='?', default='.', help='The directory to scan.')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Print sizes in human readable format')
    parser.add_argument('-l', '--length', type=int, default=20, help='Specify the length of the graph. Default is 20.')
    return parser.parse_args()

def human_readable(size):
    """Converts a byte size to a human-readable format."""
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}P"

def main():
    args = parse_command_args()
    dir_list = call_du_sub(args.target)
    dir_dict = create_dir_dict(dir_list)
    
    if not dir_dict:
        print("No subdirectories found or error processing.")
        return
    
    total_size = sum(dir_dict.values())
    
    for directory, size in dir_dict.items():
        percent = (size / total_size) * 100
        graph = percent_to_graph(percent, args.length)
        size_str = human_readable(size) if args.human_readable else f"{size} bytes"
        print(f"{percent:3.0f} % [{graph}] {size_str} {directory}")

    print(f"Total: {human_readable(total_size)} \t{args.target}")

if __name__ == "__main__":
    main()
