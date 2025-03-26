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
   <div className="relative flex flex-col w-full h-screen bg-white dark:bg-gray-900 overflow-hidden">
  <header className="sticky top-0 z-10 flex items-center justify-center w-full gap-2 p-2 bg-white shadow-md dark:bg-gray-900">
    <h1 className="font-urbanist text-lg font-semibold text-center text-black dark:text-white">
      Rafiki Bot
    </h1>
  </header>

  {/* Chatbot content section */}
  <div className="flex flex-col justify-between flex-grow h-full">
    <RouterProvider router={router} />
  </div>

  {/* Dark mode toggle button */}
  <button
    onClick={toggleTheme}
    className="absolute z-20 p-2 transition duration-300 rounded-full top-4 right-4 hover:bg-gray-200 dark:hover:bg-gray-700"
    aria-label="Toggle Theme"
  >
    {darkMode ? (
      <SunIcon className="w-5 h-5 text-yellow-400" />
    ) : (
      <MoonIcon className="w-5 h-5 text-gray-800" />
    )}
  </button>
</div>

  );
}

export default App;
