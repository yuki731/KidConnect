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
import ReportJobPage from './components/RequestJob'
import RequestWithdrawalPage from './components/RequestWithdrawal'
import ChildrenList from './components/ChildrenView'

const App: React.FC = () => {
  return (
      <Router>
          <Routes>
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/logout" element={<LogoutPage />} />
              <Route path="/parents_dashboard" element={<ParentsPage />} />
              <Route path="/permission_check" element={<PermissionCheck />} />
              <Route path="/create-user" element={<CreateUserAccount />} />
              <Route path="/create-job-card" element={<CreateJobCardForm />} />
              <Route path="/children_dashboard" element={<ChildrenPage />} />
              <Route path="/children_dashboard" element={<ChildrenPage />} />
              <Route path="/report-job" element={<ReportJobPage />} />
              <Route path="/request-withdrawal" element={<RequestWithdrawalPage />} />
              <Route path="/children_list" element={<ChildrenList />} />

          </Routes>
      </Router>
  );
};

export default App;
