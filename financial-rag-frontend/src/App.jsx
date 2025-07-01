import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import LandingPage from "./components/LandingPage";


export default function App() {
  const [started, setStarted] = useState(false);

  return (
    <>
      {!started ? (
        <LandingPage onStart={() => setStarted(true)} />
      ) : (
        <ChatWindow />
      )}
    </>
  );
}
