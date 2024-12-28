import argparse
import glob
import os
import zipfile
import time
from datetime import datetime
from multiprocessing import Process

def delete_oldest(folder_path, max_files):
    zip_files = glob.glob(os.path.join(folder_path, '*.zip'))
    while len(zip_files) > max_files:
        zip_files.sort(key=os.path.getmtime)
        oldest_file = zip_files[0]
        try:
            os.remove(oldest_file)
            print(f"Deleted: {oldest_file}")
        except OSError as e:
            print(f"Error deleting {oldest_file}: {e}")
        zip_files = glob.glob(os.path.join(folder_path, '*.zip'))

def make_zipfile(output_filename, source_dir):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    print(f"Creating ZIP file: {output_filename}")
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            zipf.write(root, os.path.relpath(root, relroot))
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zipf.write(file_path, arcname)
    print(f"ZIP file created: {output_filename}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, default="default")
    parser.add_argument('time', type=float, default=300)
    args = parser.parse_args()

    max_files = 15
    output_dir = "/output"
    input_dir = "/input"

    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        output_filename = f"{timestamp}_{args.name}.zip"
        output_path = os.path.join(output_dir, output_filename)

        p1 = Process(target=make_zipfile, args=(output_path, input_dir))
        p1.start()

        zip_files = glob.glob(os.path.join(output_dir, '*.zip'))
        if len(zip_files) > max_files:
            p2 = Process(target=delete_oldest, args=(output_dir, max_files))
            p2.start()

        time.sleep(args.time)

if __name__ == '__main__':
    main()