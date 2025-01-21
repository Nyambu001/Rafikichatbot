import { useState, useEffect, useRef } from 'react';
import Message from './Message';
import InputField from './InputField';

function Chatbot({ isDarkMode }) {
  const [messages, setMessages] = useState([]); // Current chat's messages
  const [newMessage, setNewMessage] = useState(''); // New user input
  const [chats, setChats] = useState([]); // Array of all chats
  const messagesEndRef = useRef(null);

  // Load chat history from localStorage when the component mounts
  useEffect(() => {
    const savedChats = JSON.parse(localStorage.getItem('chats')) || [];
    setChats(savedChats); // Load past chats from localStorage
  }, []);

  // Update localStorage whenever the chats array is updated
  useEffect(() => {
    if (chats.length > 0) {
      localStorage.setItem('chats', JSON.stringify(chats)); // Save chat history
    }
  }, [chats]);

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
    if (messages.length > 0) {
      setChats(prevChats => [
        ...prevChats,
        { name: `Chat ${prevChats.length + 1}`, history: [...messages] },
      ]);
    }

    setMessages([]); // Clear current messages for a new conversation
    setNewMessage(''); // Clear input field
  };

  return (
    <div className={`flex flex-col h-screen ${isDarkMode ? 'dark' : ''}`}>
      {/* Start New Conversation button */}
      <div className="absolute z-50 top-4 left-4">
        <button
          onClick={startNewConversation}
          className="px-4 py-2 text-white bg-blue-500 rounded-lg shadow-md hover:bg-blue-400 focus:outline-none"
        >
          Start New Conversation
        </button>
      </div>

      {/* Chat Layout - Grid */}
      <div className="relative grid h-full grid-cols-1 gap-4 p-4 md:grid-cols-3">
        
        {/* Chat History Grid */}
        <div className="col-span-1 overflow-y-auto bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg max-h-[90vh]">
          <ul className="text-sm font-medium text-gray-900">
            {chats.map((chat, index) => (
              <li key={index}>
                <button
                  onClick={() => {
                    setMessages(chat.history); // Load the entire conversation history
                    setNewMessage(''); // Clear the input field
                  }}
                  className="block px-4 py-2 mt-1 bg-gray-100 rounded-md dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700"
                >
                  {chat.name}
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* Messages container with scrolling */}
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

      {/* Input field section at the bottom */}
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