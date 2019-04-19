#!/usr/local/bin/python3

import subprocess
import requests
import json
import argparse
import os
import sys
from requests.auth import HTTPBasicAuth


def get_urls(workspace, username, password, project_key=None):
	# TODO: Add support for >100 repos. Bitbucket API returns max 100 items per single query.
	params = {
		'pagelen': 100
	}
	if project_key:
		params['q'] = 'project.key="%s"' % (project_key)

	r = requests.get('https://bitbucket.org/api/2.0/repositories/%s' % (workspace), params=params, auth=HTTPBasicAuth(username, password))

	try:
		r.raise_for_status()
	except Exception as e:
		sys.exit(e)
	
	urls = []

	for i in r.json()['values']:
		for k in i['links']['clone']:
			if k['name'] == 'ssh':
				urls.append({'name': i['name'], 'url': k['href']})

	return urls

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('command', help='[list | clone]')
	parser.add_argument('workspace', help='Bitbucket workspace ID')

	parser.add_argument('--project-key', nargs=1, help='Bitbucket project key')
	parser.add_argument('--path', nargs=1, help='Clone destination path')

	parser.add_argument('--username', nargs=1, help='Bitbucket username', required=True)
	parser.add_argument('--password', nargs=1, help='Bitbucket app password', required=True)

	args = parser.parse_args()

	project_key = None
	if args.project_key:
		project_key = args.project_key[0]

	path = None
	if args.path:
		path = args.path[0]

	for i in get_urls(args.workspace, args.username[0], args.password[0], project_key):
		if (args.command) == 'list':
			print(i)
		elif (args.command) == 'clone':
			cmd = ['git', 'clone', i['url']]
			if path:
				cmd.append('%s/%s' % (path, i['name']))
			subprocess.call(cmd, stdout=None, stderr=None)

if __name__ == '__main__':
	main()
