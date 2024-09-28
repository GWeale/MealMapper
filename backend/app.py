from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from ai_model.model import analyze_meal

app = Flask(__name__)
CORS(app) # cant tell you these parts
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meals.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    image_filename = db.Column(db.String(120), nullable=False)

db.create_all()

@app.route('/api/meals', methods=['POST'])
def add_meal():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    meal_data = analyze_meal(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    meal = Meal(name=meal_data['name'], calories=meal_data['calories'], image_filename=filename)
    db.session.add(meal)
    db.session.commit()
    return jsonify({'id': meal.id, 'name': meal.name, 'calories': meal.calories}), 201

@app.route('/api/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([{'id': meal.id, 'name': meal.name, 'calories': meal.calories, 'image': meal.image_filename} for meal in meals]), 200

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
