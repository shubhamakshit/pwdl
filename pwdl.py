import requests
import os
import shutil
import csv
from process import shell
import argparse
import re
import sys
import parse_pref as pf 
import requests
import glv

def cprint(msg,success=True):
    if success: glv.setSuccess()
    format_text = '{:-^'+str(shutil.get_terminal_size().columns)+"}"
    sys.stdout.write(format_text.format(msg))
    glv.reset()

def clear():
    if not os.system('cls')  == 0:
        os.system('clear')

    
cprint("Essential Debugging")
global FFMPEG_PATH
global tmp_dir
global script_location
global OUT_DIRECTORY

OUT_DIRECTORY = str(os.getcwd())
script_location = f'{os.path.dirname(os.path.realpath(__file__))}'
tmp_dir = f'{script_location}/tmp'

FFMPEG_PATH = pf.ffmpeg_path()
if FFMPEG_PATH == None:
    print(f"no valid ffmpeg path in in {pf.PREF_FILE}\nExiting ...")
    exit(2)
if FFMPEG_PATH.endswith('ffmpeg'):
    FFMPEG_PATH = FFMPEG_PATH[:-6] + "ffpb"
print(f"FFMPEG PATH => {FFMPEG_PATH}")


# dl_script_location is required as files are still downloaded using bash command via shell()
dl_script_location = os.path.dirname(os.path.realpath(__file__)) + '/dl.py'

start_location =  str(os.getcwd())
cprint('Initial steps performed') # DEBUG

def tmp_dir_check():
    try:
        if not os.path.exists(f'{tmp_dir}') : os.system(f'mkdir {tmp_dir}')
    except:
        print(f"Failed to create directory {os.getcws()}/tmp\nExiting...")
        exit(-2)


def download_file(url, filename=None):
    if filename is None:
        filename = url.split('/')[-1]

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)

    return filename


def download_m3u8(url):
    if glv.vout : glv.dprint(f"URL at download m3u8 = {url}")
    # shell(f'aria2c {url}') #legacy method
    download_file(url)

def extract_last_segment_number(m3u8_content):
    return m3u8_content.split('\n')[m3u8_content.split('\n').index('#EXT-X-ENDLIST')-1].split('.')[0]

def replace_api_penpencil_url(m3u8_content):

        if glv.vout: glv.dprint(f"DEBUGGING AT replace_api_penpencil_url()\n") # DEBUG
        if glv.vout: glv.dprint(f"LOCATION : {os.getcwd()}\n") #DEUBG
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
    print(f"\t\tProcessing file-name: {name}")

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
        cprint("Starting Download!")
        cprint("Please Wait")
    #------------------------------------------------------------------------------------------
    # _id is the name of folder in /tmp where the files are downloaded
    import uuid
    if _id == None: _id = str(uuid.uuid4())

    if os.path.exists(f'{tmp_dir}/{_id}'): os.system(f'rm -rf {tmp_dir}/{_id}')
    os.mkdir(f'{tmp_dir}/{_id}')
    os.chdir(f'{tmp_dir}/{_id}')
    #------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------

    trimmed_link = link.replace('/main.m3u8','')

    shell(f"python {dl_script_location} {trimmed_link} {last_segment_number}")

    cprint("Downloaded files!")
    #---------------------------------------------------------------------------cd---------------


    #------------------------------------------------------------------------------------------
    #changing directory to /tmp/<_id>
    try:
        os.chdir(f'{tmp_dir}/{_id}')
    except Exception as e:
        print(f"Error when changing directory to {tmp_dir}/{_id}")
        print(e)


    if glv.vout: glv.dprint("Successfully changed directory to "+ os.getcwd()) #DEBUG
    #------------------------------------------------------------------------------------------


    #------------------------------------------------------------------------------------------
    #performing file operations within /tmp/<_id> folder

    # m3u8 file
    with open('main.m3u8','w+') as m3u8_file:
        m3u8_file.write(m3u8_content)

    # downloading enc.key
    #shell(f'aria2c {enc_url} ') #legacy method
    download_file(enc_url,"enc.key")
    #------------------------------------------------------------------------------------------


    if glv.vout: glv.dprint("enc.key and m3u8 status")
    if glv.vout: os.system('ls -l | grep \'enc\' ') #DEBUG
    if glv.vout: os.system('ls -l | grep \'m3u8\' ') #DEBUG

    #------------------------------------------------------------------------------------------
    # Convert to MP4 using ffmpeg
    cprint('Running ffmpeg (ffpb)')
    shell(f'{FFMPEG_PATH} -allowed_extensions ALL -y -i main.m3u8 -c copy {name}.mp4')
    #------------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------------
    # Cleanup
    os.system(f'rm -rf *.ts')
    #------------------------------------------------------------------------------------------



def main():
    global OUT_DIRECTORY
     
    

    glv.vout = False


    parser = argparse.ArgumentParser(description='PhysicsWallah M3u8 parser.')
    parser.add_argument('--csv-file', type=str, help='Input csv file. Legacy Support too.')
    parser.add_argument('--url', type=str, help='M3U8 URL for single usage. Incompatible with --csv-file.   Must be used with --name')
    parser.add_argument('--name', type=str, help='Name for the output file. Incompatible with --csv-file.   Must be used with --url')
    parser.add_argument('--dir', type=str, help='Output Directory')
    parser.add_argument('--verbose',action='store_true',help='Verbose Output')
    args = parser.parse_args()

    glv.vout = args.verbose
    
    # cleaning unnecessary debug info 
    clear()
    
    if args.dir:
        OUT_DIRECTORY = args.dir
        if glv.vout: glv.dprint(OUT_DIRECTORY)
    
    if args.csv_file and ( args.url or args.name):
        print("Both csv file and url (or name) is provided. Unable to decide. Aborting! ...")
        exit(3)

    if args.csv_file:
        csv_m3u8(args.csv_file)

    elif args.url and args.name:
        m3u8_module(args.name, args.url)
    else:
        print("Invalid usage. Use either --csv_file or --url with --name.")
        parser.print_help()

    #m3u8(args.csv_file)

def csv_m3u8(csv_file):
     # Read links from CSV file
     with open(csv_file, 'r') as file:
        
        data = file.read().split('\n')
        count = 0
        for line in data:

            # Skip header row
            if count == 0:
                count = 1
                continue

            line_content = line.split(',')

            #Skips unwanted conditions 
            if not line.strip() or len(line_content) != 2: continue

            name = line_content[0]
            link = line_content[1]

            try:
                tmp_dir_check()
                m3u8_module(name,link)
            except Exception as e:
                glv.errprint(f"Error Processing {name} with link:{link}")
                glv.errprint(f"Exception trace,{e}")

def m3u8_module(name,link):

    final_path = OUT_DIRECTORY
  
    from parsev2 import sudo_link as get_id
    if glv.vout: print(f'link before parsing {link}')
    process_link(name, get_id(link))
  

    if glv.vout: glv.dprint(f'Attempting to move ./{name}.mp4')
    if glv.vout: glv.dprint(f'OUT_DIRECTORY {final_path}')
    if glv.vout: glv.dprint(f"Current Directory contents")
    if glv.vout: os.system('ls -l')

    glv.setDebug() # set debug => True
    # checks if file moved (that is all operations done)
    if shell(f'mv {"-v" if glv.vout else ""} ./{name}.mp4 {final_path}') == 0:
        glv.reset()
        cprint(f"Done! {name}.mp4")
    else:
        print(f"Error in moving {name}.mp4")
       
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
    

