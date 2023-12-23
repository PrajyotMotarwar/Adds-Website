from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.binary import Binary


app = Flask(__name__, template_folder='template')


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://motarwarprajyot:Rrx91Ak5xoiNUh8F@cluster0.k0sxca1.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded images
app.config['MONGO_URI'] = 'mongodb+srv://motarwarprajyot:Rrx91Ak5xoiNUh8F@cluster0.k0sxca1.mongodb.net/?retryWrites=true&w=majority'

mongo = MongoClient(app.config['MONGO_URI'])
db = mongo['ads']
collection = db['images']



@app.route("/") 
def home():
    return render_template('index.html') 

@app.route("/about")
def about(): 
    return render_template('about.html')

@app.route("/post") 
def post():
    return render_template('post.html') 

@app.route('/contact')
def index():
    return render_template('contact.html') 

@app.route('/contact', methods=['POST'])
def upload():
    image = request.files['image']
    if image:
        # Read the image file
        image_data = image.read()
        # Store the image data in the database
        image_binary = Binary(image_data)
        collection.insert_one({'image': image_binary})
        return 'Image uploaded successfully!'
    else:
        return 'No image selected.'
    return render_template('contact.html')

@app.route('/image/<image_id>')
def get_image(image_id):
    image = collection.find_one({'_id': image_id})
    if image:
        image_data = image['image']
        return image_data, 200, {'Content-Type': 'image/jpeg'}
    else:
        return 'Image not found', 404

if __name__ == '__main__':
    app.run(debug=True)  