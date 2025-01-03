import React from 'react';

function Message({ messages }) {
  return (
    <div className="space-y-4 grow">
      {messages.map(({ role, content }, idx) => {
        const isUser = role === 'user';

        return (
          <div
            key={idx}
            className={`flex items-start gap-4 py-3 px-4 rounded-xl ${
              isUser
                ? 'bg-primary-blue/10 justify-end text-right text-primary-blue dark:text-white'
                : 'justify-start text-left bg-gray-100 dark:bg-gray-800 text-black dark:text-gray-200'
            }`}
          >
            {/* Message content */}
            <div className="message-content">
              <div className="whitespace-pre-line">{content}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default Message;
