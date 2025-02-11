import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Message from './Message';
import InputField from './InputField';

function Chatbot({ isDarkMode }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedChatId, setSelectedChatId] = useState(null);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchChatHistory();
  }, []);

  const fetchChatHistory = async () => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      setError('User ID not found');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://127.0.0.1:8000/chat_history/?user_id=${userId}`);
      const data = await response.json();

      if (response.ok) {
        if (Array.isArray(data.chats) && data.chats.length > 0) {
          setChats(data.chats);
          setSelectedChatId(data.chats[0].conversation_id);
          setMessages(data.chats[0].messages || []);
        } else {
          setChats([]);
          setSelectedChatId(null);
          setMessages([]);
        }
      } else {
        setError(data.error || 'Failed to fetch chat history');
      }
    } catch (error) {
      setError('Error fetching chat history');
    } finally {
      setLoading(false);
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setNewMessage('');
    setSelectedChatId(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    navigate('/login');
  };

  const submitNewMessage = async () => {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage) return;

    setMessages(prevMessages => [
      ...prevMessages,
      { role: 'user', content: trimmedMessage }
    ]);
    setNewMessage('');

    try {
      const token = localStorage.getItem('authToken');
      if (!token) return;

      const requestData = {
        message: trimmedMessage,
        conversation_id: selectedChatId || null,
      };

      const response = await fetch('http://localhost:8000/chatbot/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error('Error sending message to Django API');
      }

      const data = await response.json();

      if (data.responses && data.responses.length > 0) {
        setMessages(prevMessages => [
          ...prevMessages,
          ...data.responses.map(resp => ({
            role: 'assistant',
            content: data.responses[0].content ||'No response',
          })),
        ]);
      }

      fetchChatHistory();

    } catch (error) {
      alert('There was an error sending the message.');
    }
  };

  const handleChatSelect = (chat) => {
    setSelectedChatId(chat.conversation_id);
    setMessages(chat.messages.map(entry => ({
      role: entry.role,
      content: entry.message || entry.content,
    })));
  };

  return (
    <div className={`flex flex-col h-screen ${isDarkMode ? 'dark' : ''}`}>
      <div className="absolute z-50 top-4 left-4">
        <button
          onClick={startNewConversation}
          className="px-4 py-2 text-white bg-blue-500 rounded-lg shadow-md hover:bg-blue-400 focus:outline-none"
        >
          +
        </button>
      </div>

      <div className="absolute z-50 top-4 right-4">
        <button
          onClick={handleLogout}
          className="px-4 py-2 text-white bg-red-500 rounded-lg shadow-md hover:bg-red-400 focus:outline-none"
        >
          Logout
        </button>
      </div>

      <div className="relative grid h-full grid-cols-1 gap-4 p-4 md:grid-cols-3">
        <div className="col-span-1 overflow-y-auto bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg max-h-[90vh]">
          <h2 className="text-lg font-bold mb-4">Chat History</h2>
          {loading && <p>Loading chat history...</p>}
          {error && <p className="text-red-500">{error}</p>}
          <ul className="text-sm font-medium text-gray-900">
            {chats.length > 0 ? (
              chats.map((chat, index) => {
                const conversationLabel = `Conversation ${index + 1}`;
                return (
                  <li key={chat.conversation_id}>
                    <button
                      onClick={() => handleChatSelect(chat)}
                      className="block px-4 py-2 mt-1 bg-gray-100 rounded-md dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700"
                    >
                      <strong>{conversationLabel}</strong>
                    </button>
                  </li>
                );
              })
            ) : (
              <p>No chat history available.</p>
            )}
          </ul>
        </div>

        <div className="flex-grow col-span-2 p-4 overflow-auto bg-white dark:bg-gray-900">
          {messages.length === 0 && (
            <div className="mt-3 space-y-2 text-xl font-light text-primary-blue dark:text-gray-300">
              <p>👋 Hey, how can I help?</p>
            </div>
          )}
          <Message messages={messages} />
          <div ref={messagesEndRef} />
        </div>
      </div>

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
