import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Message from "./Message";
import InputField from "./InputField";
import PHQ9Form from "./PHQ9Form";
import GAD7Form from "./GAD7Form";
import { FiMenu } from "react-icons/fi";
import {FiArrowLeft } from "react-icons/fi";


function Chatbot({ isDarkMode }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [selectedChatId, setSelectedChatId] = useState(null);
  const [showQuestionnaireOptions, setShowQuestionnaireOptions] = useState(true);
  const [showPHQ9Form, setShowPHQ9Form] = useState(false);
  const [showGAD7Form, setShowGAD7Form] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const goBackToHome = () => {
    navigate("/");
  };



 useEffect(() => {
    fetchChatHistory();
  }, []);

const startNewConversation = () => {
    setShowQuestionnaireOptions(true);
    setShowPHQ9Form(false);
    setShowGAD7Form(false);


};



  const fetchChatHistory = async () => {
    const userId = localStorage.getItem("userId");
    if (!userId) {
      setError("User ID not found");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/chat_history/?user_id=${userId}`
      );
      const data = await response.json();

      if (response.ok) {
        setChats(data.chats || []);
      } else {
        setError(data.error || "Failed to fetch chat history");
      }
    } catch (error) {
      setError("Error fetching chat history");
    } finally {
      setLoading(false);
    }
  };



const handleSelectQuestionnaire = async (type) => {
  setShowQuestionnaireOptions(false);

  try {
    const token = localStorage.getItem("authToken");
    if (!token) return;

    const requestData = { type };

    const response = await fetch("http://localhost:8000/create_chat_session/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) throw new Error("Error creating chat session");

    const data = await response.json();
    setSelectedChatId(data.chat_id);

    if (type === "PHQ-9") {
      setShowPHQ9Form(true);
    } else if (type === "GAD-7") {
      setShowGAD7Form(true);
    } else if (type === "both") {
      setShowPHQ9Form(true);
      setShowGAD7Form("pending");
    }

  } catch (error) {
    console.error("Error creating chat session:", error);
  }
};


  const handleBack = () => {
    setShowQuestionnaireOptions(true);
    setShowPHQ9Form(false);
    setShowGAD7Form(false);


  };


  const sendMessageToBackend = async (message) => {
    try {
      const token = localStorage.getItem("authToken");
      if (!token) return;

      const requestData = {
        message: message,
        conversation_id: selectedChatId,
      };

      const response = await fetch("http://localhost:8000/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error("Error sending message");
      }

      const data = await response.json();
      if(!selectedChatId&&data.conversation_id){
      setSelectedChatId(data.conversation_id);
      }

      if (data.responses && data.responses.length > 0) {
        setMessages((prevMessages) => [
          ...prevMessages,
          ...data.responses.map((resp) => ({
            role: "assistant",
            content: resp.content || "No response",
          })),
        ]);
      }
      fetchChatHistory();
    } catch (error) {
      setError("There was an error sending the message. Please try again later.");
    }
  };

  const submitNewMessage = () => {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage) return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { role: "user", content: trimmedMessage },
    ]);
    setNewMessage("");

    sendMessageToBackend(trimmedMessage);
  };

 const handleSubmitScore = (combinedMessage) => {
    setMessages((prevMessages) => [
    ...prevMessages,
    { role: "user", content: combinedMessage },
  ]);

  sendMessageToBackend(combinedMessage);
};
const handleSkipQuestionnaire = async () => {
  await handleSelectQuestionnaire("skip");
  setShowQuestionnaireOptions(false);
};

  const handleChatSelect = (chat) => {
    setSelectedChatId(chat.conversation_id);
    setMessages(
      chat.messages.map((entry) => ({
        role: entry.role,
        content: entry.message || entry.content,
      }))
    );
    setShowQuestionnaireOptions(false);
    setShowPHQ9Form(false);
    setShowGAD7Form(false);
  };
   useEffect(() => {
    setTimeout(() => {
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
      }
    }, 100);
  }, [messages]);

 return (
    <div className={`flex flex-col h-screen ${isDarkMode ? "dark text-white" : ""}`}>
      <div className="w-5 h-5 absolute z-50 top-4 left-4 flex items-center space-x-4">
        <button
          onClick={() => setShowHistory(!showHistory)}
          className="text-xl text-gray-700 dark:text-white hover:text-gray-500"
        >
          <FiMenu />
        </button>
        <button
          onClick={() => {
            localStorage.removeItem("authToken");
            localStorage.removeItem("userId");
            navigate("/login");
          }}
          className="w-7 h-7 bg-white dark:bg-gray-900"
        >
          ⏻
        </button>
      </div>

      <div className={`grid h-full ${showHistory ? "grid-cols-[250px_auto]" : "grid-cols-1"} gap-4 p-4`}>
        {showHistory && (
          <div className="w-[250px] overflow-y-auto bg-white dark:bg-gray-800 dark:text-white p-4 rounded-lg shadow-lg">
            <h2 className="text-lg font-bold mb-4">Chat History</h2>
            {loading && <p>Loading chat history...</p>}
            {error && <p className="text-red-500">{error}</p>}
            <ul className="text-sm font-medium text-gray-900">
              {chats.length > 0 ? (
                chats.map((chat, index) => (
                  <li key={chat.conversation_id}>
                    <button
                      onClick={() => handleChatSelect(chat)}
                      className="block px-4 py-2 mt-1 bg-gray-100 rounded-md dark:bg-gray-800 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700"
                    >
                      <strong>Gumzo la {index + 1}</strong>
                    </button>
                  </li>
                ))
              ) : (
                <p className="text-md dark:text-white">No chat history available.</p>
              )}
            </ul>
          </div>
        )}
          <div className={`flex flex-col ${showHistory ? "col-span-1" : "col-span-1"} bg-white dark:bg-gray-900 rounded-lg shadow-lg h-full`}>
            {!showQuestionnaireOptions ? (
                       <button
              onClick={startNewConversation}
              className={`absolute top-12 z-20 transition-all duration-300
                          ${showHistory ? "left-[300px]" : "left-20"}`}
              title="Go Back"
            >
            ⬅️
          </button>
          ) : null}
          {/* Chat Messages - Scrollable */}
          <div className="flex-grow overflow-y-auto p-4" style={{ maxHeight: "calc(100vh - 150px)" }}>

            {showQuestionnaireOptions ? (
              <div className="flex flex-col items-center space-y-4">
                <h2 className="text-xl font-semibold text-center dark:text-white">
                  Je ungependa kushiriki katika dodoso la afya ya akili?
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <button
                    className="p-4 bg-blue-100 dark:bg-blue-800 dark:text-white rounded-lg shadow-md hover:bg-blue-200 dark:hover:bg-blue-700"
                    onClick={() => handleSelectQuestionnaire("PHQ-9")}
                  >
                    📋 PHQ-9
                    <p className="text-sm dark:text-white">mtihani wa unyongovu</p>
                  </button>
                  <button
                    className="p-4 bg-green-100 dark:text-white dark:bg-green-800 rounded-lg shadow-md hover:bg-green-200 dark:hover:bg-green-700"
                    onClick={() => handleSelectQuestionnaire("GAD-7")}
                  >
                    📋 GAD-7
                    <p className="text-sm dark:text-white">mtihani wa wasiwasi</p>
                  </button>
                  <button
                    className="p-4 bg-teal-100 dark:text-white dark:bg-teal-800 rounded-lg shadow-md hover:bg-teal-200 dark:hover:bg-teal-700"
                    onClick={() => handleSelectQuestionnaire("both")}
                  >
                    📋 zote mbili
                    <p className="text-sm dark:text-white">mitihani yote</p>
                  </button>
                  <button
                    className="p-4 bg-gray-100 dark:text-white dark:bg-gray-700 rounded-lg shadow-md hover:bg-gray-200 dark:hover:bg-gray-600"
                    onClick={() => handleSelectQuestionnaire("skip")}
                  >
                    🏃‍♂️‍➡️🏃‍♂️‍➡️️ Apana
                  </button>
                </div>
              </div>

            ) : showPHQ9Form ? (
              <PHQ9Form onSubmit={handleSubmitScore} onClose={() => setShowPHQ9Form(false)} />
            ) : showGAD7Form ? (
              <GAD7Form onSubmit={handleSubmitScore} onClose={() => setShowGAD7Form(false)} />
            ) : (
              <>
                <Message messages={messages} />
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

       {!showQuestionnaireOptions ? (
  <div className="relative bg-white dark:bg-gray-900 p-4 shadow-lg">
    <InputField
      startNewConversation={startNewConversation}
      newMessage={newMessage}
      setNewMessage={setNewMessage}
      submitNewMessage={submitNewMessage}
      isDarkMode={isDarkMode}
    />
  </div>
) : null}
        </div>
      </div>
    </div>
  );
}

export default Chatbot;