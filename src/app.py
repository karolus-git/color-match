import os
import gridfs
import numpy as np
import base64
from dotenv import load_dotenv
from bson import objectid
from flask import Flask, render_template, request, jsonify
from flask_dropzone import Dropzone
from flask_mongoengine import MongoEngine

from flask import redirect, url_for

import mongo
from color_kmeans import ColorKMeans

load_dotenv()

FLASK_PORT = os.getenv('FLASK_PORT', '8050')
FLASK_HOST = os.getenv('FLASK_HOST', 'localhost')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
    static_folder='static')

dropzone = Dropzone(app)

#Load the DB
database, _ = mongo.init_db()

#Create an object of GridFs for the above database.
fs = gridfs.GridFS(database)

@app.route('/delete/<md5>')
def delete(md5):

    # Get the md5 of the file
    result = fs.find_one({ "md5": md5 })
    
    # Delete it
    fs.delete(result._id)

    return redirect(url_for('upload'))

@app.route('/', methods=['POST', 'GET'])
def upload():
    
    # TODO make a variable
    color_number = 0

    if request.method == 'POST':

        # For all files dropped in the dropzone
        for key, f in request.files.items():         
            
            # File is read
            contents = f.read()

            # Search the colors
            ckm = ColorKMeans(contents=contents)
            labels, palette = ckm.extract_colors(color_number=color_number)
            
            # Push it in the db, including the image
            fs.put(contents, 
                md5=ckm.md5, 
                filename=f.filename, 
                colors=color_number,
                palette=np.array2string(palette, separator=','),
                labels=np.array2string(labels, separator=','),
            )

    # Get all the objects of the database
    # BUG the sort part is useless because of the Masonry inclusion 
    objects_found = fs.find().sort("uploadDate")
    
    # Content that will be pushed in the html
    contents = []

    # For each object
    for f in objects_found:

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb

        # Decode the image
        img_base64 = base64.b64encode(f.read())
        img_base = img_base64.decode()

        palette = eval('np.array(' + f.palette + ')')
        palette = tuple(map(tuple, palette))
        # Convert RGB to Hex
        palette_hex = [rgb_to_hex((r,g,b)) for r, g, b in palette]

        # Create a dict 
        settings = {
            "file" : img_base, #Image
            "filename" : f.filename, # Filename
            "palette_hex" : palette_hex, #List of colors as hex
            "md5" : f.md5, # MD5
        }

        contents.append(settings)
    
    return render_template('index.html', contents=contents)


if __name__ == '__main__':
    app.run(debug=True, host=FLASK_HOST, port=FLASK_PORT)