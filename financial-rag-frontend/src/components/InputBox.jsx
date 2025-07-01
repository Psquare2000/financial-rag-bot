import { useState } from 'react';

function InputBox({ onSend }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex border-t border-gray-700 p-4 bg-gray-800">
      <input
        type="text"
        className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
      />
      <button
        type="submit"
        className="ml-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 transition rounded-lg text-white"
      >
        Send
      </button>
    </form>
  );
}

export default InputBox;
