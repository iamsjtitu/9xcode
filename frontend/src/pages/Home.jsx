import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Eye, Heart, MessageCircle, TrendingUp, Clock, Terminal } from 'lucide-react';
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import FilterSidebar from '../components/FilterSidebar';
import GoogleAd from '../components/GoogleAd';
import UniversalSubcategories from '../components/UniversalSubcategories';
import { categories, operatingSystems, difficultyLevels } from '../data/mockData';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = ({ searchQuery, adsConfig }) => {
  const [filters, setFilters] = useState({});
  const [filteredSnippets, setFilteredSnippets] = useState([]);
  const [sortBy, setSortBy] = useState('recent');
  const [loading, setLoading] = useState(true);
  const [subcategory, setSubcategory] = useState(null);

  useEffect(() => {
    fetchSnippets();
  }, [filters, searchQuery, sortBy, subcategory]);

  const fetchSnippets = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      
      if (filters.category && filters.category.length > 0) {
        params.append('category', filters.category[0]);
      }
      if (filters.os && filters.os.length > 0) {
        params.append('os', filters.os[0]);
      }
      if (filters.difficulty && filters.difficulty.length > 0) {
        params.append('difficulty', filters.difficulty[0]);
      }
      if (searchQuery && searchQuery.trim() !== '') {
        params.append('search', searchQuery);
      }
      
      // Add subcategory tag filter if selected
      if (subcategory) {
        params.append('tag', subcategory);
      }
      
      params.append('sort', sortBy);
      
      const response = await axios.get(`${API}/snippets?${params.toString()}`);
      setFilteredSnippets(response.data);
    } catch (error) {
      console.error('Error fetching snippets:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubcategoryChange = (tag) => {
    setSubcategory(tag);
  };

  const selectedCategory = filters.category && filters.category.length > 0 ? filters.category[0] : null;

  const getCategoryName = (slug) => {
    const category = categories.find((c) => c.slug === slug);
    return category ? category.name : slug;
  };

  const getDifficultyColor = (slug) => {
    const difficulty = difficultyLevels.find((d) => d.slug === slug);
    return difficulty ? difficulty.color : '#6B7280';
  };

  const getOSColor = (slug) => {
    const os = operatingSystems.find((o) => o.slug === slug);
    return os ? os.color : '#6B7280';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-16 border-b border-slate-700">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 px-4 py-2 rounded-full mb-6">
              <Terminal className="h-4 w-4 text-blue-400" />
              <span className="text-sm text-blue-400 font-medium">Solve Your Coding Problems in 9x Speed!</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-blue-300 to-blue-400 bg-clip-text text-transparent">
              Master Linux Server Commands
            </h1>
            <p className="text-xl text-slate-300 mb-8">
              Discover copy-ready commands, tutorials, and best practices for Ubuntu, CentOS, Debian, and more.
            </p>
            <div className="flex flex-wrap justify-center gap-6 text-sm">
              <div className="flex items-center space-x-2">
                <div className="bg-blue-500/20 p-2 rounded-lg">
                  <Terminal className="h-5 w-5 text-blue-400" />
                </div>
                <span className="text-slate-300">{filteredSnippets.length}+ Code Snippets</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="bg-blue-500/20 p-2 rounded-lg">
                  <TrendingUp className="h-5 w-5 text-blue-400" />
                </div>
                <span className="text-slate-300">Updated Daily</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="bg-blue-500/20 p-2 rounded-lg">
                  <Clock className="h-5 w-5 text-blue-400" />
                </div>
                <span className="text-slate-300">Step-by-Step Tutorials</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <FilterSidebar filters={filters} setFilters={setFilters} />
          </div>

          {/* Code Snippets */}
          <div className="flex-1">
            {/* Universal Subcategories */}
            {selectedCategory && (
              <UniversalSubcategories
                category={selectedCategory}
                selectedSubcategory={subcategory}
                onSubcategoryChange={handleSubcategoryChange}
              />
            )}

            {/* Sort Bar */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-6">
              <div className="flex items-center justify-between">
                <p className="text-sm text-slate-600">
                  Showing <span className="font-semibold text-slate-900">{filteredSnippets.length}</span> results
                </p>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-slate-600">Sort by:</span>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="text-sm border border-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="recent">Most Recent</option>
                    <option value="popular">Most Popular</option>
                    <option value="views">Most Viewed</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Snippets Grid */}
            <div className="space-y-6">
              {loading ? (
                <Card className="text-center py-12">
                  <CardContent>
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-slate-600">Loading code snippets...</p>
                  </CardContent>
                </Card>
              ) : filteredSnippets.length === 0 ? (
                <Card className="text-center py-12">
                  <CardContent>
                    <Terminal className="h-12 w-12 text-slate-300 mx-auto mb-4" />
                    <p className="text-slate-600">No code snippets found matching your criteria.</p>
                  </CardContent>
                </Card>
              ) : (
                filteredSnippets.map((snippet, index) => (
                  <React.Fragment key={snippet.id}>
                    <Card
                      className="hover:shadow-lg transition-all duration-300 border-slate-200 hover:border-blue-300 group"
                    >
                      <CardHeader>
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <div className="flex flex-wrap items-center gap-2 mb-2">
                              <Badge className="bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-100">
                                {getCategoryName(snippet.category)}
                              </Badge>
                              <Badge
                                style={{
                                  backgroundColor: `${getDifficultyColor(snippet.difficulty)}15`,
                                  color: getDifficultyColor(snippet.difficulty),
                                  borderColor: `${getDifficultyColor(snippet.difficulty)}30`,
                                }}
                                className="border capitalize"
                              >
                                {snippet.difficulty}
                              </Badge>
                              {snippet.os.slice(0, 2).map((os, idx) => (
                                <Badge
                                  key={idx}
                                  style={{
                                    backgroundColor: `${getOSColor(os)}15`,
                                    color: getOSColor(os),
                                    borderColor: `${getOSColor(os)}30`,
                                  }}
                                  className="border capitalize"
                                >
                                  {os}
                                </Badge>
                              ))}
                            </div>
                            <Link to={`/snippet/${snippet.slug}`}>
                              <CardTitle className="text-xl font-bold text-slate-900 group-hover:text-blue-600 transition-colors mb-2">
                                {snippet.title}
                              </CardTitle>
                            </Link>
                            <CardDescription className="text-slate-600">
                              {snippet.description}
                            </CardDescription>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        {/* Tags */}
                        <div className="flex flex-wrap gap-2 mb-4">
                          {snippet.tags.map((tag, idx) => (
                            <span
                              key={idx}
                              className="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded-md"
                            >
                              #{tag}
                            </span>
                          ))}
                        </div>

                        {/* Stats */}
                        <div className="flex items-center justify-between pt-4 border-t border-slate-200">
                          <div className="flex items-center space-x-4 text-sm text-slate-500">
                            <div className="flex items-center space-x-1 hover:text-blue-600 transition-colors">
                              <Eye className="h-4 w-4" />
                              <span>{snippet.views.toLocaleString()}</span>
                            </div>
                            <div className="flex items-center space-x-1 hover:text-red-500 transition-colors cursor-pointer">
                              <Heart className="h-4 w-4" />
                              <span>{snippet.likes}</span>
                            </div>
                            <div className="flex items-center space-x-1 hover:text-blue-600 transition-colors">
                              <MessageCircle className="h-4 w-4" />
                              <span>{snippet.comments || 0}</span>
                            </div>
                          </div>
                          <Link to={`/snippet/${snippet.slug}`}>
                            <button className="text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors">
                              View Tutorial →
                            </button>
                          </Link>
                        </div>
                      </CardContent>
                    </Card>
                    
                    {/* Display Ad after every 3rd snippet */}
                    {adsConfig?.enabled && adsConfig?.betweenSnippetsAdCode && (index + 1) % 3 === 0 && (
                      <div className="my-6">
                        <GoogleAd adCode={adsConfig.betweenSnippetsAdCode} className="flex justify-center" />
                      </div>
                    )}
                  </React.Fragment>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;