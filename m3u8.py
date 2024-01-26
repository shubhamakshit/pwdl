import requests
import os
import shutil
import csv
from process import shell
import argparse
import re
import sys
import parse_pref as pf 

global FFMPEG_PATH

FFMPEG_PATH = pf.ffmpeg_path()
if FFMPEG_PATH == None:
    print(f"no valid ffmpeg path in in {pf.PREF_FILE}\nExiting ...")
    exit(2)
print(f"FFMPEG PATH => {FFMPEG_PATH}")

try:
    from urllib.parse import urlparse
except ImportError:
    shell('pip install urllib')

try:
    if not os.path.exists('./tmp') : os.system('mkdir ./tmp')
except:
    print(f"Failed to create directory {os.getcws()}/tmp\nExiting...")
    exit(-2)

# dl_script_location is required as files are still downloaded using bash command via shell()
dl_script_location = os.path.dirname(os.path.realpath(__file__)) + '/dl.py'

start_location =  str(os.getcwd())
print('ENTERED M3u8 DOWNLOADER ORIGINAL SCRIPT') # DEBUG

def download_m3u8(url):
    print(f"URL at download m3u8 = {url}")
    shell(f'aria2c {url}')

def extract_last_segment_number(m3u8_content):
    return m3u8_content.split('\n')[m3u8_content.split('\n').index('#EXT-X-ENDLIST')-1].split('.')[0]

def replace_api_penpencil_url(m3u8_content):

        sys.stderr.write(f"DEBUGGING AT replace_api_penpencil_url()\n") # DEBUG
        sys.stderr.write(f"LOCATION : {os.getcwd()}\n") #DEUBG
        #
        # sys.stderr.write(f"AT replace_api_penpencil_url():\n content: {m3u8_content}") #debug
        #
        
        input_string = m3u8_content # Your input string

        #------------------------------------------------------------------------------------------
        # Define the regex pattern
        regex_pattern = r'https:\/\/api\.penpencil\.(co|xyz)\/v1\/videos\/get-hls-key\?videoKey[A-Za-z0-9&=.-]*'
        


        # Find the match using re.search
        match = re.search(regex_pattern, input_string)
        
        #------------------------------------------------------------------------------------------


        #------------------------------------------------------------------------------------------
        # Check if a match is found
        if match:
            # Store the matched string in a variable
            url_original = match.group(0)

            # Replace the matched string with 'enc.key'
            m3u8_content = re.sub(regex_pattern, 'enc.key', input_string)
        #------------------------------------------------------------------------------------------
        else:
            sys.stderr.write("NO MATCH FOUND AT replace_api_penpencil_url()") #debug

        #return modified m3u8 content
        return [m3u8_content, url_original]


def process_link(name, link,_id=None):
    print(f"\nProcessing link: {name}")

    if os.path.exists('./main.m3u8'): os.system('rm -f ./main.m3u8') # remove already existing m3u8 file
    if os.path.exists('./enc.key'):   os.system('rm -f ./enc.key')   # remove already existing key file


    download_m3u8(link)
    with open('main.m3u8','r') as mfile:
        m3u8_content = mfile.read()

        #print(m3u8_content) # DEBUG

        last_segment_number = extract_last_segment_number(m3u8_content)

        # replace_api_penpencil_url() returns a list with
        #   [0] = m3u8 content
        #   [1] = enc.key url
        # storing enc.key url for future use

        changed_m3u8_data = replace_api_penpencil_url(m3u8_content)

        m3u8_content = changed_m3u8_data[0]
        enc_url = changed_m3u8_data[1]







    #Downloading files via ' dl.py '----------------------------------------------------------
        print("Starting Download!")

    #------------------------------------------------------------------------------------------
    # _id is the name of folder in /tmp where the files are downloaded
    import uuid
    if _id == None: _id = str(uuid.uuid4())

    if os.path.exists(f'./tmp/{_id}'): os.system(f'rm -rf ./tmp/{_id}')
    os.mkdir(f'./tmp/{_id}')
    os.chdir(f'./tmp/{_id}')
    #------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------

    trimmed_link = link.replace('/main.m3u8','')

    shell(f"python {dl_script_location} {trimmed_link} {last_segment_number}")

    print("\nDownloaded files!")
    #---------------------------------------------------------------------------cd---------------


    #------------------------------------------------------------------------------------------
    #changing directory to /tmp/<_id>
    try:
        os.chdir(f'./tmp/{_id}')
    except Exception as e:
        print(f"Error when changing directory to /tmp/{_id}")
        print(e)


    print("SUCCESSFULLY CHANGED DIRECTORY to "+ os.getcwd()) #DEBUG
    #------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------
    #performing file operations within /tmp/<_id> folder

    # m3u8 file
    with open('main.m3u8','w+') as m3u8_file:
        m3u8_file.write(m3u8_content)

    # downloading enc.key
    shell(f'aria2c {enc_url} ')
    #------------------------------------------------------------------------------------------



    os.system('ls -l | grep \'enc\' ') #DEBUG
    os.system('ls -l | grep \'m3u8\' ') #DEBUG

    #------------------------------------------------------------------------------------------
    # Convert to MP4 using ffmpeg
    sys.stderr.write('Attempting to run ffmpeg command using shell() defined in process.py ')
    shell(f'{FFMPEG_PATH} -allowed_extensions ALL -y -i main.m3u8 -c copy {name}.mp4')
    #------------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------------
    # Cleanup
    os.system(f'rm -rf *.ts')
    #------------------------------------------------------------------------------------------



def main():
    parser = argparse.ArgumentParser(description='PhysicsWallah M3u8 parser.')
    parser.add_argument('csv_file', type=str, help='CSV FILE')
    args = parser.parse_args()


    m3u8(args.csv_file)

def m3u8(csv_file):
     # Read links from CSV file
     with open(csv_file, 'r') as file:
         reader = csv.reader(file)
         next(reader)  # Skip header row
         for row in reader:
             name, link = row
             #checking if ./<name> exists
             # if os.path.exists(f'./{name}'):
             #     pass #default value is overwrite
             # else:
             #     os.mkdir(f'./{name}')
             final_path = str( os.getcwd() )

             from parsev2 import sudo_link as get_id

             print(f'link before parsing {link}')

             process_link(name, get_id(link))

             tmp_dir = str(os.getcwd())

             os.system(f'mv ./{name}.mp4 {final_path}')

             #------------------------------------------------------------------------------------------
             #Cleanup
             os.chdir(start_location)
             os.system(f'rm -rf {tmp_dir}')
             #------------------------------------------------------------------------------------------
             #Cleanup of ,m3u8 and .enc files 
             os.system(f'rm -rf *.m3u8')
             os.system(f'rm -rf *.enc')
             #-----------------------------------------------------------------------------------------
         return final_path + f"/.{name}.mp4"

           


if __name__ == "__main__":
    main()

