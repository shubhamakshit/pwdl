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
- ~~now download is via a csv file only [ will add an option for a single url through commandline ]~~
- no documentation or help

## Requirements
- `ffmpeg` installed on PATH
- python requirements `requests argparse urllib3 colorama tqdm`

```bash
#For Debian/Ubuntu users
sudo apt-get update -y
sudo apt-get install ffmpeg -y

#For Fedora users
sudo dnf install \
https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf update
sudo dnf install ffmpeg

#Note: this app will work on any linux that supports python, ffmpeg, and python-requirements
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
python -m pip install requests argparse urllib3 colorama tqdm
```
- Usage

use `--verbose` for verbose output

```bash
python pwdl.py --csv-file "/path/to/file.csv"
```

```bash

# alternate usages 
export CSV_FILE="/path/to/file.csv"
python pwdl.py --csv-file "$CSV_FILE"

python pwdl.py --url "<url>" --name "name"

# You may also use the --dir flag to change output directory

python pwdl.py --csv-file "file.csv" --dir "/path/to/out/dir/"
#                        or
python pwdl.py --url "url" --name "name" --dir "/path/to/out/dir"
```
