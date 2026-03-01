import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Eye, Heart, MessageCircle, TrendingUp, Clock, Terminal, Flame, Bookmark, BookmarkCheck, Tag, ChevronLeft, ChevronRight } from 'lucide-react';
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import FilterSidebar from '../components/FilterSidebar';
import GoogleAd from '../components/GoogleAd';
import UniversalSubcategories from '../components/UniversalSubcategories';
import { categories, operatingSystems, difficultyLevels } from '../data/mockData';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Bookmark helpers
const getBookmarks = () => {
  try {
    return JSON.parse(localStorage.getItem('9xcodes_bookmarks') || '[]');
  } catch { return []; }
};
const toggleBookmark = (snippet) => {
  const bookmarks = getBookmarks();
  const exists = bookmarks.find(b => b.slug === snippet.slug);
  let updated;
  if (exists) {
    updated = bookmarks.filter(b => b.slug !== snippet.slug);
  } else {
    updated = [...bookmarks, { slug: snippet.slug, title: snippet.title, category: snippet.category, description: snippet.description }];
  }
  localStorage.setItem('9xcodes_bookmarks', JSON.stringify(updated));
  return updated;
};

const Home = ({ searchQuery, adsConfig }) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [filters, setFilters] = useState({});
  const [filteredSnippets, setFilteredSnippets] = useState([]);
  const [popularSnippets, setPopularSnippets] = useState([]);
  const [sortBy, setSortBy] = useState('recent');
  const [loading, setLoading] = useState(true);
  const [subcategory, setSubcategory] = useState(null);
  const [bookmarks, setBookmarks] = useState(getBookmarks());
  const [showBookmarks, setShowBookmarks] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const activeTag = searchParams.get('tag');

  useEffect(() => {
    fetchPopularSnippets();
  }, []);

  useEffect(() => {
    fetchSnippets();
  }, [filters, searchQuery, sortBy, subcategory, activeTag, page]);

  const fetchPopularSnippets = async () => {
    try {
      const response = await axios.get(`${API}/snippets/popular?limit=6`);
      setPopularSnippets(response.data);
    } catch (error) {
      console.error('Error fetching popular snippets:', error);
    }
  };

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
      if (subcategory) {
        params.append('tag', subcategory);
      }
      if (activeTag) {
        params.append('tag', activeTag);
      }
      params.append('sort', sortBy);
      params.append('page', page);
      params.append('limit', 12);
      const response = await axios.get(`${API}/snippets?${params.toString()}`);
      setFilteredSnippets(response.data.snippets);
      setTotalPages(response.data.pages);
      setTotalCount(response.data.total);
    } catch (error) {
      console.error('Error fetching snippets:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubcategoryChange = (tag) => {
    setSubcategory(tag);
    setPage(1);
  };

  const handleTagClick = (tag) => {
    setSearchParams({ tag });
    setPage(1);
  };

  const clearTagFilter = () => {
    setSearchParams({});
  };

  const handleBookmarkToggle = (snippet) => {
    const updated = toggleBookmark(snippet);
    setBookmarks(updated);
  };

  const isBookmarked = (slug) => bookmarks.some(b => b.slug === slug);

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

  const displaySnippets = showBookmarks
    ? filteredSnippets.filter(s => isBookmarked(s.slug))
    : filteredSnippets;

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
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-blue-300 to-blue-400 bg-clip-text text-transparent">
              Master Linux Server Commands
            </h1>
            <p className="text-base md:text-lg text-slate-300 mb-8">
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

      {/* Most Popular Articles */}
      {popularSnippets.length > 0 && !activeTag && !showBookmarks && (
        <section className="container mx-auto px-4 py-10" data-testid="popular-articles-section">
          <div className="flex items-center gap-2 mb-6">
            <Flame className="h-6 w-6 text-orange-500" />
            <h2 className="text-base md:text-lg font-bold text-slate-900">Most Popular Articles</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {popularSnippets.map((snippet) => (
              <Link key={snippet.slug} to={`/snippet/${snippet.slug}`} data-testid={`popular-article-${snippet.slug}`}>
                <Card className="h-full hover:shadow-lg transition-all duration-300 border-slate-200 hover:border-orange-300 group cursor-pointer">
                  <CardHeader className="pb-2">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge className="bg-blue-50 text-blue-700 border border-blue-200 text-xs">
                        {getCategoryName(snippet.category)}
                      </Badge>
                      <Badge
                        style={{
                          backgroundColor: `${getDifficultyColor(snippet.difficulty)}15`,
                          color: getDifficultyColor(snippet.difficulty),
                          borderColor: `${getDifficultyColor(snippet.difficulty)}30`,
                        }}
                        className="border capitalize text-xs"
                      >
                        {snippet.difficulty}
                      </Badge>
                    </div>
                    <CardTitle className="text-base font-bold text-slate-900 group-hover:text-orange-600 transition-colors line-clamp-2">
                      {snippet.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <p className="text-sm text-slate-500 line-clamp-2 mb-3">{snippet.description}</p>
                    <div className="flex items-center gap-4 text-xs text-slate-400">
                      <span className="flex items-center gap-1">
                        <Eye className="h-3.5 w-3.5" />
                        {snippet.views.toLocaleString()}
                      </span>
                      <span className="flex items-center gap-1">
                        <Heart className="h-3.5 w-3.5" />
                        {snippet.likes}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <FilterSidebar filters={filters} setFilters={setFilters} />
            {/* Bookmarks Toggle */}
            <button
              onClick={() => setShowBookmarks(!showBookmarks)}
              data-testid="bookmarks-toggle"
              className={`w-full mt-4 flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                showBookmarks
                  ? 'bg-amber-50 text-amber-700 border-2 border-amber-300 shadow-sm'
                  : 'bg-white text-slate-600 border border-slate-200 hover:border-amber-300 hover:text-amber-600'
              }`}
            >
              <BookmarkCheck className="h-4 w-4" />
              Saved Articles ({bookmarks.length})
            </button>
          </div>

          {/* Code Snippets */}
          <div className="flex-1">
            {/* Active Tag Filter Banner */}
            {activeTag && (
              <div className="flex items-center gap-2 mb-4 bg-blue-50 border border-blue-200 rounded-lg px-4 py-3" data-testid="active-tag-banner">
                <Tag className="h-4 w-4 text-blue-600" />
                <span className="text-sm text-blue-700">Filtering by tag: <strong>#{activeTag}</strong></span>
                <button
                  onClick={clearTagFilter}
                  className="ml-auto text-xs text-blue-600 hover:text-blue-800 font-medium underline"
                  data-testid="clear-tag-filter"
                >
                  Clear filter
                </button>
              </div>
            )}

            {/* Bookmarks Banner */}
            {showBookmarks && (
              <div className="flex items-center gap-2 mb-4 bg-amber-50 border border-amber-200 rounded-lg px-4 py-3">
                <BookmarkCheck className="h-4 w-4 text-amber-600" />
                <span className="text-sm text-amber-700">Showing your <strong>saved articles</strong></span>
              </div>
            )}

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
                  Showing <span className="font-semibold text-slate-900">{displaySnippets.length}</span> results
                </p>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-slate-600">Sort by:</span>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="text-sm border border-slate-300 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    data-testid="sort-select"
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
              ) : displaySnippets.length === 0 ? (
                <Card className="text-center py-12">
                  <CardContent>
                    <Terminal className="h-12 w-12 text-slate-300 mx-auto mb-4" />
                    <p className="text-slate-600">
                      {showBookmarks ? 'No saved articles yet. Bookmark articles to see them here!' : 'No code snippets found matching your criteria.'}
                    </p>
                  </CardContent>
                </Card>
              ) : (
                displaySnippets.map((snippet, index) => (
                  <React.Fragment key={snippet.id}>
                    <Card
                      className="hover:shadow-lg transition-all duration-300 border-slate-200 hover:border-blue-300 group"
                      data-testid={`snippet-card-${snippet.slug}`}
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
                          {/* Bookmark Button */}
                          <button
                            onClick={() => handleBookmarkToggle(snippet)}
                            data-testid={`bookmark-btn-${snippet.slug}`}
                            className={`flex-shrink-0 p-2 rounded-lg transition-all ${
                              isBookmarked(snippet.slug)
                                ? 'text-amber-500 bg-amber-50 hover:bg-amber-100'
                                : 'text-slate-400 hover:text-amber-500 hover:bg-slate-50'
                            }`}
                            title={isBookmarked(snippet.slug) ? 'Remove bookmark' : 'Save for later'}
                          >
                            {isBookmarked(snippet.slug) ? (
                              <BookmarkCheck className="h-5 w-5" />
                            ) : (
                              <Bookmark className="h-5 w-5" />
                            )}
                          </button>
                        </div>
                      </CardHeader>
                      <CardContent>
                        {/* Tags - Clickable */}
                        <div className="flex flex-wrap gap-2 mb-4">
                          {snippet.tags.map((tag, idx) => (
                            <button
                              key={idx}
                              onClick={() => handleTagClick(tag)}
                              data-testid={`tag-${tag}`}
                              className="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded-md hover:bg-blue-100 hover:text-blue-700 transition-colors cursor-pointer"
                            >
                              #{tag}
                            </button>
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
                            <button className="text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors" data-testid={`view-tutorial-${snippet.slug}`}>
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
