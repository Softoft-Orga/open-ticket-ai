
import React, { useState, useEffect } from 'react';
import { GoogleGenAI } from "@google/genai";

// Removed local declare global for window.aistudio as the environment already provides it as AIStudio.

const MediaLab: React.FC = () => {
  const [prompt, setPrompt] = useState('An abstract high-tech visual representing "Tagging AI": a crystalline tree with glowing data nodes, 8k, dark purple and cyan aesthetic, cinematic lighting, sharp focus, digital art style.');
  const [size, setSize] = useState<'1K' | '2K' | '4K'>('1K');
  const [aspectRatio, setAspectRatio] = useState<'1:1' | '16:9' | '4:3'>('16:9');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImageUrl, setGeneratedImageUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loadingStep, setLoadingStep] = useState(0);

  const loadingMessages = [
    "Initializing Nano Banana Pro Engine...",
    "Sampling latent space for Tagging AI aesthetics...",
    "Refining crystalline structures...",
    "Injecting cybernetic luminescence...",
    "Upscaling to target resolution..."
  ];

  useEffect(() => {
    let interval: number;
    if (isGenerating) {
      interval = window.setInterval(() => {
        setLoadingStep((prev) => (prev + 1) % loadingMessages.length);
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [isGenerating]);

  const handleGenerate = async () => {
    setError(null);
    setIsGenerating(true);
    setGeneratedImageUrl(null);

    try {
      // Cast window to any to access aistudio and avoid TypeScript modifier/type conflicts with global definitions
      const aistudio = (window as any).aistudio;
      const hasKey = await aistudio.hasSelectedApiKey();
      if (!hasKey) {
        await aistudio.openSelectKey();
        // Proceeding assuming success as per guidelines to avoid race condition delays
      }

      // Initialize GoogleGenAI right before the call to ensure the latest API key is used
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const response = await ai.models.generateContent({
        model: 'gemini-3-pro-image-preview',
        contents: {
          parts: [{ text: prompt }],
        },
        config: {
          imageConfig: {
            aspectRatio: aspectRatio,
            imageSize: size
          },
          tools: [{ googleSearch: {} }] // Pro image model supports search for better realism
        },
      });

      let imageUrl = '';
      // Find the image part in the response as per best practices
      for (const part of response.candidates[0].content.parts) {
        if (part.inlineData) {
          imageUrl = `data:image/png;base64,${part.inlineData.data}`;
          break;
        }
      }

      if (imageUrl) {
        setGeneratedImageUrl(imageUrl);
      } else {
        throw new Error("No image part found in model response.");
      }
    } catch (err: any) {
      console.error("Generation error:", err);
      const msg = err.message || "";
      // Reset key selection state and prompt user again if billing/key is invalid
      if (msg.includes("Requested entity was not found")) {
        setError("API Key Error. Please re-select a valid billing-enabled API key.");
        await (window as any).aistudio.openSelectKey();
      } else {
        setError("An unexpected error occurred during generation. Please try again.");
      }
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-background-dark py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-[10px] font-black uppercase mb-4">
            <span className="material-symbols-outlined text-xs">auto_awesome</span>
            Nano Banana Pro Studio
          </div>
          <h1 className="text-4xl md:text-6xl font-black text-white mb-4 tracking-tighter">Media Lab</h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Generate high-fidelity enterprise visuals for Tagging AI and platform documentation.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* Controls */}
          <div className="lg:col-span-4 space-y-8">
            <div className="bg-surface-dark border border-white/5 rounded-2xl p-6">
              <label className="block text-xs font-black text-slate-500 uppercase tracking-widest mb-3">Creative Prompt</label>
              <textarea 
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full bg-background-dark border border-white/10 rounded-xl p-4 text-sm text-white placeholder-slate-700 h-40 focus:ring-1 focus:ring-primary focus:border-primary transition-all resize-none"
                placeholder="Describe the visual you want to create..."
              />
            </div>

            <div className="bg-surface-dark border border-white/5 rounded-2xl p-6">
              <label className="block text-xs font-black text-slate-500 uppercase tracking-widest mb-4">Output Configuration</label>
              
              <div className="space-y-6">
                <div>
                  <div className="text-[10px] text-slate-400 mb-2 font-bold">IMAGE SIZE</div>
                  <div className="grid grid-cols-3 gap-2">
                    {['1K', '2K', '4K'].map((s) => (
                      <button 
                        key={s}
                        onClick={() => setSize(s as any)}
                        className={`py-2 rounded-lg text-xs font-bold transition-all border ${size === s ? 'bg-primary border-primary text-white shadow-glow' : 'bg-background-dark border-white/10 text-slate-500 hover:border-white/20'}`}
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-[10px] text-slate-400 mb-2 font-bold">ASPECT RATIO</div>
                  <div className="grid grid-cols-3 gap-2">
                    {['1:1', '16:9', '4:3'].map((ar) => (
                      <button 
                        key={ar}
                        onClick={() => setAspectRatio(ar as any)}
                        className={`py-2 rounded-lg text-xs font-bold transition-all border ${aspectRatio === ar ? 'bg-primary border-primary text-white shadow-glow' : 'bg-background-dark border-white/10 text-slate-500 hover:border-white/20'}`}
                      >
                        {ar}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <button 
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full h-14 bg-gradient-to-r from-primary to-purple-600 rounded-2xl text-white font-black uppercase tracking-widest hover:scale-[1.02] active:scale-95 transition-all shadow-xl shadow-primary/20 flex items-center justify-center gap-3 disabled:opacity-50 disabled:grayscale"
            >
              {isGenerating ? (
                <span className="material-symbols-outlined animate-spin">refresh</span>
              ) : (
                <span className="material-symbols-outlined">rocket_launch</span>
              )}
              {isGenerating ? 'Generating...' : 'Generate Visual'}
            </button>

            {error && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-bold flex gap-3">
                <span className="material-symbols-outlined text-sm">error</span>
                {error}
              </div>
            )}
            
            <div className="text-[10px] text-slate-600 italic px-2">
              Requires a <a href="https://ai.google.dev/gemini-api/docs/billing" target="_blank" className="underline hover:text-primary">billing-enabled</a> API key.
            </div>
          </div>

          {/* Preview Area */}
          <div className="lg:col-span-8">
            <div className="bg-[#0a060d] border border-white/5 rounded-3xl aspect-video w-full relative flex items-center justify-center overflow-hidden shadow-2xl">
              {isGenerating ? (
                <div className="text-center p-12 animate-in fade-in duration-700">
                  <div className="size-16 mx-auto mb-8 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
                  <h3 className="text-xl font-bold text-white mb-2">{loadingMessages[loadingStep]}</h3>
                  <p className="text-slate-500 text-sm">The high-fidelity generation process takes roughly 30-60 seconds.</p>
                </div>
              ) : generatedImageUrl ? (
                <div className="w-full h-full relative group">
                  <img src={generatedImageUrl} className="w-full h-full object-contain animate-in zoom-in-95 duration-500" alt="Generated visual" />
                  <div className="absolute inset-x-0 bottom-0 p-6 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                    <a 
                      href={generatedImageUrl} 
                      download="open-ticket-ai-visual.png"
                      className="inline-flex items-center gap-2 bg-white text-black px-4 py-2 rounded-lg font-bold text-xs"
                    >
                      <span className="material-symbols-outlined text-sm">download</span>
                      Download Visual
                    </a>
                  </div>
                </div>
              ) : (
                <div className="text-center text-slate-700">
                  <span className="material-symbols-outlined text-6xl mb-4">image</span>
                  <p className="text-sm font-medium">Generation results will appear here.</p>
                </div>
              )}
            </div>

            <div className="mt-8 bg-surface-dark border border-white/5 rounded-2xl p-8">
              <h4 className="text-white font-bold mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">lightbulb</span>
                Pro Tips for Tagging AI Visuals
              </h4>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-500">
                <li className="flex gap-2 items-start">
                  <span className="size-1.5 rounded-full bg-primary mt-1 flex-shrink-0"></span>
                  Use words like "hierarchical", "taxonomy tree", or "glowing nodes" for core technology visuals.
                </li>
                <li className="flex gap-2 items-start">
                  <span className="size-1.5 rounded-full bg-primary mt-1 flex-shrink-0"></span>
                  For German engineering vibes, add "precision", "industrial", and "clean lines" to your prompt.
                </li>
                <li className="flex gap-2 items-start">
                  <span className="size-1.5 rounded-full bg-primary mt-1 flex-shrink-0"></span>
                  Nano Banana Pro (Gemini 3) is best for text within images—try "The words 'TAGGING AI' written in neon".
                </li>
                <li className="flex gap-2 items-start">
                  <span className="size-1.5 rounded-full bg-primary mt-1 flex-shrink-0"></span>
                  4K resolution is recommended for marketing-ready assets and slide presentations.
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MediaLab;
