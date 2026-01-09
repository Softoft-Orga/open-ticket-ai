
import React, { useState, useMemo } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface NavItem {
  label: string;
  to: string;
  icon?: string;
}

interface NavGroup {
  id: string;
  title: string;
  icon: string;
  items: NavItem[];
}

const DocsSidebar: React.FC<{ onClose?: () => void }> = ({ onClose }) => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedGroups, setExpandedGroups] = useState<string[]>(['tagging', 'ota', 'started']);

  const isActive = (path: string) => location.pathname === path;

  const docStructure: NavGroup[] = [
    {
      id: 'started',
      title: "Getting Started",
      icon: "rocket_launch",
      items: [
        { label: "Introduction", to: "/docs" },
        { label: "Quick Start Guide", to: "/docs/ota/getting-started" },
        { label: "Platform Overview", to: "/docs/overview" },
      ]
    },
    {
      id: 'tagging',
      title: "Ticket Tagging AI",
      icon: "psychology",
      items: [
        { label: "Engine Overview", to: "/docs/tagging-ai" },
        { label: "Taxonomy Design", to: "/docs/tagging-ai/taxonomy" },
        { label: "Model Training", to: "/docs/tagging-ai/training" },
        { label: "Benchmarking", to: "/docs/tagging-ai/benchmarking" },
        { label: "GPU Optimization", to: "/docs/tagging-ai/gpu" },
      ]
    },
    {
      id: 'ota',
      title: "Automation (OTA)",
      icon: "settings_suggest",
      items: [
        { label: "OTA Overview", to: "/docs/ota" },
        { label: "Rule Engine", to: "/docs/ota/rules" },
        { label: "Connectors", to: "/docs/ota/connectors" },
        { label: "Advanced Workflows", to: "/docs/ota/workflows" },
        { label: "Error Handling", to: "/docs/ota/errors" },
      ]
    },
    {
      id: 'integration',
      title: "Integration",
      icon: "cable",
      items: [
        { label: "REST API Reference", to: "/docs/api" },
        { label: "Webhooks", to: "/docs/webhooks" },
        { label: "OTRS / Znuny Setup", to: "/docs/integration/znuny" },
        { label: "Zammad Setup", to: "/docs/integration/zammad" },
        { label: "Custom Adapters", to: "/docs/integration/custom" },
      ]
    },
    {
      id: 'data',
      title: "Data & Privacy",
      icon: "database",
      items: [
        { label: "Synthetic Data Hub", to: "/docs/synthetic-data" },
        { label: "PII Masking", to: "/docs/privacy/masking" },
        { label: "Air-Gapped Config", to: "/docs/deployment/air-gapped" },
        { label: "Compliance (GDPR)", to: "/docs/compliance" },
      ]
    }
  ];

  const toggleGroup = (id: string) => {
    setExpandedGroups(prev => 
      prev.includes(id) ? prev.filter(g => g !== id) : [...prev, id]
    );
  };

  const filteredDocs = useMemo(() => {
    if (!searchQuery) return docStructure;
    return docStructure.map(group => ({
      ...group,
      items: group.items.filter(item => 
        item.label.toLowerCase().includes(searchQuery.toLowerCase())
      )
    })).filter(group => group.items.length > 0);
  }, [searchQuery]);

  return (
    <div className="flex flex-col h-full">
      {/* Search Filter */}
      <div className="px-4 mb-6 sticky top-0 bg-background-dark z-10 pt-1">
        <div className="relative group">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-sm group-focus-within:text-primary transition-colors">search</span>
          <input 
            type="text" 
            placeholder="Filter docs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-surface-dark border border-white/10 rounded-xl py-2 pl-9 pr-4 text-xs text-white placeholder-slate-600 focus:ring-1 focus:ring-primary focus:border-primary transition-all"
          />
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-2 pb-10">
        {filteredDocs.map((group) => (
          <div key={group.id} className="mb-2">
            <button 
              onClick={() => toggleGroup(group.id)}
              className="w-full flex items-center justify-between px-3 py-2 text-slate-400 hover:text-white transition-colors group"
            >
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-lg text-slate-600 group-hover:text-primary transition-colors">{group.icon}</span>
                <span className="text-[11px] font-black uppercase tracking-widest">{group.title}</span>
              </div>
              <span className={`material-symbols-outlined text-xs transition-transform duration-200 ${expandedGroups.includes(group.id) ? 'rotate-180' : ''}`}>expand_more</span>
            </button>
            
            <div className={`mt-1 overflow-hidden transition-all duration-300 ${expandedGroups.includes(group.id) ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'}`}>
              <div className="ml-4 pl-4 border-l border-white/5 space-y-1">
                {group.items.map((item, idx) => (
                  <Link
                    key={idx}
                    to={item.to}
                    onClick={onClose}
                    className={`block px-3 py-1.5 text-xs rounded-md transition-all ${
                      isActive(item.to)
                        ? 'text-primary-light font-bold bg-primary/5'
                        : 'text-slate-500 hover:text-slate-300 hover:translate-x-1'
                    }`}
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        ))}
        
        {filteredDocs.length === 0 && (
          <div className="px-4 py-8 text-center">
            <p className="text-xs text-slate-600 italic">No documentation found matching "{searchQuery}"</p>
          </div>
        )}
      </nav>
    </div>
  );
};

export default DocsSidebar;
