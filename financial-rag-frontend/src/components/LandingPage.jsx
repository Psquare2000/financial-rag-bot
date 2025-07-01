function LandingPage({ onStart }) {
    return (
      <div className="h-screen w-screen bg-gray-900 text-white flex flex-col justify-center items-center">
        <h1 className="text-3xl font-bold mb-4">Welcome to Financial RAG Bot</h1>
        <p className="mb-6 text-gray-300">Your personal assistant for financial queries.</p>
        <button
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded"
          onClick={onStart}
        >
          Get Started
        </button>
      </div>
    );
  }
  
  export default LandingPage;
  