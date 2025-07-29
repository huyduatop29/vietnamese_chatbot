"use client";

import "./globals.css";
import { ReactNode, useState } from "react";
import { Bot, ChevronLeft, ChevronRight, Mail } from "lucide-react";

export default function RootLayout({ children }: { children: ReactNode }) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <html lang="en">
      <head>
        <title>ChatBox Agent App</title>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body
        className="h-screen overflow-hidden font-sans m-0 p-0 text-white"
        style={{
          backgroundImage: "url('/back_ground.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
          backgroundAttachment: "fixed",
        }}
      >
        {/* Sidebar */}
        <div
          className={`fixed top-0 left-0 h-full bg-black/60 border-r border-gray-700 transition-all duration-300 z-10 ${
            isCollapsed ? "w-12" : "w-60"
          }`}
        >
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="absolute top-4 right-[-20px] bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-full shadow z-20"
          >
            {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          </button>

          <div className="flex flex-col items-center space-y-4 mt-16 text-sm">
            <span className="text-gray-400">{isCollapsed ? "..." : "menu"}</span>
          </div>
        </div>

        {/* Main content area */}
        <div
          className={`transition-all duration-300 h-screen flex flex-col ${
            isCollapsed ? "ml-12" : "ml-60"
          }`}
        >
          {/* Header */}
          <header className="flex-shrink-0 text-center py-6">
            <h1 className="text-3xl md:text-5xl font-bold flex justify-center items-center gap-4 drop-shadow">
              ChatBot Agent <Bot size={50} />
            </h1>
          </header>

          {/* Main content - flexible height with proper scrolling */}
          <main className="flex-1 px-6 min-h-0">
            <div className="h-full max-w-7xl mx-auto bg-white/10 opacity-70 rounded-xl backdrop-blur-md flex flex-col">
              <div className="flex-1 overflow-y-auto border border-gray rounded-xl">
                {children}
              </div>
            </div>
          </main>

          {/* Footer */}
          <footer className="flex-shrink-0 text-center py-4 text-gray-300 flex justify-center items-center gap-2">
            <Mail size={16} />
            <span className="text-sm">quochuy@gmail.com</span>
          </footer>
        </div>
      </body>
    </html>
  );
}