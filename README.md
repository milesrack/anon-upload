# anon-upload :file_folder:
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>

Creates a password protected zip archive of a file or directory and uploads it to [anonfiles](https://anonfiles.com).
## :pushpin: Installation
```
git clone https://github.com/milesrack/anon-upload.git
cd anon-upload
pip3 install -r requirements.txt
python3 anon-upload.py
```
## :pushpin: Usage
```
usage: anon-upload.py [-h] [-f FILE] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path of file to upload
  -d DIRECTORY, --directory DIRECTORY
                        path of directory to upload
```
You will have to replace **line 14** with your anonfiles API key. You can use `api-gen.py` to register any number of accounts and get the API key, or you can manually sign up for an account. The usage of `api-gen.py` is simple: `python3 api-gen.py [NUMBER OF ACCOUNTS]`. The API keys will be printed to the console and saved in `api-keys.txt`
