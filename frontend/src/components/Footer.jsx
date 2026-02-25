import React from 'react';
import { Terminal, Github, Twitter, Mail } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-b from-slate-900 to-slate-950 text-slate-300 border-t border-slate-800">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg blur opacity-75"></div>
                <div className="relative bg-gradient-to-br from-blue-600 via-blue-500 to-purple-600 p-2 rounded-lg">
                  <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold text-white">9xCodes</span>
                <span className="text-xs text-blue-400">Solve problems 9x faster</span>
              </div>
            </div>
            <p className="text-sm text-slate-400">
              Your ultimate resource for server commands, code snippets, and Linux tutorials.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-white mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-sm hover:text-blue-400 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/admin" className="text-sm hover:text-blue-400 transition-colors">
                  Admin Panel
                </Link>
              </li>
              <li>
                <a href="#" className="text-sm hover:text-blue-400 transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="text-sm hover:text-blue-400 transition-colors">
                  Contact
                </a>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="font-semibold text-white mb-4">Categories</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-sm hover:text-blue-400 transition-colors">
                  Installation
                </a>
              </li>
              <li>
                <a href="#" className="text-sm hover:text-blue-400 transition-colors">
                  Security
                </a>
              </li>
              <li>
                <a href="#" className="text-sm hover:text-blue-400 transition-colors">
                  Configuration
                </a>
              </li>
              <li>
                <a href="#" className="text-sm hover:text-blue-400 transition-colors">
                  Networking
                </a>
              </li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h3 className="font-semibold text-white mb-4">Connect</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors">
                <Github className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-400 hover:text-blue-400 transition-colors">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-slate-800 mt-8 pt-8 text-center text-sm text-slate-400">
          <p>&copy; 2025 9xCodes.com. All rights reserved. | Built for system administrators and developers.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;