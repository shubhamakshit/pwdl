# PW DOWNLOADER

## codename 'panther'
- version = **0.1A**
- development_name = **panther[0:1A]**

## Advantages
- Easy to use commandline
- Supports multi - video downloading
- Uses Multi Threading for blazing download speed

## Issues - to be fixed
- Only available for **linux** ( bash only )
- ~~requires aria2c to installed and on path [ will be replaced by requests library soon ]~~
- ~~cannot show download progress as of now [ will be fixed along with aria2c issue ]~~
- ~~requires ffmpeg to be installed and on path [ plans to create a auto-install script ]~~
- now download is via a csv file only [ will add an option for a single url through commandline ]
- no documentation or help

## Requirements
- `aria2c` (package name `aria2`) installed on PATH
- `ffmpeg` installed on PATH

```bash
#For Debian/Ubuntu users
sudo apt-get update -y
sudo apt-get install aria2 ffmpeg -y
```



## Usage 

- Requires a csv file of format
```csv
name, link
<name1>, <link1>
<name2>, <link2>
```
- Installation
```bash
#!/bin/bash 
git clone https://github.com/shubhamakshit/pwdl.git
cd pwdl/
python -m pip install requests argparse 
```
- Usage
```bash
python m3u8.py /path/to/file.csv
# alternate usage
export CSV_FILE="/path/to/file.csv"
python m3u8.py $CSV_FILE
```
