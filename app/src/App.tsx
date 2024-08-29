import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignupPage from './components/SignupPage';
import LoginPage from './components/LoginPage';
import LogoutPage from './components/Logout';
import ParentsPage from './components/ParentsPage';
import PermissionCheck from './components/PermissionCheck';
import CreateUserAccount from './components/CreateUser';
import ChildrenPage from './components/ChildrenPage';
import CreateJobCardForm from './components/CreateJobCard'

const App: React.FC = () => {
  return (
      <Router>
          <Routes>
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/parents_dashboard" element={<ParentsPage />} />
              <Route path="/permission_check" element={<PermissionCheck />} />
              <Route path="/create-user" element={<CreateUserAccount />} />
              <Route path="/create-job-card" element={<CreateJobCardForm />} />
              <Route path="/children_dashboard" element={<ChildrenPage />} />
              <Route path="/logout" element={<LogoutPage />} />

          </Routes>
      </Router>
  );
};

export default App;
