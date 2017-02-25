'''
Created on Feb 24, 2017

@author: TuanNguyen
'''
'''
Created on Feb 24, 2017

@author: TuanNguyen
'''
from flask import Flask, request, redirect
from flask_restful import Api, Resource
import urllib2
from urllib2 import Request, URLError
import requests
import json

app = Flask(__name__)
api = Api(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #maximum allowed upload to 16 megabytes

class Proxy(Resource):
    def get(self,url):
        try:
            user_agent = request.headers['User-Agent']
            accept=request.headers['Accept']
            headers = {'User-Agent': user_agent,'Accept':accept}
            req = Request(url,headers=headers)
            response = urllib2.urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                return str('We failed to reach a server. Reason: '+ str(e.reason))
            elif hasattr(e, 'code'):
                print str('The server couldn\'t fulfill the request.'+ ' Error code: '+ str(e.code))
        else:
            the_page = response.read()
            try: 
                the_page = json.loads(the_page)
                return the_page
            except ValueError:
                return the_page
    def post(self,url):
        try:
            values=None
            upfile=None
            files=request.files
            if request.form != '':
                values = request.form
            if files.__len__() != 0:
                f = files[files.keys()[0]]
                f.save(f.filename)
                upfile = {files.keys()[0]: open(f.filename, 'rb')}
            user_agent = request.headers['User-Agent']
            accept=request.headers['Accept']
            headers = {'User-Agent': user_agent,'Accept':accept}
            r = requests.post(headers=headers,data=values,url=url, files=upfile)
            the_page = r.text
            try: 
                the_page = json.loads(the_page)
                return the_page
            except ValueError:
                return the_page
        except URLError as e:
            if hasattr(e, 'reason'):
                return str('We failed to reach a server. Reason: '+ str(e.reason))
            elif hasattr(e, 'code'):
                print str('The server couldn\'t fulfill the request.'+ ' Error code: '+ str(e.code))
        

api.add_resource(Proxy, '/proxy/<path:url>')

@app.route('/')
def index():
    return redirect('http://localhost:8000/proxy/http://httpbin.org/get') #redirect default page

if __name__ == '__main__':
    app.run(port=8000,debug=True)