from flask import Flask, redirect, render_template, request, send_file
import requests
import os
import sys
from flasgger import Swagger
from server import app
from server.routes.prometheus import track_requests
from userapp import osclient
import mimetypes
import os.path
from os import path
import json
import base64

app=Flask(__name__)
UPLOAD_FOLDER = '.'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
global bucket_global
bucket_global = 'classifieds'


# The python-flask stack includes the flask extension flasgger, which will build
# and publish your swagger ui and specification at the /apidocs url. Here we set up
# the basic swagger attributes, which you should modify to match you application.
# See: https://github.com/rochacbruno-archive/flasgger
swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Example API for python-flask stack",
    "description": "API for helloworld, plus health/monitoring",
    "contact": {
      "responsibleOrganization": "IBM",
      "responsibleDeveloper": "Henry Nash",
      "email": "henry.nash@uk.ibm.com",
      "url": "https://appsody.dev",
    },
    "version": "0.2"
  },
  "schemes": [
    "http"
  ],
}
swagger = Swagger(app, template=swagger_template)

# The python-flask stack includes the prometheus metrics engine. You can ensure your endpoints
# are included in these metrics by enclosing them in the @track_requests wrapper.
@app.route('/hello')
@track_requests
def HelloWorld():
    # To include an endpoint in the swagger ui and specification, we include a docstring that
    # defines the attributes of this endpoint.
    """A hello message
    Example endpoint returning a hello message
    ---
    responses:
      200:
        description: A successful reply
        examples:
          text/plain: Hello from Appsody!
    """
    return 'Hello from Appsody!'

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/')
def index():
    return redirect('/apidocs')

# If you have additional modules that contain your API endpoints, for instance
# using Blueprints, then ensure that you use relative imports, e.g.:
# from .mymodule import myblueprint

@app.route("/home")
def home():
  return "Your object storage operations application test is successful"

@app.route('/createbucket', methods = ['GET'])
@track_requests
def create_bucket():
   """Create bucket
    Create a bucket in Cloud Object Storage
    ---
    responses:
      200:
        description: A successful reply. Returns home page html.
   """
   bucketname = request.args.get("bucketname");
   print("creating bucket: " + bucketname);
   resp = osclient.create_bucket(bucketname);
   bukets = osclient.get_buckets();
   return bukets;

@app.route('/setbucket', methods = ['GET'])
@track_requests
def set_bucket():
   """Create bucket
    Create a bucket in Cloud Object Storage
    ---
    responses:
      200:
        description: A successful reply. Returns home page html.
   """
   bucketname = request.args.get("buket");
   print("setting bucket: " + bucketname);
   bucket_global = bucketname
   return "success";

@app.route('/upload', methods = ['GET', 'POST'])
@track_requests
def upload_file():
   """Upload file
    Upload a file to Cloud Object Storage
    ---
    responses:
      200:
        description: A successful reply. Returns home page html.
    """
   print("inside upload method")
   if request.method == 'POST':
      f = request.files['file']
      bucket = bucket_global
      # save to object storage
      resp = osclient.put_file(bucket, f.filename, f.read());
      #bukets = osclient.get_buckets()
      return resp


@app.route('/getfile', methods = ['GET'])
@track_requests
def get_object():
   """Get file
    Get a file from Cloud Object Storage
    ---
    responses:
      200:
        description: A successful reply. Returns html with file contents for text and image files.
    """
   # clear the cache
   if path.exists("./userapp/image"):
       os.remove("./userapp/image");

   if request.method == 'GET':
      print(request.args)
      bucket = request.args["buket"]
      bucket_global = bucket
      name =  request.args["filename"]
      contents = osclient.get_file(bucket, name)
      print(type(contents))
      mime = mimetypes.guess_type(name)[0]
      txtcontent = "";
   if "text" in mime:
      txtcontent=contents.read().decode('utf-8')
      return txtcontent

   if "image" in mime:
     f = open("./userapp/image.jpg", "wb+");
     x= contents.read()
     y = x
     f.write(x);
     #f.close()
     res = name + " retrieved successfully from " +  bucket + " bucket"
     return res


@app.route('/getimage')
@track_requests
def get_image():
    with open("./userapp/image.jpg", "rb") as imageFile:
      stri = base64.b64encode(imageFile.read())
      result = stri.decode('ASCII')
    return result
