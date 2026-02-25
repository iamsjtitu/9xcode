import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Menu, X, Terminal, LogOut } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';

const Header = ({ onSearch }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('admin_token');
    setIsAuthenticated(!!token);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(searchQuery);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    setIsAuthenticated(false);
    navigate('/login');
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
          <form onSubmit={handleSearch} className="hidden md:flex items-center flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
              <Input
                type="text"
                placeholder="Search commands, tutorials..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-slate-700 border-slate-600 text-white placeholder-slate-400 focus:border-blue-500"
              />
            </div>
          </form>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-4">
            <Link to="/">
              <Button variant="ghost" className="text-white hover:bg-slate-700 hover:text-blue-400 transition-colors">
                Home
              </Button>
            </Link>
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
            <Button className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-md hover:shadow-blue-500/50 transition-all">
              Submit Code
            </Button>
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
        <form onSubmit={handleSearch} className="md:hidden mt-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
            <Input
              type="text"
              placeholder="Search commands..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-slate-700 border-slate-600 text-white placeholder-slate-400"
            />
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
            <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
              Submit Code
            </Button>
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;