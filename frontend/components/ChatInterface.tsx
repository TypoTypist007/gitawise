import React, { useState } from 'react';
import { askQuestion } from '../lib/api';
import { useChatStore } from '../lib/store';

export const ChatInterface: React.FC = () => {
  const { messages, addMessage, setLoading, loading } = useChatStore();
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    addMessage({ id: Date.now().toString(), role: 'user', content: input });
    setInput('');
    setLoading(true);

    try {
      const { data } = await askQuestion(input);
      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
      });
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-900">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`p-3 rounded ${
              msg.role === 'user' ? 'bg-blue-600 ml-auto' : 'bg-slate-700'
            } max-w-md`}
          >
            {msg.content}
          </div>
        ))}
      </div>

      <div className="border-t border-slate-700 p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={loading}
            className="flex-1 bg-slate-700 text-white rounded px-3 py-2"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
