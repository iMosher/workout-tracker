// Author: Ian Surat-Mosher | Github: @iMosher
// Description: Form Component for workout entry
import React, { useState } from 'react';

function WorkoutForm() {
  //workout variables
  const [date, setDate] = useState('');
  const [exercises, setExercises] = useState([
    {
      name: '',
      sets: [{ reps: '', weight: '' }],
    },
  ]);

  //Exercise name change event handler
  function handleExerciseNameChange(index, value) {
    const updated = [...exercises];
    updated[index].name = value;
    setExercises(updated);
  }

  //Set Change Handler
  function handleSetChange(exerciseIndex, setIndex, field, value) {
    const updated = [...exercises];
    updated[exerciseIndex].sets[setIndex][field] = value;
    setExercises(updated);
  }

  //Add a set to the workout
  function addSet(exerciseIndex) {
    const updated = [...exercises];
    updated[exerciseIndex].sets.push({ reps: '', weight: '' });
    setExercises(updated);
  }

  //Remove a set
  function removeSet(exerciseIndex, setIndex) {
    const updated = [...exercises];
    updated[exerciseIndex].sets.splice(setIndex, 1);
    setExercises(updated);
  }

  function addExercise() {
    setExercises([
      ...exercises,
      { name: '', sets: [{ reps: '', weight: '' }] },
    ]);
  }

  //Remove an exercise
  function removeExercise(exerciseIndex) {
    const updated = [...exercises];
    updated.splice[(exerciseIndex, 1)];
    setExercises(updated);
  }

  //Submit the workout
  const handleSubmit = async (e) => {
    // prevent default refresh on submit
    e.preventDefault();

    //Basic Validation
    if (!date) {
      alert('Please enter a date for the workout.');
      return;
    }

    for (let i = 0; i < exercises.length; i++) {
      const ex = exercises[i];
      if (!ex.name.trim()) {
        alert(`Exercise ${i + 1} is missing a name.`);
        return;
      }
      for (let j = 0; j < ex.sets.length; j++) {
        const s = ex.sets[j];
        if (!s.reps || !s.weight) {
          alert(`Set ${j + 1} in Exercise ${i + 1} is missing reps or weight.`);
          return;
        }
      }
    }
    //Submission setup
    const workoutData = {
      date: date,
      exercises: exercises.map((exercise) => ({
        name: exercise.name,
        sets: exercise.sets.map((set) => ({
          reps: parseFloat(set.reps),
          weight: parseFloat(set.weight),
        })),
      })),
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/workouts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(workoutData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log('Workout submitted successfully:', result);
    } catch (error) {
      console.error('Error submitting workout:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Date:</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      {exercises.map((exercise, exerciseIndex) => (
        <div
          key={exerciseIndex}
          style={{ border: '1px solid #ccc', margin: '1rem', padding: '1rem' }}
        >
          <label>Exercise Name:</label>
          <input
            type="text"
            value={exercise.name}
            onChange={(e) =>
              handleExerciseNameChange(exerciseIndex, e.target.value)
            }
          />

          {exercise.sets.map((set, setIndex) => (
            <div key={setIndex} style={{ marginLeft: '1rem' }}>
              <label>Reps:</label>
              <input
                type="number"
                value={set.reps}
                onChange={(e) =>
                  handleSetChange(
                    exerciseIndex,
                    setIndex,
                    'reps',
                    e.target.value
                  )
                }
              />

              <label>Weight:</label>
              <input
                type="number"
                step="0.1"
                value={set.weight}
                onChange={(e) =>
                  handleSetChange(
                    exerciseIndex,
                    setIndex,
                    'weight',
                    e.target.value
                  )
                }
              />
            </div>
          ))}

          <button type="button" onClick={() => addSet(exerciseIndex)}>
            + Add Set
          </button>
        </div>
      ))}

      <button type="button" onClick={addExercise}>
        + Add Exercise
      </button>

      <button
        type="button"
        onClick={() => removeExercise(exerciseIndex)}
        style={{ color: 'red', marginTop: '0.5rem' }}
      >
        🗑 Remove Exercise
      </button>
      <div>
        <button type="submit">Submit Workout</button>
      </div>
    </form>
  );
}

export default WorkoutForm;
