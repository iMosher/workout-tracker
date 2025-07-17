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
      <h2>Workout History</h2>
      {workouts.map((workout) => (
        <div key={workout.id} style={{ marginBottom: '1rem' }}>
          <h3>{workout.date}</h3>

          {workout.tags.length > 0 && (
            <div>
              {workout.tags.map((tag) => (
                <span
                  key={tag.id}
                  style={{
                    backgroundColor: tag.color || '#ddd',
                    color: '#000',
                    padding: '0.25rem 0.5rem',
                    marginRight: '0.5rem',
                    borderRadius: '5px',
                  }}
                >
                  {tag.name}
                </span>
              ))}
            </div>
          )}

          {workout.exercises.map((exercise) => (
            <div key={exercise.id}>
              <strong>{exercise.name}</strong>
              <ul>
                {exercise.sets.map((set) => (
                  <li key={set.id}>
                    Reps: {set.reps}, Weight: {set.weight ?? 'Bodyweight'}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default WorkoutList;
