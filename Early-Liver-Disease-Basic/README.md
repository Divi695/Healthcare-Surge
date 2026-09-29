# Early Prediction of Liver Disease Using Deep Learning - Beginner Version

A simple hackathon-style web project with:
- HTML for frontend structure
- CSS for design
- JavaScript for form handling and API calls
- Python Flask for a basic backend

## Project structure

frontend/
  index.html
  style.css
  script.js

backend/
  app.py
  requirements.txt

## Run backend

cd backend
pip install -r requirements.txt
python app.py

Backend: http://127.0.0.1:5000

## Run frontend

Open `frontend/index.html` directly in a browser.

Enter the patient values and click **Predict Liver Disease Risk**.

The browser sends the data to the Flask backend and displays the prediction.

## Important

The backend currently uses a simple demonstration rule instead of a clinically validated model. It is suitable for learning and a basic hackathon prototype, not medical diagnosis.
