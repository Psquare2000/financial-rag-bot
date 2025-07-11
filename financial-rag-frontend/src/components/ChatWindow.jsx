import { useState, useRef, useEffect } from 'react';
import Message from './Message';
import InputBox from './InputBox';

function ChatWindow() {
  const [messages, setMessages] = useState([
    { text: 'Hello! How can I help you today?', sender: 'bot' }
  ]);

  const messagesEndRef = useRef(null);

  const handleSend = async (text) => {
    setMessages((prev) => [...prev, { text, sender: 'user' }]);
  
    try {
      const res = await fetch('http://localhost:8088/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text })
      });
  
      const data = await res.json();
      setMessages((prev) => [...prev, { text: data.answer, sender: 'bot' }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [...prev, { text: 'Bot is currently unavailable.', sender: 'bot' }]);
    }
  };
  
  

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="h-screen w-screen bg-gray-900 flex flex-col">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-800">
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-gray-700 p-3 bg-gray-800">
        <InputBox onSend={handleSend} />
      </div>
    </div>
  );
}

export default ChatWindow;
