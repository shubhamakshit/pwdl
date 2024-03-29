from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter,Completer
from prompt_toolkit.history import FileHistory
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

def iswindows():
    return os.name == 'nt'
    
cprint("Essential Debugging")
glv.dprint(str(pf.prefs))
global FFMPEG_PATH
global tmp_dir
global script_location
global OUT_DIRECTORY

OUT_DIRECTORY = glv.OUT_DIRECTORY

script_location = f'{os.path.dirname(os.path.realpath(__file__))}'.replace('\\','/')
tmp_dir = f'{script_location}/tmp'.replace('\\','/')

FFMPEG_PATH = pf.ffmpeg_path()
if FFMPEG_PATH == None:
    print(f"no valid ffmpeg path in in {pf.PREF_FILE}\nExiting ...")
    exit(2)
if os.system('python -m ffpb -h') == 0 :
    FFMPEG_PATH = 'python -m ffpb'
print(f"FFMPEG PATH => {FFMPEG_PATH}")


# dl_script_location is required as files are still downloaded using bash command via shell()
dl_script_location = os.path.dirname(os.path.realpath(__file__)) + '/dl.py'

start_location =  str(os.getcwd()).replace('\\','/')
cprint('Initial steps performed') # DEBUG

def tmp_dir_check():
    try:
        if glv.vout: glv.dprint(f"tmp_dir {tmp_dir}")
        if not os.path.exists(f'{tmp_dir}') : os.system(f'mkdir "{tmp_dir}" ')
    except:
        glv.errprint(f"Failed to create directory {os.getcwd()}/tmp\nExiting...")
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
        #if glv.vout: glv.dprint(f"LOCATION : {(os.getcwd()).replace('\','/')}\n") #DEUBG
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

    if os.path.exists('./main.m3u8'): os.system('rm -f ./main.m3u8') if not iswindows() else os.system('del /F main.m3u8') # remove already existing m3u8 file
    if os.path.exists('./enc.key'):   os.system('rm -f ./enc.key')   if not iswindows() else os.system('del /F enc.key')# remove already existing key file


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
    if glv.vout: os.system('ls -l | grep \'enc\' ') if not iswindows() else os.system('dir | findstr "enc') #DEBUG
    if glv.vout: os.system('ls -l | grep \'m3u8\' ') if not iswindows() else os.system('dir | findstr "m3u8') #DEBUG

    #------------------------------------------------------------------------------------------
    # Convert to MP4 using ffmpeg
    cprint('Running ffmpeg (ffpb)')
    shell(f'{FFMPEG_PATH} -allowed_extensions ALL -y -i main.m3u8 -c copy {name}.mp4')
    #------------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------------
    # Cleanup
    os.system(f'rm -rf *.ts') if not iswindows() else os.system('del /S /Q *.ts') 
    #------------------------------------------------------------------------------------------



def main():
    global OUT_DIRECTORY
     
    

    


    parser = argparse.ArgumentParser(description='PhysicsWallah M3u8 parser.')
    parser.add_argument('--csv-file', type=str, help='Input csv file. Legacy Support too.')
    parser.add_argument('--url', type=str, help='M3U8 URL for single usage. Incompatible with --csv-file.   Must be used with --name')
    parser.add_argument('--name', type=str, help='Name for the output file. Incompatible with --csv-file.   Must be used with --url')
    parser.add_argument('--dir', type=str, help='Output Directory')
    parser.add_argument('--verbose',action='store_true',help='Verbose Output')
    args = parser.parse_args()

    # user_input is given prefernce i.e if --verbose is true it will override
    # however if --verbose is false but pf.prefs['verbose'] is true 
    glv.vout = args.verbose
    
    if not glv.vout and pf.prefs['verbose'] : glv.vout = pf.prefs['verbose']


    # cleaning unnecessary debug info 
    if not glv.vout: clear()
    
    if args.dir:
        
        OUT_DIRECTORY = os.path.abspath(args.dir)
        if glv.vout: glv.dprint(OUT_DIRECTORY)

    #if both csv file and (url or name) is provided then -> exit with error code 3
    if args.csv_file and ( args.url or args.name):
        print("Both csv file and url (or name) is provided. Unable to decide. Aborting! ...")
        sys.exit(3)

    # handle in case --csv-file is provided
    if args.csv_file:
        csv_m3u8(args.csv_file)

    # handle in case url and name is given 
    elif args.url and args.name:
        m3u8_module(args.name, args.url)
    
    # in case neither is used 
    else:
        # Warning as pwdl-console is still not complete
        if not pf.prefs['supress_warn']: glv.dprint("Console still under development")
        def add_command(args):
            """Adds a name and URL to a list or performs other actions as needed."""
            name = args[0]
            url = args[1]
            if glv.vout: glv.dprint(f"Adding {name} with URL {url} to the downlaod.")
            m3u8_module(name,url)
            # You can add the name and URL to a list or perform other actions here

        commands = {
            # "add": [re.compile(r"add\s+([\w-]+)\s+(\S+)"), add_command],
            "add_help":[
                re.compile(r"add\s+(\-h|\-\-help)[ ]*"),
                lambda x: print("add\nFunction: Download Videos via url\nUsage:\tadd <name> <url>")
            ],
            "add": [
                re.compile(r"add\s+([\w-]+)\s+(\S+)"), add_command,  # Enclose in parentheses
            ],
            "clear":[re.compile(r"(cls|clear)[ ]*"),lambda x : clear()],
            
            #  bash command has yet to be designed
            # "bash":[re.compile(r"bash[ ]*[A-Za-z0-9\-\$]*"),lambda x:shell(" ".join(x))]

            }

        
        history = FileHistory(".pwdl_history")

        while True:

            command = prompt("\n|PWDL|>", history=history)

            if command.strip() == 'exit' : sys.exit(0)

            for command_name, (regex, function) in commands.items():
                match = regex.match(command)
                if match:
                    function(match.groups())
                    break
            else:
                print("Invalid command.")

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
                m3u8_module(name,link)
            except Exception as e:
                glv.errprint(f"Error Processing {name} with link:{link}")
                glv.errprint(f"Exception trace,{e}")

def m3u8_module(name,link):
    tmp_dir_check()
    final_path = OUT_DIRECTORY
  
    from parsev2 import sudo_link as get_id
    if glv.vout: print(f'link before parsing {link}')
    process_link(name, get_id(link))
  

    if glv.vout: glv.dprint(f'Attempting to move ./{name}.mp4')
    if glv.vout: glv.dprint(f'OUT_DIRECTORY {final_path}')
    if glv.vout: glv.dprint(f"Current Directory contents")
    if glv.vout: os.system('ls -l') if not iswindows() else os.system('dir')

    glv.setDebug() # set debug => True
    # checks if file moved (that is all operations done)
    
    move_exit_code = shell(f'mv {"-v" if glv.vout else ""} ./{name}.mp4 {final_path}') if not iswindows() else 0
    if move_exit_code == 0:
        glv.reset()
        cprint(f"Done! {name}.mp4")
    else:
        print(f"Error in moving {name}.mp4")
    
    if iswindows():
        try:
            shutil.move(os.path.join(os.getcwd(), f'{name}.mp4'), os.path.join(final_path, f'{name}.mp4'))
            if glv.vout: glv.dprint(f"Successfully Transferred {name}.mp4 to {final_path}")
        except Exception as e:
            print(f"Error in moving {name}.mp4\nException trace -> {e}")

    #------------------------------------------------------------------------------------------
    #Cleanup
    os.chdir(start_location)
    os.system(f'rm  -rf {tmp_dir}') if not iswindows() else os.system('rmdir /s /q '+tmp_dir.replace('/','\\')+'  > NUL')
    #------------------------------------------------------------------------------------------
    #Cleanup of ,m3u8 and .enc files 
    os.system(f'rm -rf *.m3u8') if not iswindows() else os.system('del /s /q *.m3u8')
    os.system(f'rm -rf *.enc') if not iswindows() else os.system('del /s /q *.enc')
    cprint("Cleanup-successful")
    #-----------------------------------------------------------------------------------------
    return final_path + f"/.{name}.mp4"

if __name__ == "__main__":
    main()
    glv.reset()

