
import React, { useState } from 'react';
import { TopicLink, ArticleCard } from '../components/BlogElements';
import { Link } from 'react-router-dom';

const Blog: React.FC = () => {
  const [activeTopic, setActiveTopic] = useState('All Posts');

  const topics = [
    { icon: "grid_view", label: "All Posts", count: 12 },
    { icon: "rocket_launch", label: "Product Updates", count: 4 },
    { icon: "code", label: "Engineering", count: 3 },
    { icon: "lightbulb", label: "Use Cases", count: 3 },
    { icon: "security", label: "Security", count: 2 },
  ];

  return (
    <div className="min-h-screen bg-background-dark">
      {/* Featured Header */}
      <section className="relative w-full border-b border-surface-lighter bg-surface-dark py-20 overflow-hidden">
        <div className="absolute right-0 top-0 h-full w-1/2 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/20 via-background-dark to-transparent opacity-50 blur-3xl"></div>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-16 lg:grid-cols-2 lg:items-center">
            <div className="flex flex-col gap-8">
              <div className="inline-flex w-fit items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary-light">
                <span className="size-2 rounded-full bg-primary animate-pulse"></span>
                Featured Announcement
              </div>
              <h1 className="font-display text-5xl font-bold leading-tight tracking-tight text-white lg:text-7xl">
                The Future of <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-primary-light">Tagging Intelligence</span>
              </h1>
              <p className="text-xl text-gray-400 max-w-xl leading-relaxed">
                Discover how AI tagging is the catalyst for full-cycle autonomous resolution.
              </p>
              <div className="flex flex-wrap gap-4 pt-4">
                <Link to="/blog/advantages-of-ticket-tagging-ai" className="group flex h-14 items-center justify-center gap-3 rounded-lg bg-white px-8 text-lg font-bold text-background-dark transition-transform hover:-translate-y-1">
                  Read Article
                  <span className="material-symbols-outlined text-2xl transition-transform group-hover:translate-x-1">arrow_forward</span>
                </Link>
              </div>
            </div>
            <div className="relative aspect-square w-full overflow-hidden rounded-2xl border border-surface-lighter bg-surface-lighter shadow-2xl">
              <img 
                src="https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=1000" 
                alt="Automation Abstract" 
                className="w-full h-full object-cover opacity-60 transition-transform duration-700 hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background-dark/90 via-transparent to-transparent"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Grid */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24">
        <div className="flex flex-col lg:flex-row gap-16">
          {/* Sidebar */}
          <aside className="w-full lg:w-80 flex-shrink-0 space-y-12">
            <div className="relative">
              <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-text-dim">search</span>
              <input 
                className="block w-full rounded-xl border border-surface-lighter bg-surface-dark py-4 pl-12 pr-4 text-sm text-white placeholder-text-dim focus:border-primary focus:ring-primary transition-all shadow-sm" 
                placeholder="Search articles..." 
                type="text" 
              />
            </div>
            
            <div className="sticky top-32">
              <h3 className="mb-6 font-display text-sm font-bold uppercase tracking-wider text-gray-400">Explore Topics</h3>
              <nav className="space-y-2">
                {topics.map((topic, i) => (
                  <button 
                    key={i} 
                    onClick={() => setActiveTopic(topic.label)}
                    className="w-full text-left"
                  >
                    <TopicLink 
                      icon={topic.icon} 
                      label={topic.label} 
                      count={topic.count} 
                      active={activeTopic === topic.label} 
                    />
                  </button>
                ))}
              </nav>

              <div className="mt-12 rounded-2xl border border-surface-lighter bg-surface-dark p-8 relative overflow-hidden">
                <div className="absolute -top-10 -right-10 w-32 h-32 bg-primary/10 rounded-full blur-2xl"></div>
                <div className="mb-6 flex size-12 items-center justify-center rounded-xl bg-primary/20 text-primary relative z-10">
                  <span className="material-symbols-outlined text-3xl">mail</span>
                </div>
                <h3 className="mb-3 font-display text-xl font-bold text-white relative z-10">Newsletter</h3>
                <p className="mb-6 text-sm text-text-dim relative z-10">Get engineering updates straight to your inbox.</p>
                <form className="space-y-4 relative z-10">
                  <input className="w-full rounded-xl border border-surface-lighter bg-background-dark px-4 py-3 text-sm text-white placeholder-text-dim focus:border-primary" placeholder="work@email.com" type="email"/>
                  <button className="w-full rounded-xl bg-white py-3 text-sm font-bold text-background-dark transition-colors hover:bg-gray-200">
                    Subscribe
                  </button>
                </form>
              </div>
            </div>
          </aside>

          {/* Articles Grid */}
          <div className="flex-1">
            <div className="mb-12 flex items-end justify-between border-b border-white/5 pb-6">
              <h2 className="font-display text-3xl font-bold text-white tracking-tight">Latest Articles</h2>
              <div className="flex items-center gap-2">
                <span className="text-xs text-text-dim">Sort by:</span>
                <select className="rounded border-none bg-transparent py-0 pl-2 pr-10 text-xs font-medium text-white focus:ring-0 cursor-pointer">
                  <option>Newest First</option>
                  <option>Oldest First</option>
                </select>
              </div>
            </div>
            
            <div className="grid gap-12 md:grid-cols-2">
              <Link to="/blog/advantages-of-ticket-tagging-ai" className="contents">
                <ArticleCard 
                  category="AI Strategy" 
                  title="The Advantages of using a Ticket Tagging AI" 
                  date="Mar 12" 
                  img="https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=400" 
                  desc="Consistency, speed, and privacy: Why high-fidelity ticket tagging is the cornerstone of support automation." 
                  tagColor="text-primary-light"
                  bgColor="bg-primary/10"
                />
              </Link>
              <ArticleCard 
                category="Engineering" 
                title="How we secure on-premise LLMs" 
                date="Oct 20" 
                img="https://picsum.photos/400/250?1" 
                desc="Dive into our architecture for air-gapped deployments and how we maintain zero-trust security." 
              />
              <ArticleCard 
                category="Release Notes" 
                title="v2.4: Improved German Language Support" 
                date="Oct 18" 
                img="https://picsum.photos/400/250?2" 
                desc="NLP models now handle complex German compound nouns with 99.8% accuracy." 
                tagColor="text-teal-400" 
                bgColor="bg-teal-500/10" 
              />
              <ArticleCard 
                category="Tutorial" 
                title="Automating Tier 1 tickets with zero hallucinations" 
                date="Oct 12" 
                img="https://picsum.photos/400/250?3" 
                desc="A step-by-step guide to setting up guardrails for your customer-facing AI agents." 
                tagColor="text-indigo-400" 
                bgColor="bg-indigo-500/10" 
              />
            </div>

            {/* Pagination Placeholder */}
            <div className="mt-20 flex justify-center gap-2">
              <button className="size-10 rounded-lg bg-surface-dark border border-white/5 flex items-center justify-center text-white hover:border-primary transition-all">1</button>
              <button className="size-10 rounded-lg bg-transparent border border-white/5 flex items-center justify-center text-slate-500 hover:text-white transition-all">2</button>
              <button className="size-10 rounded-lg bg-transparent border border-white/5 flex items-center justify-center text-slate-500 hover:text-white transition-all">3</button>
              <span className="flex items-center text-slate-700">...</span>
              <button className="size-10 rounded-lg bg-transparent border border-white/5 flex items-center justify-center text-slate-500 hover:text-white transition-all">10</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Blog;
