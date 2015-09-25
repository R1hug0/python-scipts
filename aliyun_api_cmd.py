# coding: utf-8
import sys,os
import urllib,urllib2
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json

# 运行脚本前需要设置access_key_id和access_key_secret
access_key_id = '';
access_key_secret = '';


# 根据所使用的服务设置对应的服务接口地址
server_address = 'https://ecs.aliyuncs.com'


def percent_encode(str):
    res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2014-05-26', \
            'AccessKeyId'   : access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
    }

    for key in user_params.keys():
        parameters[key] = user_params[key]

    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = server_address + "/?" + urllib.urlencode(parameters)
    return url

def make_request(user_params, quiet=False):
    url = compose_url(user_params)
    request = urllib2.Request(url)

    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
    except urllib2.HTTPError, e:
        print(e.read().strip())
        raise SystemExit(e)

    try:
        obj = json.loads(response)
        if quiet:
            return obj
    except ValueError, e:
        raise SystemExit(e)
    json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write('\n')


if __name__ == '__main__':

	if len(sys.argv) < 2:
		print "Usage: python %s Action Param1=Value1 Param2=Value2 ..." % sys.argv[0]
		sys.exit(0)

	user_params = {}
	idx = 1
	if not sys.argv[1].lower().startswith('action='):
		user_params['action'] = sys.argv[1]
		idx = 2

	for arg in sys.argv[idx:]:
		try:
			key, value = arg.split('=')
			user_params[key.lower()] = value
		except ValueError, e:
			print(e.read().strip())
			raise SystemExit(e)


	make_request(user_params)

