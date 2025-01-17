import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from veg_test import testImage
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    # Function to upload an image. You can upload images from test folder or from the internet and classify them.
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)

	file = request.files['file']

	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)

	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		flash('Image successfully uploaded and displayed below')
        # please make sure to change path of your uploads folder
		return render_template('upload.html', filename=filename,caption=testImage({"image":"D:/w/weaviate-examples/vegetable-classification/static/uploads/{}".format(filename)}))

	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    # Function to display uploaded image
    print("Display image called")
    
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)