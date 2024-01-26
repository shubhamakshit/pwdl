import os
import sys
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def download_file(url, filename, progress_bar):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        with open(filename, 'wb') as file:
            for data in response.iter_content(chunk_size=block_size):
                file.write(data)

        progress_bar.update(1)
    except Exception as e:
        print(f'Error downloading {filename}: {e}')

def dl(base_url, num_files):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        progress_bar = tqdm(total=num_files, desc='Overall Progress')

        for i in range(1, num_files + 1):
            n = f'{i:03}'
            file_url = f'{base_url}/{n}.ts'
            filename = f'{n}.ts'
            futures.append(executor.submit(download_file, file_url, filename, progress_bar))

        for future in futures:
            future.result()

        progress_bar.close()

def main():
    parser = argparse.ArgumentParser(description='Download files using multithreading.')
    parser.add_argument('base_url', help='Base URL for the files')
    parser.add_argument('num_files', type=int, help='Number of files to download')

    args = parser.parse_args()
    base_url = args.base_url
    dl(base_url, args.num_files)

if __name__ == '__main__':
    main()
