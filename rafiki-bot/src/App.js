import { useState, useEffect } from 'react';
import Chatbot from './interface/ChatBot';
import { MoonIcon, SunIcon } from '@heroicons/react/20/solid'; 
import SignUp from './Signup/Login/SignUp';
import Login from './Signup/Login/Login';
import ForgotPassword from './Signup/Login/ForgotPassword';
import LogOut from './Signup/Login/Logout';
import { createBrowserRouter, createRoutesFromElements, RouterProvider, Route, Navigate } from 'react-router-dom';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => localStorage.getItem('isLoggedIn') === 'true');
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('theme') === 'dark');

  // Dark mode logic
  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  const toggleTheme = () => setDarkMode((prev) => !prev);

  // Handle login state change
  const handleLogin = (status) => {
    setIsLoggedIn(status);
    localStorage.setItem('isLoggedIn', status ? 'true' : 'false');
  };

  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        {/* Define route for signup */}
        <Route path="/signup" element={isLoggedIn ? <Navigate to="/" /> : <SignUp />} />
        {/* Define route for login */}
        <Route path="/login" element={isLoggedIn ? <Navigate to="/" /> : <Login onLogin={handleLogin} />} />
        {/* Define route for forgot password */}
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/logout" element={<LogOut onLogin={handleLogin}/>} />
        {/* Define route for home that checks if user is logged in */}
        <Route path="/" element={isLoggedIn ? <Chatbot/> : <Navigate to="/login" />} />
      </>
    )
  );

  return (
    <div className="relative flex flex-col w-full min-h-screen bg-white dark:bg-gray-900">
      <header className="sticky top-0 z-10 flex items-center justify-center w-full gap-2 p-4 bg-white shadow-md dark:bg-gray-900">
        <h1 className="font-urbanist text-[1.65rem] font-semibold text-center text-black dark:text-white">
          Rafiki Bot
        </h1>
      </header>

      {/* Main Content - Only renders the Chatbot if logged in */}
      <div className="flex flex-col justify-between flex-grow">
        {/* Navigate to login if user is not logged in */}
        <RouterProvider router={router} />
      </div>

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
    </div>
  );
}

export default App;
