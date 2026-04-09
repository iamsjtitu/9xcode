import React, { useState } from 'react';
import { Github, Twitter, Mail, Send } from 'lucide-react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Footer = () => {
  const [email, setEmail] = useState('');
  const [subStatus, setSubStatus] = useState(null); // 'success' | 'error' | 'exists' | null
  const [submitting, setSubmitting] = useState(false);

  const handleSubscribe = async (e) => {
    e.preventDefault();
    if (!email.trim()) return;
    setSubmitting(true);
    setSubStatus(null);
    try {
      await axios.post(`${API}/newsletter/subscribe`, { email: email.trim() });
      setSubStatus('success');
      setEmail('');
    } catch (err) {
      if (err.response?.status === 409) setSubStatus('exists');
      else setSubStatus('error');
    } finally {
      setSubmitting(false);
    }
  };

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
                <Link to="/about" className="text-sm hover:text-blue-400 transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-sm hover:text-blue-400 transition-colors">
                  Contact Us
                </Link>
              </li>
              <li>
                <Link to="/contribute" className="text-sm hover:text-blue-400 transition-colors">
                  Contribute
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-semibold text-white mb-4">Legal</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/privacy-policy" className="text-sm hover:text-blue-400 transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link to="/terms-of-service" className="text-sm hover:text-blue-400 transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link to="/disclaimer" className="text-sm hover:text-blue-400 transition-colors">
                  Disclaimer
                </Link>
              </li>
              <li>
                <a href="https://9xcodes.com/api/seo/rss.xml" target="_blank" rel="noopener noreferrer" className="text-sm hover:text-blue-400 transition-colors">
                  RSS Feed
                </a>
              </li>
            </ul>
          </div>

          {/* Newsletter + Social */}
          <div>
            <h3 className="font-semibold text-white mb-4">Newsletter</h3>
            <p className="text-sm text-slate-400 mb-3">Get weekly updates on new tutorials.</p>
            <form onSubmit={handleSubscribe} className="flex gap-2" data-testid="footer-newsletter-form">
              <input
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => { setEmail(e.target.value); setSubStatus(null); }}
                required
                className="flex-1 px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 min-w-0"
                data-testid="footer-email-input"
              />
              <button
                type="submit"
                disabled={submitting}
                className="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex-shrink-0"
                data-testid="footer-subscribe-btn"
              >
                <Send className="h-4 w-4" />
              </button>
            </form>
            {subStatus === 'success' && <p className="text-xs text-green-400 mt-2">Subscribed successfully!</p>}
            {subStatus === 'exists' && <p className="text-xs text-amber-400 mt-2">Already subscribed!</p>}
            {subStatus === 'error' && <p className="text-xs text-red-400 mt-2">Something went wrong. Try again.</p>}
            <div className="flex space-x-4 mt-4">
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-blue-400 transition-colors">
                <Github className="h-5 w-5" />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-blue-400 transition-colors">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="mailto:contact@9xcodes.com" className="text-slate-400 hover:text-blue-400 transition-colors">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-slate-800 mt-8 pt-8 text-center text-sm text-slate-400">
          <p>&copy; 2026 9xCodes.com. All rights reserved.</p>
          <div className="flex justify-center gap-4 mt-2">
            <Link to="/privacy-policy" className="hover:text-blue-400 transition-colors">Privacy Policy</Link>
            <span>|</span>
            <Link to="/terms-of-service" className="hover:text-blue-400 transition-colors">Terms</Link>
            <span>|</span>
            <Link to="/disclaimer" className="hover:text-blue-400 transition-colors">Disclaimer</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;