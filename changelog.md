# panther [0:1]

inherited from original project 'PWDL-WEBUI' which used flask 
the download process was then made 

panther[0:1] edited the original files to suit commandline usage

## Issues - to be fixed
 - Only available for linux ( bash only )
 - requires aria2c to installed and on path [ will be replaced by requests library soon ]
 - cannot show download progress as of now [ will be fixed along with aria2c issue ]
 - requires ffmpeg to be installed and on path [ plans to create a auto-install script ]
 - now download is via a csv file only [ will add an option for a single url through commandline ]
 - no documentation or help

# panther[0:1A]

## Issues fixed 
 - aria2c dependency removed
 - download progress now effectively shown

## Updates 
 - now uses tqdm to show download progress


