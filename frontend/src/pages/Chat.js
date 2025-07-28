
import React, { useState } from 'react';

function Chat() {
  const [prompt, setPrompt] = useState('');
  const [history, setHistory] = useState([]);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    const userMessage = { type: 'user', content: prompt };
    setHistory(prev => [...prev, userMessage]);
    setPrompt('');

    const res = await fetch('/api/mcp/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });

    const data = await res.json();
    const botMessage = {
      type: 'bot',
      content: data.error
        ? `Error: ${data.error}`
        : `SQL:
${data.sql}

Result:
${JSON.stringify(data.result, null, 2)}`
    };
    setHistory(prev => [...prev, botMessage]);
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Chat with Observability Assistant</h2>
      <div style={{
        border: '1px solid #ccc', padding: '1rem', maxHeight: '400px',
        overflowY: 'scroll', marginBottom: '1rem', background: '#f9f9f9'
      }}>
        {history.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: '1rem' }}>
            <strong>{msg.type === 'user' ? 'You' : 'Assistant'}:</strong>
            <pre style={{
              background: msg.type === 'bot' ? '#eef' : '#fff',
              padding: '0.5rem'
            }}>{msg.content}</pre>
          </div>
        ))}
      </div>
      <input
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        placeholder="Ask a question like 'Find slow spans from cart service'"
        style={{ width: '80%' }}
      />
      <button onClick={handleSubmit} style={{ marginLeft: '0.5rem' }}>Send</button>
    </div>
  );
}

export default Chat;
