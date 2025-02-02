
import { PaperAirplaneIcon } from '@heroicons/react/20/solid'; // Import paper airplane icon from Heroicons

function InputField({ newMessage, isLoading, setNewMessage, submitNewMessage, isDarkMode }) {

  // Adjusting the textarea height based on content
  const handleInputChange = (e) => {
    setNewMessage(e.target.value);
    e.target.style.height = 'auto'; // Reset the height to allow growth
    e.target.style.height = `${e.target.scrollHeight}px`; // Set the height to fit content
  };

  function handleKeyDown(e) {
    if (e.keyCode === 13 && !e.shiftKey && !isLoading) {
      e.preventDefault();
      submitNewMessage();
    }
  }

  return (
    <div className="p-1 bg-white py- dark:bg-gray-900">
      <div className="p-0 font-mono origin-bottom z-250 bg-primary-blue/35 rounded-3xl animate-chat duration-400">
        <div
          className={`pr-0.5 relative shrink-0 rounded-3xl overflow-hidden 
            ring-primary-blue ring-1 focus-within:ring-2 transition-all 
            ${isDarkMode ? 'bg-gray-800 ring-gray-700' : 'bg-white'}`}
        >
          <textarea
            className={`block w-full py-2 px-4 pr-11 
              resize-none rounded-2xl placeholder:text-primary-blue 
              focus:outline-none transition-all 
              ${isDarkMode
                ? 'bg-gray-800 placeholder:text-gray-400 text-gray-200'
                : 'bg-white placeholder:text-primary-blue text-black'}
            `}
            style={{ height: 'auto', minHeight: '40px', maxHeight: '140px' }} // Enabling flexible height up to a limit
            rows="1"
            value={newMessage}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type a message..."
          />
          <button
            className={`absolute p-2 -translate-y-1/2 rounded-md top-1/2 right-3 
              hover:bg-primary-blue/20 transition 
              ${isDarkMode ? 'text-gray-300' : 'text-primary-blue'}`}
            onClick={submitNewMessage}
          >
            <PaperAirplaneIcon className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default InputField;
