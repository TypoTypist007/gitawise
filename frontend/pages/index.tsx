import React from 'react';
import { ChatInterface } from '../components/ChatInterface';

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-900">
      <header className="bg-slate-800 p-6 border-b border-slate-700">
        <h1 className="text-4xl font-bold text-purple-400">🕉️ GitaWise</h1>
        <p className="text-slate-400">Bhagavad Gita AI Companion</p>
      </header>
      <ChatInterface />
    </div>
  );
}
