#!/usr/bin/python3
import requests
import re
import argparse
import random
import os
from threading import Thread

parser = argparse.ArgumentParser()
parser.add_argument('accounts',type=int,help='number of accounts to register')
args = parser.parse_args()
path = path = os.path.dirname(os.path.abspath(__file__))
api_keys = []
api_keys_file = os.path.join(path,'api-keys.txt')

def register(username,password):
	s = requests.Session()
	reg_get = s.get('https://anonfiles.com/register')
	try:
		app_csrf_token = re.findall('var app_csrf_token = "(.*)";',reg_get.text)[0]
	except:
		return ''
	data = {'username':username,'password':password,'password_confirm':password,'_token':app_csrf_token}
	reg_post = s.post('https://anonfiles.com/register',data=data)
	if 'Username already exists' in reg_post.text:
		s.get('https://anonfiles.com/login')
		data = {'username':username,'password':password,'_token':app_csrf_token}
		login_post = s.post('https://anonfiles.com/login',data=data)
		if 'Invalid username or password' in login_post.text:
			print(f'{username}:{password} is invalid')
			return ''
	api_get = s.get('https://anonfiles.com/docs/api')
	try:
		api_key = re.findall('<p>Your account API key is <code class="text-nowrap">(.*)</code></p>',api_get.text)[0]
	except:
		return ''
	return api_key

def get_tokens():
	chars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&?'
	username = ''.join(random.sample(chars,20))
	password = ''.join(random.sample(chars,20))
	key = register(username,password)
	if len(key) == 16:
		print(key)
		api_keys.append(key)	

threads = []

for i in range(args.accounts):
	threads.append(Thread(target=get_tokens))

for thread in threads:
	thread.start()

for thread in threads:
	thread.join()

with open(api_keys_file,'a') as a:
		for key in api_keys:
			a.write(key+'\n')
print(f'Saved API keys to {api_keys_file}')
