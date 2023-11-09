import os
import sys
from tqdm import tqdm
import concurrent.futures

def split_file_part(args):
    file_path, start, size, part = args
    print(f"Processing part {part}")
    with open(file_path, 'r') as f:
        f.seek(start)
        data = f.read(size)
    with open(f'{file_path}_{part}', 'w') as f:
        f.write(data)
    print(f"Finished part {part}")

def split_file(file_path, size_limit):
    file_size = os.path.getsize(file_path)
    parts = file_size // size_limit
    if file_size % size_limit:
        parts += 1  # Add extra part for the remaining data
    print(f"Splitting {file_path} into {parts} parts")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for part in range(parts):
            start = part * size_limit
            size = min(size_limit, file_size - start)
            futures.append(executor.submit(split_file_part, (file_path, start, size, part)))
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Raise exception if any occurred

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_file.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    split_file(file_path, 500*1024*1024)  # 500MB
