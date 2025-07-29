"use client";
import React, { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";
import { useTypewriter } from "./useTypewriter";

type Message = { sender: "user" | "bot"; text: string };

const MessageBubble = ({
  message,
  isLatestBot,
}: {
  message: Message;
  isLatestBot: boolean;
}) => {
  const displayedText =
    message.sender === "bot" && isLatestBot
      ? useTypewriter(message.text)
      : message.text;

  return (
    <div
      className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`max-w-xs px-4 py-2 rounded-xl whitespace-pre-wrap ${
          message.sender === "user"
            ? "bg-blue-600 text-white rounded-br-none"
            : "bg-gray-300 text-black rounded-bl-none"
        }`}
      >
        {displayedText}
      </div>
    </div>
  );
};

const ChatBoxOutput = () => {
  const [messages, setMessages] = useState<Message[]>([
    { sender: "bot", text: "Hello! I'm your assistant." },
  ]);
  const [userText, setUserText] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const handleSend = () => {
    if (!userText.trim()) return;

    const userMessage = { sender: "user", text: userText };
    setMessages((prev) => [...prev, userMessage]);

    const botResponse = "This is a simulated AI response...";
    const botMessage = { sender: "bot", text: botResponse };

    setTimeout(() => {
      setMessages((prev) => [...prev, botMessage]);
    }, 600);

    setUserText("");
  };

  const lastBotIndex = [...messages].reverse().findIndex((m) => m.sender === "bot");
  const total = messages.length;
  const latestBotIndex = lastBotIndex === -1 ? -1 : total - 1 - lastBotIndex;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col max-w-5xl mx-auto text-white">
      <div className="flex-1 space-y-2 p-4 pb-28">
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            message={msg}
            isLatestBot={msg.sender === "bot" && index === latestBotIndex}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="fixed bottom-0 left-0 w-full bg-black/80 rounded-xl backdrop-blur-md py-4 px-6">
        <div className="max-w-5xl mx-auto relative">
          <textarea
            placeholder="Type your message..."
            className="w-full px-10 p-4 pr-14 border border-gray rounded-xl resize-none text-white bg-white/1 backdrop-blur-sm placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={userText}
            onChange={(e) => setUserText(e.target.value)}
            rows={1}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button
            onClick={handleSend}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-green-500 hover:bg-green-600 text-white p-2 rounded-lg transition-colors"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBoxOutput;
