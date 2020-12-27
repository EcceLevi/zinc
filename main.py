import sys
import requests
from googlesearch import search as gsearch
from duckduckpy import query as ddquery
from urllib.parse import urlparse
import re


arguments = []
domain = ''
testList = ['exodus.io',
            'wikipedia.com',
            'google.com']


def main():
	define()

	#recon target
	subdomains = recon(domain)
	print(subdomains)

	#recon domains/servers
	domainData = checkHTTP(subdomains)
	robotsData = checkRobots(domainData)

	#recon apps
	#checkSSRFCandidates()


def recon(domain):
	print('Target domain ' + domain)
	print('subdomain recon:')
	print('\tsearching engines...')
	subdomains = []

	global testList
	subdomains = testList
	#googleResults = googleSearch(domain)
	#duckduckResults = duckduckgoSearch(domain)
	#subdomains.append(googleResults)
	#subdomains.append(duckduckResults)
	subdomains = subdomains + domainsParse(subdomains)

	return subdomains


def domainsParse(domains_list):
	results = []
	for j in domains_list:
		results.append(urlparse(j).netloc)
	results = list(dict.fromkeys(results))
	for j in results:
		print(j)
	return results

def googleSearch(domain):
	print("\tGoogle:")
	googleResults = []
	query = 'site:*.'+ domain + \
			' -https://' + domain + \
			' -https://www.' + domain + \
			' -http://' + domain + \
			' -http://www.' + domain
	for j in gsearch(query, tld='com', lang='en', num=100, start=0, stop=100, pause=2.0):
		googleResults.append(j)
	return googleResults
def duckduckgoSearch(domain):
	print("\tDuckDuckGo:")
	duckduckResults = []
	query = 'site:' + domain + \
			' -https://' + domain + \
			' -https://www.' + domain + \
			' -http://' + domain + \
			' -http://www.' + domain
	respone = ddquery(query_string=domain,
			secure=False,
			no_html=False,
			verbose=False,
			user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
	print(respone)
	return duckduckResults
def checkHTTP(domains):
	"""
	REWRITE
	MUST BE: [url, status, redirected_to]
	"""
	results = []
	url = ''
	cnt = 0
	#https
	for i in range(0, len(domains) - 1):
		url = 'https://' + domains[i] + '/'
		try:
			r = requests.get(url, allow_redirects=False)
			try:
				if r.headers['location'] == 'https://www.' + domains[i] + '/':
					results.append({'url': url, 'status': r.status_code})
				else:
					results.append({'url': url, 'status': r.status_code, 'redirect': r.headers['location']})
			except Exception:
				results.append({'url': url, 'status': r.status_code})
		except:
			print('none')
		cnt += 1
	#http
	for i in range(0, len(domains) - 1):
		url = 'http://' + domains[i] + '/'
		r = requests.get(url, allow_redirects=False)

		try:
			if r.headers['location'] != 'https://www.' + domains[i] + '/':
				if r.headers['location'] != 'https://' + domains[i] + '/':
					results.append({'url': url, 'status': r.status_code, 'redirect': r.headers['location']})
				else:
					if r.headers['location'] != 'https://' + domains[i] + '/':
						results.append({'url': url, 'status': r.status_code})
		except Exception:
			results.append({'url': url, 'status': r.status_code})

	for j in results:
		print(j)
	return results
def checkRobots(targets):
	results = []
	url = ''
	for i in range(0, len(targets) - 1):
		url = targets[i]['url'] + '/robots.txt'
		r = requests.get(url)
		if r.status_code == 200:
			results.append({'url': targets[i]['url'], 'disallowed': splitDisallowed(r.content)})

	for i in results:
		print(i)
	return results
def splitDisallowed(content):
	splitted = str(content).split('\\n')
	results = []

	for j in splitted:
		if str(j).startswith('Disallow'):
			results.append(j[10:-1])

	results = list(dict.fromkeys(results))
	results = list(filter(None, results))
	return results

#checkSSRFCandidates(domain/domains)
#processes domains list to acquire potential SSRF candidates
#?url=*,?q=*,?u=*,?link=*,?host=*,?file=*?,path=*,?imgurl=*,?src=*,?consumerUri=*
def checkSSRFCandidates(domain):
	results = []


	return results


def saveResults():
	#saving results
	print('zog')


def help():
	print('usage: quicksilver.py ' + '\033[4m' + 'domain.com' + '\033[0m (without www.)' + ' options ' + '\033[4m' + 'results.file' + '\033[0m' + '\n'
		  'options:' + '\n'
		  '\t...' + '\n'
		  '\t...' + '\n'
		  '\t...' + '\n'
		  '\t...' + '\n')


def define():
	global arguments
	arguments = sys.argv
	global domain
	domain = arguments[1]


if __name__ == "__main__":
	main()
