import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const BASE_URL = 'https://diet-chatbot-backend-a7h3d6ayb4aze0d8.centralindia-01.azurewebsites.net';

function App() {
  const [input, setInput] = useState(""); // User input
  const [messages, setMessages] = useState([]); // Chat history
  const [isTyping, setIsTyping] = useState(false); // Typing indicator
  const chatContainerRef = useRef(null); // Ref to chat container

  // Scroll to the bottom of the chat container
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user's message to the chat
    setMessages((prev) => [...prev, { sender: "user", text: input }]);
    setInput(""); // Clear the input field
    setIsTyping(true); // Show typing indicator

    try {
      const response = await axios.post(`${BASE_URL}/chat`, {
        question: input,
      });

      // Format bot's response into paragraphs based on newlines
      const formattedResponse = response.data.answer.split("\n").map((line) => line.trim()).filter(Boolean);

      // Add bot's response to the chat
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: formattedResponse },
      ]);
    } catch (error) {
      console.error("Error communicating with chatbot:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: ["Sorry, something went wrong!"] },
      ]);
    }

    setIsTyping(false); // Hide typing indicator
  };

  return (
    <div
      className="container-fluid d-flex flex-column align-items-center justify-content-center vh-100"
      style={{
        backgroundImage: "url('/diet_veggies.jpg')", // Use your background image
        backgroundSize: "cover",
        backgroundPosition: "center",
        color: "#f8f9fa",
      }}
    >
      <div className="card w-75" style={{ backgroundColor: "#2c2c2c" }}>
        <div className="card-body">
          <h1 className="text-center mb-4" style={{ color: "#fff" }}>
            Diet Coach Chatbot
          </h1>
          <div
            ref={chatContainerRef} // Attach the ref to the chat container
            className="border rounded p-3"
            style={{
              maxHeight: "400px",
              overflowY: "auto",
              background: "#1c1c1c",
            }}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`d-flex ${
                  msg.sender === "user"
                    ? "justify-content-end"
                    : "justify-content-start"
                } mb-2`}
              >
                <div
                  className={`p-2 rounded ${
                    msg.sender === "user"
                      ? "bg-primary text-white"
                      : "bg-light text-dark"
                  }`}
                  style={{ maxWidth: "75%" }}
                >
                  {Array.isArray(msg.text) ? (
                    msg.text.map((line, idx) => <p key={idx}>{line}</p>)
                  ) : (
                    <p>{msg.text}</p>
                  )}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="text-muted text-center">
                <small>Bot is typing...</small>
              </div>
            )}
          </div>
          <div className="d-flex mt-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="form-control"
              placeholder="Type your message..."
              style={{
                backgroundColor: "#1c1c1c",
                color: "#fff",
                border: "1px solid #444",
              }}
            />
            <button
              onClick={sendMessage}
              className="btn btn-primary ms-2"
              disabled={!input.trim()}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
