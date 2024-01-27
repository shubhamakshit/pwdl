import re
import sys
import glv


def sudo_link(link):
    if glv.vout: glv.dprint(f"AT PARSEV2 received link {link}") #debug
    regex = r"[0-9a-z]{8}-[0-9a-z]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
    #tQest_str = "https://d1d34p8vz63oiq.cloudfront.net/5fa96c14-d286-429e-a05d9f48a2428a0b/dash/480/246.mp"

    match = re.search(regex, link)

    if match:
        
        link = f"https://{glv.SUDO_KEY}.cloudfront.net/{str(match.group())}/hls/720/main.m3u8"
        if glv.vout: glv.dprint(f'Link after running through parsev2 {link}')
        return link

        # No need to iterate over groups if there's only one match
    else:
        glv.errprint("No match found at 'sudo_link'.\nReturning -1 ...")
        return '-1'

def sanitize_file_name(input_string):
    # Replace spaces with underscores
    sanitized_string = input_string.replace(' ', '_')
    
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    sanitized_string = re.sub(r'[^a-zA-Z0-9_\-]', '', sanitized_string)
    
    # You may want to limit the length of the file name to a reasonable size
    max_length = 255  # You can adjust this based on your requirements
    sanitized_string = sanitized_string[:max_length]
    
    return sanitized_string

def get_id_like_string(input_string):
    regex = r"[0-9a-z]{8}-[0-9a-z]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"
    match = re.search(regex, input_string)
    if match:
        return str(match.group())
        # No need to iterate over groups if there's only one match
    else:
        glv.errprint("No match found\n")
        return '-1'
