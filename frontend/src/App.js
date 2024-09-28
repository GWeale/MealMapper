import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [meals, setMeals] = useState([]);
  const [image, setImage] = useState(null);
  const [name, setName] = useState('');
  const [calories, setCalories] = useState('');

  useEffect(() => {
    fetchMeals();
  }, []);

  const fetchMeals = async () => {
    const res = await axios.get('http://localhost:5000/api/meals');
    setMeals(res.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;
    const formData = new FormData();
    formData.append('image', image);
    const res = await axios.post('http://localhost:5000/api/meals', formData);
    setMeals([...meals, res.data]);
    setImage(null);
  };

  return (
    <div className="container">
      <h1 className="mt-4">AI Meal Tracker</h1>
      <form onSubmit={handleSubmit} className="mt-4">
        <div className="mb-3">
          <label className="form-label">Upload Meal Photo</label>
          <input type="file" className="form-control" onChange={(e) => setImage(e.target.files[0])} required />
        </div>
        <button type="submit" className="btn btn-primary">Add Meal</button>
      </form>
      <div className="mt-5">
        <h2>Tracked Meals</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Calories</th>
              <th>Image</th>
            </tr>
          </thead>
          <tbody>
            {meals.map(meal => (
              <tr key={meal.id}>
                <td>{meal.name}</td>
                <td>{meal.calories}</td>
                <td><img src={`http://localhost:5000/uploads/${meal.image}`} alt={meal.name} width="100" /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
