import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Menu, X, LogOut, FileText } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { categories } from '../data/mockData';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Header = ({ onSearch }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [activeIdx, setActiveIdx] = useState(-1);
  const searchRef = useRef(null);
  const mobileSearchRef = useRef(null);
  const debounceRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    setIsAuthenticated(!!token);
  }, []);

  // Close suggestions on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (searchRef.current && !searchRef.current.contains(e.target) &&
          mobileSearchRef.current && !mobileSearchRef.current.contains(e.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const fetchSuggestions = (query) => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (query.length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }
    debounceRef.current = setTimeout(async () => {
      try {
        const res = await axios.get(`${API}/snippets/search-suggestions?q=${encodeURIComponent(query)}`);
        setSuggestions(res.data);
        setShowSuggestions(res.data.length > 0);
        setActiveIdx(-1);
      } catch {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    }, 250);
  };

  const handleInputChange = (e) => {
    const val = e.target.value;
    setSearchQuery(val);
    fetchSuggestions(val);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setShowSuggestions(false);
    if (onSearch) onSearch(searchQuery);
  };

  const handleSuggestionClick = (slug) => {
    setShowSuggestions(false);
    setSearchQuery('');
    navigate(`/snippet/${slug}`);
  };

  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIdx(prev => (prev < suggestions.length - 1 ? prev + 1 : 0));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIdx(prev => (prev > 0 ? prev - 1 : suggestions.length - 1));
    } else if (e.key === 'Enter' && activeIdx >= 0) {
      e.preventDefault();
      handleSuggestionClick(suggestions[activeIdx].slug);
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    setIsAuthenticated(false);
    navigate('/login');
  };

  const getCategoryName = (slug) => {
    const c = categories.find(cat => cat.slug === slug);
    return c ? c.name : slug;
  };

  const highlightMatch = (text, query) => {
    if (!query) return text;
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    return (
      <>
        {text.slice(0, idx)}
        <span className="text-blue-400 font-semibold">{text.slice(idx, idx + query.length)}</span>
        {text.slice(idx + query.length)}
      </>
    );
  };

  const SuggestionsDropdown = () => {
    if (!showSuggestions || suggestions.length === 0) return null;
    return (
      <div className="absolute top-full left-0 right-0 mt-1 bg-slate-800 border border-slate-600 rounded-lg shadow-2xl overflow-hidden z-50" data-testid="search-suggestions-dropdown">
        {suggestions.map((s, idx) => (
          <button
            key={s.slug}
            onClick={() => handleSuggestionClick(s.slug)}
            onMouseEnter={() => setActiveIdx(idx)}
            data-testid={`suggestion-${s.slug}`}
            className={`w-full text-left px-4 py-2.5 flex items-center gap-3 transition-colors ${
              idx === activeIdx ? 'bg-slate-700' : 'hover:bg-slate-700/50'
            }`}
          >
            <FileText className="h-4 w-4 text-slate-500 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-slate-200 truncate">{highlightMatch(s.title, searchQuery)}</p>
              <p className="text-xs text-slate-500 capitalize">{getCategoryName(s.category)}</p>
            </div>
          </button>
        ))}
        <div className="px-4 py-2 bg-slate-900/50 border-t border-slate-700">
          <p className="text-xs text-slate-500">Press Enter to search, ↑↓ to navigate</p>
        </div>
      </div>
    );
  };

  return (
    <header className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white sticky top-0 z-50 shadow-lg border-b border-slate-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition duration-300"></div>
              <div className="relative bg-gradient-to-br from-blue-600 via-blue-500 to-purple-600 p-3 rounded-xl shadow-lg">
                <svg className="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-extrabold bg-gradient-to-r from-blue-400 via-blue-300 to-purple-400 bg-clip-text text-transparent leading-none">
                9xCodes
              </span>
              <span className="text-xs text-blue-300 font-medium -mt-0.5">Solve problems 9x faster</span>
            </div>
          </Link>

          {/* Desktop Search */}
          <form onSubmit={handleSearch} className="hidden md:flex items-center flex-1 max-w-md mx-8" ref={searchRef}>
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
              <Input
                type="text"
                placeholder="Search commands, tutorials..."
                value={searchQuery}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                onFocus={() => { if (suggestions.length > 0) setShowSuggestions(true); }}
                className="pl-10 bg-slate-700 border-slate-600 text-white placeholder-slate-400 focus:border-blue-500"
                data-testid="search-input"
                autoComplete="off"
              />
              <SuggestionsDropdown />
            </div>
          </form>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-4">
            <Link to="/">
              <Button variant="ghost" className="text-white hover:bg-slate-700 hover:text-blue-400 transition-colors">
                Home
              </Button>
            </Link>
            {isAuthenticated ? (
              <>
                <Link to="/admin">
                  <Button variant="ghost" className="text-white hover:bg-slate-700 hover:text-blue-400 transition-colors">
                    Admin
                  </Button>
                </Link>
                <Link to="/admin/ads">
                  <Button variant="ghost" className="text-white hover:bg-slate-700 hover:text-blue-400 transition-colors">
                    Ads Manager
                  </Button>
                </Link>
                <Button 
                  onClick={handleLogout}
                  variant="ghost" 
                  className="text-white hover:bg-red-600 hover:text-white transition-colors"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </>
            ) : (
              <Link to="/login">
                <Button className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-md hover:shadow-blue-500/50 transition-all">
                  Admin Login
                </Button>
              </Link>
            )}
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-white"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Search */}
        <form onSubmit={handleSearch} className="md:hidden mt-4" ref={mobileSearchRef}>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
            <Input
              type="text"
              placeholder="Search commands..."
              value={searchQuery}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              onFocus={() => { if (suggestions.length > 0) setShowSuggestions(true); }}
              className="pl-10 bg-slate-700 border-slate-600 text-white placeholder-slate-400"
              autoComplete="off"
            />
            <SuggestionsDropdown />
          </div>
        </form>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <nav className="md:hidden mt-4 pb-4 space-y-2">
            <Link to="/" onClick={() => setIsMenuOpen(false)}>
              <Button variant="ghost" className="w-full text-left text-white hover:bg-slate-700">
                Home
              </Button>
            </Link>
            {isAuthenticated ? (
              <>
                <Link to="/admin" onClick={() => setIsMenuOpen(false)}>
                  <Button variant="ghost" className="w-full text-left text-white hover:bg-slate-700">
                    Admin
                  </Button>
                </Link>
                <Link to="/admin/ads" onClick={() => setIsMenuOpen(false)}>
                  <Button variant="ghost" className="w-full text-left text-white hover:bg-slate-700">
                    Ads Manager
                  </Button>
                </Link>
                <Button 
                  onClick={() => { handleLogout(); setIsMenuOpen(false); }}
                  variant="ghost" 
                  className="w-full text-left text-white hover:bg-red-600"
                >
                  <LogOut className="h-4 w-4 mr-2 inline" />
                  Logout
                </Button>
              </>
            ) : (
              <Link to="/login" onClick={() => setIsMenuOpen(false)}>
                <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
                  Admin Login
                </Button>
              </Link>
            )}
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;
