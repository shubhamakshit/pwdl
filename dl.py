'''
base_url = "https://d26g5bnklkwsh4.cloudfront.net/8b267870-2dee-4372-8cce-6fe6ef35a27f/hls/720"

for i in range(1, 1066):
        # Use f-string to format the number with leading zeros
        n = f'{i:03}'
        t = base_url+"/"+str(n)+".ts"
        import os 
        os.system('wget '+t)
'''

import os
import sys
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from process import shell
import uuid 

'''def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f'Downloaded {filename}')
'''

def download_file(url,filename):
    os.system(f'aria2c {url}')

def dl(base_url, num_files):
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Use a list to store the futures
        futures = []

        for i in range(0, int(num_files)+1):
            n = f'{i:03}'
            file_url = f'{base_url}/{n}.ts'
            filename = f'{n}.ts'
            # Submit the download_file function to the executor
            futures.append(executor.submit(download_file, file_url, filename))

        # Wait for all futures to complete
        for future in futures:
            future.result()

def main():
    parser = argparse.ArgumentParser(description='Download files using multithreading.')
    parser.add_argument('base_url', help='Base URL for the files')
    parser.add_argument('num_files', type=int, help='Number of files to download')

    args = parser.parse_args()
    base_url = args.base_url
    dl(base_url,args.num_files)
    
if __name__ == '__main__':
    main()