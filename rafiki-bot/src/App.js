import { useState, useEffect } from 'react';
import { createBrowserRouter, createRoutesFromElements, RouterProvider, Route, Navigate } from 'react-router-dom';
import SignUp from './Login/Signup/SignUp';
import Login from './Login/Signup/Login';
import Chatbot from './interface/ChatBot';
import { MoonIcon, SunIcon } from '@heroicons/react/20/solid'; // Import Heroicons

function App() {
  // Initialize dark mode state from localStorage
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('theme') === 'dark');
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('loggedIn') === 'true'); // State for logged-in status

  // Set up the router
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        {/* If the user is logged in, redirect to Chatbot */}
        <Route path="/" element={isLoggedIn ? <Chatbot /> : <Navigate to="/login" />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} /> {/* Pass login handler to Login */}
      </>
    )
  );

  // Handle theme toggle and save to localStorage
  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  const toggleTheme = () => {
    setDarkMode((prev) => !prev); // Toggle dark mode state
  };

  return (
    <div className="relative flex flex-col w-full min-h-screen bg-white dark:bg-gray-900">
       {/* Dark mode toggle button */}
      <button
        onClick={toggleTheme}
        className="absolute z-20 p-2 transition duration-300 rounded-full top-4 right-4 hover:bg-gray-200 dark:hover:bg-gray-700"
        aria-label="Toggle Theme"
      >
        {darkMode ? (
          <SunIcon className="w-6 h-6 text-yellow-400" />
        ) : (
          <MoonIcon className="w-6 h-6 text-gray-800" />
        )}
      </button>

      {/* RouterProvider to render routes */}
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
