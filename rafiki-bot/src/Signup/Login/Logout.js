import React, { useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const LogOut = () => {
  const navigate = useNavigate();

  const handleLogout = useCallback(() => {
    // Remove user-related data from localStorage
    localStorage.removeItem('isSignedUp');
    localStorage.removeItem('username');
    localStorage.removeItem('email');

    // Optionally, clear session data or token if needed
    // sessionStorage.removeItem('token');

    // Redirect the user to the login page
    navigate('/login');
  }, [navigate]); // We only need navigate as a dependency for memoization

  useEffect(() => {
    handleLogout(); // Call handleLogout once on mount
  }, [handleLogout]); // Include memoized handleLogout in the dependencies

  return (
    <div className="max-w-sm p-4 mx-auto my-10 bg-white border rounded-lg shadow-lg">
      <h2 className="text-2xl text-center">Logging out...</h2>
    </div>
  );
};

export default LogOut;
