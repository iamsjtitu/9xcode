import React from 'react';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';

const UniversalSubcategories = ({ category, selectedSubcategory, onSubcategoryChange }) => {
  const subcategoryConfig = {
    learning: [
      { id: 'all', name: 'All', icon: '📚', tag: null },
      { id: 'tally', name: 'Tally', icon: '📊', tag: 'tally' },
      { id: 'busy', name: 'Busy', icon: '💼', tag: 'busy' },
      { id: 'excel', name: 'MS Excel', icon: '📗', tag: 'excel' },
      { id: 'word', name: 'MS Word', icon: '📘', tag: 'word' },
      { id: 'powerpoint', name: 'PowerPoint', icon: '📙', tag: 'powerpoint' },
      { id: 'photoshop', name: 'Photoshop', icon: '🎨', tag: 'photoshop' },
    ],
    computers: [
      { id: 'all', name: 'All', icon: '💻', tag: null },
      { id: 'windows-server', name: 'Windows Server', icon: '🖥️', tag: 'windows-server' },
      { id: 'windows', name: 'Windows', icon: '🪟', tag: 'windows' },
      { id: 'mac', name: 'macOS', icon: '🍎', tag: 'mac' },
    ],
    'cctv-cameras': [
      { id: 'all', name: 'All', icon: '📹', tag: null },
      { id: 'cpplus', name: 'CP Plus', icon: '📷', tag: 'cpplus' },
      { id: 'vigi', name: 'TP-Link VIGI', icon: '📸', tag: 'vigi' },
      { id: 'setup', name: 'Setup & Config', icon: '⚙️', tag: 'installation' },
    ],
    security: [
      { id: 'all', name: 'All', icon: '🔒', tag: null },
      { id: 'firewall', name: 'Firewall', icon: '🛡️', tag: 'firewall' },
      { id: 'ssh', name: 'SSH', icon: '🔑', tag: 'ssh' },
      { id: 'ssl', name: 'SSL/TLS', icon: '🔐', tag: 'ssl' },
      { id: 'authentication', name: 'Authentication', icon: '👤', tag: 'authentication' },
    ],
    networking: [
      { id: 'all', name: 'All', icon: '🌐', tag: null },
      { id: 'router', name: 'Routers', icon: '📡', tag: 'router' },
      { id: 'vpn', name: 'VPN', icon: '🔒', tag: 'vpn' },
      { id: 'lan', name: 'LAN Setup', icon: '🔌', tag: 'lan' },
      { id: 'wifi', name: 'WiFi', icon: '📶', tag: 'wifi' },
    ],
    database: [
      { id: 'all', name: 'All', icon: '🗄️', tag: null },
      { id: 'mysql', name: 'MySQL', icon: '🐬', tag: 'mysql' },
      { id: 'postgresql', name: 'PostgreSQL', icon: '🐘', tag: 'postgresql' },
      { id: 'mongodb', name: 'MongoDB', icon: '🍃', tag: 'mongodb' },
      { id: 'backup', name: 'Backup', icon: '💾', tag: 'backup' },
    ],
    installation: [
      { id: 'all', name: 'All', icon: '📥', tag: null },
      { id: 'web-server', name: 'Web Servers', icon: '🌐', tag: 'web-server' },
      { id: 'database', name: 'Databases', icon: '🗄️', tag: 'database' },
      { id: 'development', name: 'Dev Tools', icon: '👨‍💻', tag: 'development' },
      { id: 'docker', name: 'Docker', icon: '🐳', tag: 'docker' },
    ],
  };

  const subcategories = subcategoryConfig[category] || null;

  if (!subcategories) return null;

  return (
    <div className=\"mb-6 bg-white rounded-xl shadow-sm border border-slate-200 p-4\">
      <h3 className=\"text-sm font-semibold text-slate-700 mb-3\">
        {category.charAt(0).toUpperCase() + category.slice(1).replace('-', ' ')} Topics
      </h3>
      <div className=\"flex flex-wrap gap-2\">
        {subcategories.map((subcat) => (
          <Badge
            key={subcat.id}
            onClick={() => onSubcategoryChange(subcat.tag)}
            className={`cursor-pointer text-sm px-4 py-2 transition-all hover:scale-105 ${
              selectedSubcategory === subcat.tag
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white border-blue-600 shadow-md hover:shadow-lg'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-blue-50 hover:border-blue-400'
            }`}
            style={{ borderWidth: '1px' }}
          >
            <span className=\"mr-1.5\">{subcat.icon}</span>
            {subcat.name}
          </Badge>
        ))}
      </div>
    </div>
  );
};

export default UniversalSubcategories;
