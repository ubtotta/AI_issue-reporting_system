from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import smtplib
from email.message import EmailMessage
import suggestions  # your custom suggestion module
import numpy as np
from tensorflow.keras.models import load_model #type:ignore
from tensorflow.keras.preprocessing import image  #type:ignore

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model once at start
model = load_model('issue_classifier/issue_classifier.h5')
classes = ['ac', 'fan', 'wall_leakage']

# Email configuration
EMAIL_SENDER = 'ubtotta16@gmail.com'
EMAIL_PASSWORD = 'xtby myyi utlr lbto'  # Use secure env in real apps

authority_emails = {
    'fan': 'tottaub@gmail.com',
    'ac': 'ubtotta@gmail.com',
    'wall_leakage': 'tottaub@gmail.com'
}

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        description = request.form['description']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        file = request.files['image']
        if file.filename == '':
            return "No file selected"
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess image and predict
        img = image.load_img(filepath, target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        predicted_class = classes[np.argmax(prediction)]

        # Get suggestions
        problem, solution = suggestions.get_suggestion(predicted_class)

        # Compose email
        recipient = authority_emails.get(predicted_class, 'default@example.com')
        subject = f"Issue reported: {predicted_class.upper()}"
        body = f"""
Name: {name}
Description: {description}
Predicted Issue: {predicted_class}
Problem: {problem}
Suggested Solution: {solution}
Location: https://www.google.com/maps?q={latitude},{longitude}
"""

        send_email(subject, body, recipient, filepath)
        return f"Issue submitted successfully. Identified as: {predicted_class}. Email sent to {recipient}."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def send_email(subject, body, to, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = to
    msg.set_content(body)

    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)

    msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, threaded=True, host='0.0.0.0', port=port)
