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

templates/index.html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Smart Waste Management</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
    input[type=file] { margin: 20px; }
    .result { margin-top: 20px; font-weight: bold; }
  </style>
</head>
<body>
  <h1>♻️ Smart Waste Classifier</h1>
  <form id="upload-form" enctype="multipart/form-data">
      <input type="file" name="image" accept="image/*" required>
      <button type="submit">Classify Waste</button>
  </form>
  <div class="result" id="result"></div>

  <script>
      const form = document.getElementById('upload-form');
      form.addEventListener('submit', async (e) => {
          e.preventDefault();
          const formData = new FormData(form);
          const response = await fetch('/predict', { method: 'POST', body: formData });
          const data = await response.json();
          document.getElementById('result').textContent = data.result;
      });
  </script>
</body>
</html>

requirements.txt

flask
google-generativeai
werkzeug
