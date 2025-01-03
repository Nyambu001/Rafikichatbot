import { useState, useEffect } from 'react';
import Chatbot from './interface/ChatBot';
import { MoonIcon, SunIcon } from '@heroicons/react/20/solid'; // Import Heroicons

function App() {
  // Initialize dark mode state from localStorage
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('theme') === 'dark');

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
      {/* Header with centered title */}
      <header className="sticky top-0 z-10 flex items-center justify-center w-full gap-2 p-4 bg-white shadow-md dark:bg-gray-900">
        <h1 className="font-urbanist text-[1.65rem] font-semibold text-center text-black dark:text-white">
          Rafiki Bot
        </h1>
      </header>

      {/* Chatbot content section */}
      <div className="flex flex-col justify-between flex-grow">
        <Chatbot isDarkMode={darkMode} /> {/* Pass dark mode state to Chatbot */}
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
