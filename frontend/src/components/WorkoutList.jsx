import React, { useEffect, useState } from 'react';

function WorkoutList() {
  const [workouts, setWorkouts] = useState([]);

  useEffect(() => {
    async function fetchWorkouts() {
      try {
        const response = await fetch('http://127.0.0.1:8000/workouts/');
        if (!response.ok) {
          throw new Error('Failed to fetch workouts');
        }
        const data = await response.json();
        setWorkouts(data);
      } catch (error) {
        console.error('Error fetching workouts:', error);
      }
    }

    fetchWorkouts();
  }, []);
  return (
    <div>
      <h2> Workout History</h2>
    </div>
  );
}
