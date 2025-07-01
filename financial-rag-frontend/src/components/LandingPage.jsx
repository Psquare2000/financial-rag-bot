import { useEffect, useState } from "react";

function LandingPage({ onStart }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => setVisible(true), 100); // triggers fade-in
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className="h-screen w-screen bg-gray-900 text-white flex items-center justify-center">
      <div
        className={`flex flex-col items-center transition-opacity duration-700 ease-in-out ${
          visible ? "opacity-100" : "opacity-0"
        }`}
      >
        {/* Title */}
        <h1 className="text-4xl font-bold mb-4 text-center">
          Welcome to Financial RAG Bot
        </h1>

        {/* Subtitle */}
        <p className="mb-6 text-gray-400 text-lg text-center">
          Your personal assistant for all things finance.
        </p>

        {/* Start Button */}
        <button
          onClick={onStart}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 hover:scale-105 transition-all duration-300 text-white font-semibold rounded-md"
        >
          Get Started
        </button>
      </div>
    </div>
  );
}

export default LandingPage;
