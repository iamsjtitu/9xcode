import React from 'react';
import { Badge } from './ui/badge';
import { 
  BookOpen, 
  Calculator, 
  Briefcase, 
  FileSpreadsheet, 
  FileText, 
  Presentation, 
  Image, 
  Monitor, 
  Server, 
  Laptop, 
  Apple,
  Camera,
  Video,
  Settings,
  Shield,
  Lock,
  Key,
  UserCheck,
  Globe,
  Radio,
  Wifi,
  Plug,
  Database,
  HardDrive,
  Cloud,
  Download,
  Code,
  Container,
  Layers,
  CreditCard,
  Receipt,
  ShoppingCart,
  Users,
  Mail,
  Package,
  Zap
} from 'lucide-react';

const UniversalSubcategories = ({ category, selectedSubcategory, onSubcategoryChange }) => {
  const subcategoryConfig = {
    learning: [
      { id: 'all', name: 'All', icon: BookOpen, tag: null },
      { id: 'tally', name: 'Tally', icon: Calculator, tag: 'tally' },
      { id: 'busy', name: 'Busy', icon: Briefcase, tag: 'busy' },
      { id: 'excel', name: 'MS Excel', icon: FileSpreadsheet, tag: 'excel' },
      { id: 'word', name: 'MS Word', icon: FileText, tag: 'word' },
      { id: 'powerpoint', name: 'PowerPoint', icon: Presentation, tag: 'powerpoint' },
      { id: 'photoshop', name: 'Photoshop', icon: Image, tag: 'photoshop' },
    ],
    computers: [
      { id: 'all', name: 'All', icon: Monitor, tag: null },
      { id: 'windows-server', name: 'Windows Server', icon: Server, tag: 'windows-server' },
      { id: 'windows', name: 'Windows', icon: Laptop, tag: 'windows' },
      { id: 'mac', name: 'macOS', icon: Apple, tag: 'mac' },
    ],
    'cctv-cameras': [
      { id: 'all', name: 'All', icon: Camera, tag: null },
      { id: 'cpplus', name: 'CP Plus', icon: Video, tag: 'cpplus' },
      { id: 'vigi', name: 'TP-Link VIGI', icon: Camera, tag: 'vigi' },
      { id: 'setup', name: 'Setup & Config', icon: Settings, tag: 'installation' },
    ],
    security: [
      { id: 'all', name: 'All', icon: Shield, tag: null },
      { id: 'firewall', name: 'Firewall', icon: Shield, tag: 'firewall' },
      { id: 'ssh', name: 'SSH', icon: Key, tag: 'ssh' },
      { id: 'ssl', name: 'SSL/TLS', icon: Lock, tag: 'ssl' },
      { id: 'authentication', name: 'Authentication', icon: UserCheck, tag: 'authentication' },
    ],
    networking: [
      { id: 'all', name: 'All', icon: Globe, tag: null },
      { id: 'router', name: 'Routers', icon: Radio, tag: 'router' },
      { id: 'vpn', name: 'VPN', icon: Lock, tag: 'vpn' },
      { id: 'lan', name: 'LAN Setup', icon: Plug, tag: 'lan' },
      { id: 'wifi', name: 'WiFi', icon: Wifi, tag: 'wifi' },
    ],
    database: [
      { id: 'all', name: 'All', icon: Database, tag: null },
      { id: 'mysql', name: 'MySQL', icon: Database, tag: 'mysql' },
      { id: 'postgresql', name: 'PostgreSQL', icon: Database, tag: 'postgresql' },
      { id: 'mongodb', name: 'MongoDB', icon: Layers, tag: 'mongodb' },
      { id: 'backup', name: 'Backup', icon: HardDrive, tag: 'backup' },
    ],
    installation: [
      { id: 'all', name: 'All', icon: Download, tag: null },
      { id: 'web-server', name: 'Web Servers', icon: Globe, tag: 'web-server' },
      { id: 'database', name: 'Databases', icon: Database, tag: 'database' },
      { id: 'development', name: 'Dev Tools', icon: Code, tag: 'development' },
      { id: 'docker', name: 'Docker', icon: Container, tag: 'docker' },
    ],
    virtualization: [
      { id: 'all', name: 'All', icon: Cloud, tag: null },
      { id: 'solusvm', name: 'SolusVM', icon: Server, tag: 'solusvm' },
      { id: 'virtualizor', name: 'Virtualizor', icon: Server, tag: 'virtualizor' },
      { id: 'proxmox', name: 'Proxmox', icon: Layers, tag: 'proxmox' },
      { id: 'vmware', name: 'VMware', icon: Cloud, tag: 'vmware' },
    ],
  };

  const subcategories = subcategoryConfig[category] || null;

  if (!subcategories) return null;

  const formatCategoryName = (cat) => {
    return cat.charAt(0).toUpperCase() + cat.slice(1).replace(/-/g, ' ');
  };

  return (
    <div className="mb-6 bg-white rounded-xl shadow-sm border border-slate-200 p-4">
      <h3 className="text-sm font-semibold text-slate-700 mb-3">
        {formatCategoryName(category)} Topics
      </h3>
      <div className="flex flex-wrap gap-2">
        {subcategories.map((subcat) => {
          const IconComponent = subcat.icon;
          return (
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
              <IconComponent className="h-4 w-4 mr-1.5" />
              {subcat.name}
            </Badge>
          );
        })}
      </div>
    </div>
  );
};

export default UniversalSubcategories;
