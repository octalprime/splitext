import os
import sys
from tqdm import tqdm
import concurrent.futures

def split_file_part(args):
    file_path, lines, part = args
    print(f"Processing part {part}")
    with open(f'{file_path}_{part}', 'w') as f:
        for line in lines:
            f.write(line)
    print(f"Finished part {part}")

def split_file(file_path, parts):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines_per_part = len(lines) // parts
    if len(lines) % parts:
        parts += 1  # Add extra part for the remaining lines
    print(f"Splitting {file_path} into {parts} parts")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for part in range(parts):
            start = part * lines_per_part
            end = start + lines_per_part if part != parts - 1 else None  # Last part includes the remaining lines
            futures.append(executor.submit(split_file_part, (file_path, lines[start:end], part)))
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Raise exception if any occurred

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python split_file.py <file_path> <parts>")
        sys.exit(1)
    file_path = sys.argv[1]
    parts = int(sys.argv[2])
    split_file(file_path, parts)
