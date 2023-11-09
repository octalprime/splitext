import sys
from tqdm import tqdm

def split_file(file_path, size_limit):
    file_size = os.path.getsize(file_path)
    with open(file_path, 'r') as large_file:
        count = 0
        output_file = None
        for line in tqdm(large_file, total=file_size, unit='B', unit_scale=True, unit_divisor=1024):
            if output_file is None or output_file.tell() + len(line) > size_limit:
                if output_file is not None:
                    output_file.close()
                count += 1
                output_file = open(f'split_file_{count}.txt', 'w')
            output_file.write(line)
        if output_file is not None:
            output_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_file.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    split_file(file_path, 500*1024*1024)  # 500MB
