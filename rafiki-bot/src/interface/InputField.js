import { PaperAirplaneIcon } from '@heroicons/react/20/solid'; 
import { PlusIcon } from "@heroicons/react/20/solid";

function InputField({ newMessage, isLoading, setNewMessage, submitNewMessage, startNewConversation, isDarkMode }) {
  const handleInputChange = (e) => {
    setNewMessage(e.target.value);
    e.target.style.height = 'auto'; 
    e.target.style.height = `${e.target.scrollHeight}px`; 
  };

  function handleKeyDown(e) {
    if (e.keyCode === 13 && !e.shiftKey && !isLoading) {
      e.preventDefault();
      submitNewMessage();
    }
  }

  return (
    <div className="sticky bottom-0 py-4 bg-white dark:bg-gray-900">
      <div className="p-1.5 font-mono origin-bottom z-50 bg-primary-blue/35 rounded-3xl animate-chat duration-400">
        <div
          className={`pr-0.5 relative shrink-0 rounded-3xl overflow-hidden 
            ring-primary-blue ring-1 focus-within:ring-2 transition-all 
            ${isDarkMode ? 'bg-gray-800 ring-gray-700' : 'bg-white'}`}
        >


<button
  className="absolute top-1/2 left-3 transform -translate-y-1/2 text-blue-500 z-50"
    onClick={() => {
    console.log("startNewConversation clicked!");
    if (startNewConversation) startNewConversation();
  }}>
  <PlusIcon className="w-6 h-6" />
</button>


          <textarea
            className={`block w-full py-2 px-4 pr-11
              resize-none rounded-2xl placeholder:text-primary-blue
              focus:outline-none transition-all
              ${isDarkMode
                ? 'bg-gray-800 placeholder:text-gray-400 text-gray-200'
                : 'bg-white placeholder:text-primary-blue text-black'}`}
            style={{ height: 'auto', minHeight: '40px', maxHeight: '140px', textAlign: 'center'}}
            rows="1"
            value={newMessage}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Andika ujumbe wako hapa ...."
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
