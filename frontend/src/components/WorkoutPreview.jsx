// Author: Ian Surat-Mosher | GitHub: @iMosher
// Description: Component to preview workout before submission
import React from 'react';

function WorkoutPreview({ date, exercises }) {
  if (!date && exercises.length === 0) return null; //check for the existance of both date and exercises

  return (
    <div
      style={{ border: '1px solid #999', marginTop: '2rem', padding: '1rem' }}
    >
      <h3>Workout Submission Preview</h3>
      <p>
        <strong>Date:</strong>
        {date || 'N/A'}
      </p>
      <ul>
        {exercises.map((exercise, i) => (
          <div key={i} style={{ marginTop: '1rem' }}>
            <strong>
              Exercise {i + 1}: {exercise.name || '(no name)'}
            </strong>
            <ul>
              {exercise.sets.map((set, j) => (
                <li key={j}>
                  Set {j + 1}: Reps: {set.reps || '-'} Weight:{' '}
                  {set.weight || '-'}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </ul>
    </div>
  );
}

export default WorkoutPreview;
