import os
import shutil

__FFMPEG_PATH__ = "PATH"
PREF_FILE = f"{os.path.dirname(os.path.realpath(__file__))}/user.pref"

prefs = {
    "ffmpeg" : "PATH",
    "verbose": False
}

def remove_quotes(input_str):
    """
    Remove single and double quotes from both ends of a string.

    Parameters:
    - input_str (str): The input string.

    Returns:
    - str: The string with quotes removed.
    """
    if len(input_str) >= 2 and input_str[0] == input_str[-1] and input_str[0] in ('"', "'"):
        return input_str[1:-1]
    else:
        return input_str



def __find_ffmpeg_path__():
    # Search for ffmpeg executable in the system's PATH
    ffmpeg_path = shutil.which('ffmpeg')

    if ffmpeg_path:
        print(f'ffmpeg found at: {ffmpeg_path}')
        return ffmpeg_path
    else:
        print('ffmpeg not found in PATH. Make sure it is installed.')
        return None


try:
    line_number = 0 
    with open(PREF_FILE,'r') as pref:
        data = pref.read()
        for line in data.split('\n'):
            line_number += 1

            if not line:
                print(f"Empty data at {line_number}")
                continue

            if line.strip().startswith("#"):continue    

            line_data = line.split('=')
            if not len(line_data) == 2:
                print(f'Data at {line_number} is neither valid nor comment\nSkipping..')
                continue
            
            name  = line_data[0].strip()
            value = remove_quotes(line_data[1])

            
            if name == "ffmpeg":
                print(f"FFMPEG PATH at pf => {line_data[1]}")
                prefs['ffmpeg'] = value
            
            elif name == "verbose":
                if value.lower() == "true": prefs['verbose'] = True
                else : prefs['verbose'] = False
                


except Exception as e:
    print(f'Cannot read {PREF_FILE}\nExiting ...')
    print(f'Error {e}')
    exit(1)

def ffmpeg_path():
    print(f'Global variable FFMPEG_PATH value at ffmpeg_path() in pf => {__FFMPEG_PATH__}')
    if prefs['ffmpeg'] == "PATH" : return __find_ffmpeg_path__()
    return prefs['ffmpeg']
