from flask import Flask, render_template, request, jsonify
import os
from google.generativeai import GenerativeModel
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

model = GenerativeModel("gemini-1.5-flash")

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    image = request.files['image']
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    prompt = "Classify the waste in this image as 'biodegradable' or 'non-biodegradable'. Explain briefly."
    result = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': open(filepath, 'rb').read()}])
    response_text = result.text if result else "Unable to classify."
    return jsonify({'result': response_text})

if __name__ == '__main__':
    app.run(debug=True)


