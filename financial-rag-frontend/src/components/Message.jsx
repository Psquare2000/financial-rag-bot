function Message({ text, sender }) {
    const isUser = sender === 'user';
    return (
      <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
        <div
          className={`px-4 py-2 rounded-lg max-w-[75%] text-sm whitespace-pre-wrap ${
            isUser
              ? 'bg-blue-600 text-white'
              : 'bg-gray-700 text-gray-200'
          }`}
        >
          {text}
        </div>
      </div>
    );
  }
  
  export default Message;
  