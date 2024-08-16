import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignupPage from './components/SignupPage';

const App: React.FC = () => {
  return (
      <Router>
          <Routes>
              <Route path="/signup" element={<SignupPage />} />
          </Routes>
      </Router>
  );
};

export default App;
