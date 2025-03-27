import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBars, FaTimes, FaPlus, FaEdit,FaSignOutAlt } from 'react-icons/fa';
import { PaperAirplaneIcon } from '@heroicons/react/20/solid';

function Chatbot({ isDarkMode }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedChatId, setSelectedChatId] = useState(null);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  //new

  

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

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
        setChats(data.chats || []);
        if (data.chats?.length > 0) {
          setSelectedChatId(data.chats[0].conversation_id);
          const savedMessages = JSON.parse(localStorage.getItem(`chat_${data.chats[0].conversation_id}`)) || data.chats[0].messages || [];
          setMessages(savedMessages);
        }
      } else {
        setChats([]);
        setSelectedChatId(null);
        setMessages([]);
        setError(data.error || 'Failed to fetch chat history');
      }
    } catch {
      setError('Error fetching chat history');
    } finally {
      setLoading(false);
    }
  };
  

  function handleKeyDown(e) {
    if (e.keyCode === 13 && !e.shiftKey && !loading) {
      e.preventDefault();
      submitNewMessage();
    }
  }

  const startNewConversation = async () => {
    setMessages([]);
    setNewMessage('');
    setSelectedChatId(null);
  
    const userId = localStorage.getItem('userId');
    if (!userId) return;
  
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch('http://127.0.0.1:8000/start_chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ user_id: userId })
      });
  
      const data = await response.json();
      if (response.ok) {
        setChats(prev => [...prev, data]); // Update state immediately
        setSelectedChatId(data.conversation_id);
      }
    } catch (error) {
      console.error('Error starting new chat:', error);
    }
  };
  
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    navigate('/login');
  };
 

  
  
  const submitNewMessage = async () => {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage) return;
  
    // Update UI immediately with user message
    setMessages(prevMessages => {
      const updatedMessages = [
        ...prevMessages,
        { role: 'user', content: trimmedMessage }
      ];
      localStorage.setItem('chatMessages', JSON.stringify(updatedMessages)); // Save locally
      return updatedMessages;
    });
  
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
        setMessages(prevMessages => {
          const updatedMessages = [
            ...prevMessages,
            ...data.responses.map(resp => ({
              role: 'assistant',
              content: resp.content || 'No response',
            })),
          ];
          localStorage.setItem('chatMessages', JSON.stringify(updatedMessages)); // Save responses locally
          return updatedMessages;
        });
      }
  
    } catch (error) {
      alert('There was an error sending the message.');
    }
  };
  


  const handleChatSelect = (chat) => {
    setSelectedChatId(chat.conversation_id);
    setMessages(chat.messages.map(entry => ({ role: entry.role, content: entry.message || entry.content })));
  };

  return (
    <div className={`grid grid-cols-1 md:grid-cols-4 h-screen ${isDarkMode ? 'dark' : ''}`}>
      <Sidebar 
        chats={chats} 
        onSelect={handleChatSelect}
        isOpen={isMenuOpen} 
        onClose={() => setIsMenuOpen(false)} 
        selectedChatId={selectedChatId} 
        onLogout={handleLogout}
      />
      <button onClick={() => setIsMenuOpen(true)} className="p-2 md:hidden">
        <FaBars className="w-6 h-6 text-primary-blue" />
      </button>
      <div className="flex flex-col h-screen overflow-hidden bg-white md:col-span-3 dark:bg-gray-900">
        <div className="flex-grow p-4 overflow-auto">
          {messages.length === 0 && <div className="mt-3 space-y-2 text-xl font-light text-primary-blue dark:text-gray-300"><p>👋 Hey, how can I help?</p></div>}
          <Message messages={messages} />
          <div ref={messagesEndRef} />
        </div>
        <InputField 
          newMessage={newMessage} 
          setNewMessage={setNewMessage} 
          submitNewMessage={submitNewMessage} 
          isDarkMode={isDarkMode} 
          startNewConversation={startNewConversation}
          handleKeyDown={handleKeyDown} 
        />
      </div>
    </div>
  );
}

function Sidebar({ chats, onSelect, isOpen, onClose, selectedChatId ,onLogout}) {
  return (
    <div className={`fixed md:relative top-0 left-0 h-full w-64 bg-gray-100 dark:bg-gray-800 transition-transform duration-300 ease-in-out z-50 overflow-auto ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
      <div className="flex flex-col h-full p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="font-semibold">Rafiki Bot</div>
          <button onClick={onClose} className="p-2 rounded-full md:hidden hover:bg-gray-800">
            <FaTimes className="w-5 h-5" />
          </button>
        </div>
        <button onClick={onLogout} className="p-2 rounded-full hover:bg-gray-800">
          <FaSignOutAlt className="w-5 h-5 mr-2" /> 
        </button>
        <ul className="flex-1 overflow-auto">
          {chats.length > 0 ? chats.map((chat, index) => (
            <li key={chat.conversation_id}
              className={`flex items-center justify-between px-4 py-2 mt-1 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 ${
                selectedChatId === chat.conversation_id 
                  ? 'bg-gray-300 dark:bg-gray-600' 
                  : 'bg-gray-200 dark:bg-gray-700'
              }`}>
              <button onClick={() => onSelect(chat)} className="flex-grow text-left">{`Conversation ${index + 1}`}</button>
            </li>
          )) : <div>No conversations found</div>}
        </ul>
      </div>
    </div>
  );
}

function InputField({ newMessage, setNewMessage, submitNewMessage, isDarkMode, startNewConversation, handleKeyDown }) {
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "40px";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [newMessage]);

  return (
    <div className='p-4'>
      <div className='relative'>
        <textarea
          ref={textareaRef}
          className="w-full p-2 rounded-2xl resize-none h-auto min-h-[90px] max-h-[150px] overflow-y-auto dark:bg-gray-800"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
        />
        <button
          onClick={startNewConversation}
          className="absolute flex items-center w-6 h-6 text-white transition-all -translate-y-1/2 border-r rounded-full shadow-lg left-2 top-3/4 hover:bg-gray-300"
        >
          <FaPlus className="w-5 h-5 " />
        </button>
        <button onClick={submitNewMessage} className="absolute transform -translate-y-1/2 right-3 top-1/2">
          <PaperAirplaneIcon className="w-6 h-6 text-primary-blue rounded-" />
        </button>
      </div>
    </div>
  );
}

function Message({ messages }) {
  const [hoveredMessage, setHoveredMessage] = useState(null);
  const [editingMessageId, setEditingMessageId] = useState(null);
  const [editText, setEditText] = useState('');

  const handleEditClick = (idx, content) => {
    setEditingMessageId(idx);
    setEditText(content);
  };

  const handleEditSubmit = (id) => {
    console.log(`Updating message ${id} to: ${editText}`);
    setEditingMessageId(null);
  };

  return messages.map(({ role, content }, idx) => {
    const isUser = role === 'user';

    return (
      <div
        key={idx}
        className={` ${
          isUser
            ? 'bg-primary-blue/10 justify-end text-right text-primary-blue dark:text-white'
            : 'justify-start text-left  text-black dark:text-gray-200'
        }`}
        onMouseEnter={() => setHoveredMessage(idx)}
        onMouseLeave={() => setHoveredMessage(null)}
      >
        {hoveredMessage === idx && isUser && !editingMessageId && (
          <button
            onClick={() => handleEditClick(idx, content)}
            className="mr-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
          >
            <FaEdit className="w-4 h-4" />
          </button>
        )}

        <div className={`w-full message-content ${isUser ? 'ml-auto max-w-[80%]' : 'mr-auto max-w-[80%]'}`}>
          {editingMessageId === idx ? (
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                className="w-full p-1 border rounded-md dark:bg-gray-800"
              />
              <button
                onClick={() => handleEditSubmit(idx)}
                className="text-green-500 hover:text-green-700"
              >
                <PaperAirplaneIcon className="w-5 h-5" />
              </button>
              <button
                onClick={() => setEditingMessageId(null)}
                className="text-red-500 hover:text-red-700"
              >
                <FaTimes className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="break-words whitespace-pre-line">{content}</div>
          )}
        </div>
      </div>
    );
  });
}

export default Chatbot
 