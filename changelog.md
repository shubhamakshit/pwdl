# panther [0:1]

inherited from original project 'PWDL-WEBUI' which used flask 
the download process was then made 

panther[0:1] edited the original files to suit commandline usage

## Issues - to be fixed
 - Only available for linux ( bash only )
 - requires aria2c to installed and on path [ will be replaced by requests library soon ] --> fixed in `panther[0.1A]`
 - cannot show download progress as of now [ will be fixed along with aria2c issue ] --> fixed in `panther[0.1A]`
 - requires ffmpeg to be installed and on path [ plans to create a auto-install script ] --> fixed in `panther[0.1A]`
 - now download is via a csv file only [ will add an option for a single url through commandline ] --> fixed in `panther[0.1A]`
 - no documentation or help

# panther[0:1A]

## Issues fixed 
 - aria2c dependency removed
 - download progress now effectively shown
 - fixed a not known issue whereby you cannot use m3u8.py from folders other than script-folder
## Updates 
 - now uses tqdm to show download progress
 - added support for external ffmpeg (yet to be tested)
 - added --dir flag to change output directory 
 - added --url & --name to specify input via cli directly [SUPPORTS ONLY SINGLE URL NOW]
 - 


