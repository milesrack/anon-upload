#!/usr/bin/python3
import argparse
import os
import sys
import pyzipper
import random
from anonfile.anonfile import AnonFile

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',type=argparse.FileType('r'),help='path of file to upload')
parser.add_argument('-d','--directory',type=str,help='path of directory to upload')
args = parser.parse_args()

anon = AnonFile('YOUR API KEY') #https://anonfiles.com -> Login -> https://anonfiles.com/docs/api to get API key
path = os.path.dirname(os.path.abspath(__file__))
extention = '.zip'

#Uploads the zipfile to anonfiles.com
def upload(zipname):
	try:
		print('\033[1;33mUploading %s -> anonfiles.com\033[0m' % zipname)
		status, file_url = anon.upload_file(zipname)
		if status:
			return '\033[96m%s\033[00m' % file_url
		else:
			return '\033[91mUpload failed\033[00m'
	except OSError:
		return '\033[91mCould not connect to anonfiles.com\033[00m'

#Creates a random 32 character password
def makepassword():
	chars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?'
	password = ''.join(random.sample(chars,32))
	return password

#Zips a file
def zipfile(filetuple):
	filename = filetuple[0]
	zipname = filetuple[1]
	with open(filename,'rb') as f:
		filedata = f.read()
	print('\033[1;33mZipping',filename,'->',zipname + '\033[0m')
	with pyzipper.AESZipFile(zipname,'w',compression=pyzipper.ZIP_LZMA,encryption=pyzipper.WZ_AES) as zf:
		password = bytes(makepassword(), 'utf-8')
		zf.setpassword(password)
		zf.setencryption(pyzipper.WZ_AES, nbits=256)
		zf.writestr(filename,filedata)
	return zipname, password.decode('utf-8')

#Zips a directory and its contents
def zipdir(directorytuple):
	dirname = directorytuple[0]
	zipname = directorytuple[1]
	print('\033[1;33mZipping',dirname,'->',zipname + '\033[0m')
	with pyzipper.AESZipFile(zipname, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
		password = bytes(makepassword(), 'utf-8')
		zf.setpassword(password)
		zf.setencryption(pyzipper.WZ_AES, nbits=256)
		for folderName, subfolders, filenames in os.walk(dirname):
			for filename in filenames:
				filePath = os.path.join(folderName, filename) #Create complete filepath of file in directory
				with open(filePath,'rb') as f:
					fileData = f.read()
				zf.writestr(os.path.basename(filePath),fileData)
	return zipname, password.decode('utf-8')

#Checks that the given file is valid and returns it with the corresponding zip file name
def isfile(file):
	if os.path.isfile(file.name):
		filename = file.name
		zipname = os.path.splitext(os.path.basename(filename))[0] + extention
		return filename,zipname
	else:
		print('\033[91mNot a valid file!\033[00m')
		sys.exit()

#Checks that the given directory is valid and returns it with the corresponding zip file name
def isdir(directory):
	if os.path.isdir(directory):
		dirname = os.path.basename(os.path.dirname(directory))
		zipname = dirname + extention
		return directory,zipname
	else:
		print('\033[91mNot a valid directory!\033[00m')
		sys.exit()

#Main function
def main():
	if args.file:
		file = isfile(args.file)
		zipped, password = zipfile(file)
	elif args.directory:
		directory = isdir(args.directory)
		zipped, password = zipdir(directory)	
	else:
		parser.print_help()
		sys.exit()
	uploaded = upload(zipped)
	print(uploaded)
	print(f'\033[92m{password}\033[00m')
	os.remove(zipped)

if __name__ == '__main__':
	main()
