import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Message from './Message';
import InputField from './InputField';

function Chatbot({ isDarkMode }) {
  const [messages, setMessages] = useState([]); // Current chat's messages
  const [newMessage, setNewMessage] = useState(''); // New user input
  const [chats, setChats] = useState([]); // Array of all chats
  const [isLoggedIn, setIsLoggedIn] = useState(() => localStorage.getItem('isLoggedIn') === 'true'); // Fetch login status from localStorage
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  // Load chat history from localStorage when the component mounts
  useEffect(() => {
    if (isLoggedIn) {
      const savedChats = JSON.parse(localStorage.getItem('chats')) || [];
      setChats(savedChats); // Load past chats from localStorage
    }
  }, [isLoggedIn]);

  // Update localStorage whenever the chats array is updated
  useEffect(() => {
    if (isLoggedIn && chats.length > 0) {
      localStorage.setItem('chats', JSON.stringify(chats)); // Save chat history
    }
  }, [chats, isLoggedIn]);

  // Scroll to bottom whenever new message is added
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Function to handle new message submission
  const submitNewMessage = async () => {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage) return;

    // If it is the start of a new conversation, initialize a new chat entry
    if (messages.length === 0) {
      setMessages([{ role: 'user', content: trimmedMessage }]); // Add user’s first message
    } else {
      setMessages(prevMessages => [...prevMessages, { role: 'user', content: trimmedMessage }]); // Add to existing conversation
    }

    setNewMessage(''); // Clear the input field

    // Simulate generating the assistant's response after a delay
    setTimeout(() => {
      setMessages(prevMessages => {
        const updatedMessages = [...prevMessages];
        updatedMessages.push({ role: 'assistant', content: `Here's the assistant's response to: ${trimmedMessage}` });
        return updatedMessages;
      });
    }, 1000); // Simulated delay for assistant's response
  };

  // Function to start a new conversation
  const startNewConversation = () => {
    // Save the current conversation to the chat history before starting a new one
    if (messages.length > 0 && isLoggedIn) {
      setChats(prevChats => [
        ...prevChats,
        { name: `Chat ${prevChats.length + 1}`, history: [...messages] },
      ]);
    }

    setMessages([]); // Clear current messages for a new conversation
    setNewMessage(''); // Clear input field
  };

  // Handle Login
  const handleLogin = () => {
    setIsLoggedIn(true); // User is logged in
    localStorage.setItem('isLoggedIn', 'true'); // Store login status
    navigate('/login'); // Redirect to the chatbot page after login
  };
  
  

  // Handle Logout
  const handleLogout = () => {
    setIsLoggedIn(false); // Update state
    localStorage.removeItem('isLoggedIn'); // Remove the logged-in state from localStorage
    setChats([]); // Clear current chat history (optional)
    navigate('/login'); // Ensure the user is redirected to login
  };
 

  return (
    <div className={`flex flex-col h-screen ${isDarkMode ? 'dark' : ''}`}>
      {/* Header */}
      <header className="sticky top-0 z-50 flex justify-between p-4 bg-white shadow-md dark:bg-gray-900">
        <h1 className="text-xl font-bold text-gray-900 dark:text-white">Chatbot</h1>

        <div className="flex space-x-4">
          {!isLoggedIn && (
            <>
              <button
                onClick={handleLogin}
                className="px-4 py-2 text-white bg-blue-500 rounded-lg shadow-md hover:bg-blue-400"
              >
                Log In
              </button>
              <button
                onClick={() => navigate('/signup')} 
                className="px-4 py-2 text-white bg-green-500 rounded-lg shadow-md hover:bg-green-400"
              >
                Sign Up
              </button>
            </>
          )}
          {isLoggedIn && (
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-white bg-red-500 rounded-lg shadow-md hover:bg-red-400"
            >
              Log Out
            </button>
          )}
        </div>
      </header>

      {/* Start New Conversation button */}
      <div className="absolute z-50 top-4 left-20">
        <button
          onClick={startNewConversation}
          className="px-4 py-2 text-white bg-blue-500 rounded-lg shadow-md hover:bg-blue-400 focus:outline-none"
        >
          Start New Conversation
        </button>
      </div>

      {/* Chat Layout */}
      <div className="relative grid h-full grid-cols-1 gap-4 p-4 md:grid-cols-3">
        {/* Chat History Grid */}
        {isLoggedIn && (
          <div className="col-span-1 overflow-y-auto bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg max-h-[90vh]">
            <ul className="text-sm font-medium text-gray-900">
              {chats.map((chat, index) => (
                <li key={index}>
                  <button
                    onClick={() => {
                      setMessages(chat.history); // Load conversation history
                      setNewMessage(''); // Clear input field
                    }}
                    className="block px-4 py-2 mt-1 bg-gray-100 rounded-md dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700"
                  >
                    {chat.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Messages container */}
        <div className="flex-grow col-span-2 p-4 overflow-auto bg-white dark:bg-gray-900">
          {messages.length === 0 && (
            <div className="mt-3 space-y-2 text-xl font-light text-primary-blue dark:text-gray-300">
              <p>👋 Welcome! I'm here to help. Ask me anything.</p>
            </div>
          )}
          <Message messages={messages} />
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input field section */}
      <div className="p-4 bg-white dark:bg-gray-800 dark:border-gray-700">
        <InputField
          newMessage={newMessage}
          setNewMessage={setNewMessage}
          submitNewMessage={submitNewMessage}
          isDarkMode={isDarkMode}
        />
      </div>
    </div>
  );
}

export default Chatbot;
