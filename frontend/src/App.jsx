// Author: Ian Surat-Mosher | Github: @iMosher
import WorkoutForm from './components/WorkoutForm';
import WorkoutList from './components/WorkoutList';

function App() {
  return (
    <div className="App">
      <h1>Workout Tracker</h1>
      <WorkoutForm />
      <WorkoutList />
    </div>
  );
}

export default App;
