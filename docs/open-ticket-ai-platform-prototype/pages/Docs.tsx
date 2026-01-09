
import React, { useState, useRef, useEffect } from 'react';
import { DocCard, QuickLink } from '../components/DocElements';
import { GoogleGenAI } from "@google/genai";

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const Docs: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your Open Ticket AI assistant. How can I help you with our documentation today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: [...messages, { role: 'user', content: userMessage }].map(m => ({
          role: m.role === 'user' ? 'user' : 'model',
          parts: [{ text: m.content }]
        })),
        config: {
          systemInstruction: `You are the Open Ticket AI Documentation Expert.
          Use the following internal documentation to answer user queries.
          If the answer is found in the docs, you MUST cite the source and provide the specific link.

          DOCUMENTATION SOURCES:
          1. [Open Ticket Automation (OTA) Docs] - Focuses on helpdesk connectors (Znuny, OTOBO, Zammad), automation rules for routing, priority updates, and triggering tasks.
             Link: #/docs/ota
          2. [Tagging AI Docs] - Covers on-prem ticket classification, hierarchical tag schemas, multilingual support (EN/DE), and hardware sizing for local LLMs.
             Link: #/docs/tagging-ai
          3. [Synthetic Data Generator Docs] - Explains how to generate privacy-compliant support ticket datasets for model evaluation and training.
             Link: #/docs/synthetic-data

          RULES:
          - Always mention the source if you use its info.
          - Use Markdown for formatting.
          - Be professional, technical, and concise.
          - If a query is outside these docs, state that you can only answer questions related to Open Ticket AI products.`,
          temperature: 0.7,
        },
      });

      const assistantContent = response.text || "I'm sorry, I couldn't process that request.";
      setMessages(prev => [...prev, { role: 'assistant', content: assistantContent }]);
    } catch (error) {
      console.error("AI Chat Error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "I encountered an error connecting to the documentation engine. Please try again later." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background-dark py-24 relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary/5 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-900/10 rounded-full blur-[120px]"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            AI Assistant v2.4 Live
          </div>
          <h2 className="text-5xl md:text-7xl font-black tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400">
            Documentation
          </h2>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Ask our AI assistant anything about our products or browse the source documentation below.
          </p>
        </div>

        {/* AI Chat Interface */}
        <div className="w-full max-w-4xl mx-auto mb-24 relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-primary/30 to-purple-600/30 rounded-2xl blur opacity-20 transition duration-500"></div>
          <div className="relative flex flex-col bg-[#150c19] rounded-2xl border border-slate-700 shadow-2xl overflow-hidden h-[500px]">
            {/* Chat Messages */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4 cyber-scrollbar">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] rounded-2xl p-4 text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-primary text-white rounded-br-none'
                      : 'bg-surface-lighter text-slate-200 rounded-bl-none border border-white/5 shadow-inner'
                  }`}>
                    {msg.role === 'assistant' && (
                      <div className="flex items-center gap-2 mb-2 text-[10px] font-bold uppercase tracking-widest text-primary-light">
                        <span className="material-symbols-outlined text-xs">auto_awesome</span>
                        AI Docs Assistant
                      </div>
                    )}
                    <div className="whitespace-pre-wrap">
                      {msg.content.split('\n').map((line, i) => (
                        <p key={i} className={i > 0 ? 'mt-2' : ''}>
                          {line.split(/(\[.*?\]\(#.*?\))/g).map((part, pi) => {
                            const match = part.match(/\[(.*?)\]\((.*?)\)/);
                            if (match) {
                              return (
                                <a key={pi} href={match[2]} className="text-cyan-400 font-bold hover:underline">
                                  {match[1]}
                                </a>
                              );
                            }
                            return part;
                          })}
                        </p>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-surface-lighter text-slate-400 rounded-2xl rounded-bl-none p-4 text-sm animate-pulse flex items-center gap-2">
                    <span className="material-symbols-outlined animate-spin text-xs">refresh</span>
                    Analyzing sources...
                  </div>
                </div>
              )}
            </div>

            {/* Input Form */}
            <form onSubmit={handleSendMessage} className="p-4 bg-background-dark border-t border-slate-700 flex gap-3">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 bg-surface-dark border border-slate-700 rounded-xl px-4 py-3 text-white placeholder:text-slate-600 focus:ring-1 focus:ring-primary focus:border-primary transition-all text-sm"
                placeholder="Ask e.g. 'How do I integrate with Znuny?' or 'Does Tagging AI support German?'"
                type="text"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading}
                className="size-12 rounded-xl bg-primary hover:bg-primary-dark text-white flex items-center justify-center transition-all disabled:opacity-50"
              >
                <span className="material-symbols-outlined">send</span>
              </button>
            </form>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <DocCard
            icon="settings_suggest"
            title="Open Ticket Automation Docs"
            desc="Integration layer for OTOBO, Znuny/OTRS, and Zammad. Setup, connectors, and automation rules."
            link="Open Automation Docs"
            to="/docs/ota"
          />
          <DocCard
            icon="label_important"
            title="Tagging AI Docs"
            desc="On-prem ticket classification. Tag schema, output format, multilingual behavior, and hardware sizing."
            link="Open Tagging AI Docs"
          />
          <DocCard
            icon="database"
            title="Synthetic Data Docs"
            desc="Privacy-compliant support ticket generation. Schemas, export formats, and data privacy."
            link="Open Data Docs"
            to="/docs/synthetic-data"
          />
        </div>

        <div className="mt-24 pt-16 border-t border-slate-800 text-center">
          <h4 className="text-sm font-bold uppercase tracking-[0.2em] text-slate-500 mb-12">Quick Resources</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <QuickLink icon="rocket_launch" label="Deployment" />
            <QuickLink icon="verified_user" label="Security & Data Flow" />
            <QuickLink icon="build_circle" label="Troubleshooting" />
            <QuickLink icon="history_edu" label="Release Notes" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Docs;
