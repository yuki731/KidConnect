import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignupPage from './components/SignupPage';
import LoginPage from './components/LoginPage';
import ParentsPage from './components/ParentsPage';
import PermissionCheck from './components/PermissionCheck';

const App: React.FC = () => {
  return (
      <Router>
          <Routes>
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/parents_dashboard" element={<ParentsPage />} />
              <Route path="/permission_check" element={<PermissionCheck />} />
          </Routes>
      </Router>
  );
};

export default App;
