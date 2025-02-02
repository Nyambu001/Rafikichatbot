const ChatHistory = ({ chats, loadChat, startNewConversation }) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow-lg dark:bg-gray-800">
      <h2 className="text-lg font-semibold text-primary-blue dark:text-gray-300">Chats</h2>
      <div className="mt-4">
        {/* Start New Conversation Button */}
        <button
          onClick={startNewConversation}
          className="w-full px-4 py-2 mb-4 text-white bg-blue-500 rounded-lg shadow-md hover:bg-blue-400 focus:outline-none"
        >
          Start New Conversation
        </button>

        <ul className="space-y-2">
          {chats.length > 0 ? (
            chats.map((chat, index) => (
              <li key={index} className="cursor-pointer" onClick={() => loadChat(chat.name)}>
                <div className="flex items-center p-3 space-x-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                  <div className="flex-grow">
                    <h3 className="font-medium text-primary-blue dark:text-gray-300">{chat.name}</h3>
                  </div>
                  <span className="text-sm text-gray-500 dark:text-gray-400">History</span>
                </div>
              </li>
            ))
          ) : (
            <li className="text-gray-500 dark:text-gray-400">No chats available.</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ChatHistory;
