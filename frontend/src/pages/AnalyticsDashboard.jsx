import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  BarChart3,
  Eye,
  Heart,
  MessageSquare,
  FileText,
  TrendingUp,
  Tag,
  Layers,
  ArrowLeft,
  RefreshCw
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const AnalyticsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/analytics/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching analytics:', err);
      setError('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="flex items-center gap-3">
          <RefreshCw className="h-6 w-6 animate-spin text-blue-600" />
          <span className="text-slate-600">Loading analytics...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">{error}</p>
          <Button onClick={fetchAnalytics}>Retry</Button>
        </div>
      </div>
    );
  }

  const overview = stats?.overview || {};
  const categories = stats?.categories || [];
  const topArticles = stats?.top_articles || [];
  const topTags = stats?.top_tags || [];
  const difficulties = stats?.difficulties || [];

  return (
    <div className="min-h-screen bg-slate-50 py-8" data-testid="analytics-dashboard">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              onClick={() => navigate('/admin')}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Admin
            </Button>
            <h1 className="text-2xl font-bold text-slate-800">Analytics Dashboard</h1>
          </div>
          <Button onClick={fetchAnalytics} variant="outline" className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        </div>

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <Card className="bg-gradient-to-br from-blue-500 to-blue-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100 text-sm">Total Articles</p>
                  <p className="text-3xl font-bold">{overview.total_articles?.toLocaleString()}</p>
                </div>
                <FileText className="h-10 w-10 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-500 to-green-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100 text-sm">Total Views</p>
                  <p className="text-3xl font-bold">{overview.total_views?.toLocaleString()}</p>
                </div>
                <Eye className="h-10 w-10 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-pink-500 to-pink-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-pink-100 text-sm">Total Likes</p>
                  <p className="text-3xl font-bold">{overview.total_likes?.toLocaleString()}</p>
                </div>
                <Heart className="h-10 w-10 text-pink-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-500 to-purple-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100 text-sm">Comments</p>
                  <p className="text-3xl font-bold">{overview.total_comments?.toLocaleString()}</p>
                </div>
                <MessageSquare className="h-10 w-10 text-purple-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-500 to-orange-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-orange-100 text-sm">This Week</p>
                  <p className="text-3xl font-bold">{overview.articles_this_week?.toLocaleString()}</p>
                </div>
                <TrendingUp className="h-10 w-10 text-orange-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Categories Distribution */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Layers className="h-5 w-5 text-blue-600" />
                Articles by Category
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {categories.slice(0, 10).map((cat, index) => {
                  const maxCount = categories[0]?.count || 1;
                  const percentage = (cat.count / maxCount) * 100;
                  return (
                    <div key={index} className="flex items-center gap-3">
                      <div className="w-32 text-sm text-slate-600 truncate capitalize">
                        {cat.name?.replace(/-/g, ' ')}
                      </div>
                      <div className="flex-1 bg-slate-100 rounded-full h-6 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full flex items-center justify-end pr-2 transition-all duration-500"
                          style={{ width: `${percentage}%` }}
                        >
                          <span className="text-xs text-white font-medium">{cat.count}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Difficulty Distribution */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-green-600" />
                Articles by Difficulty
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {difficulties.map((diff, index) => {
                  const colors = {
                    beginner: 'from-green-400 to-green-500',
                    intermediate: 'from-yellow-400 to-yellow-500',
                    advanced: 'from-red-400 to-red-500'
                  };
                  const maxCount = Math.max(...difficulties.map(d => d.count));
                  const percentage = (diff.count / maxCount) * 100;
                  return (
                    <div key={index} className="flex items-center gap-3">
                      <div className="w-28 text-sm text-slate-600 capitalize">{diff.name}</div>
                      <div className="flex-1 bg-slate-100 rounded-full h-8 overflow-hidden">
                        <div
                          className={`bg-gradient-to-r ${colors[diff.name] || 'from-slate-400 to-slate-500'} h-full rounded-full flex items-center justify-end pr-3 transition-all duration-500`}
                          style={{ width: `${percentage}%` }}
                        >
                          <span className="text-sm text-white font-bold">{diff.count}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Top Articles */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-purple-600" />
                Top 10 Most Viewed Articles
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {topArticles.map((article, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-lg font-bold text-slate-400">#{index + 1}</span>
                      <div>
                        <p className="font-medium text-slate-800 text-sm line-clamp-1">
                          {article.title}
                        </p>
                        <p className="text-xs text-slate-500 capitalize">
                          {article.category?.replace(/-/g, ' ')}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="flex items-center gap-1 text-slate-600">
                        <Eye className="h-4 w-4" />
                        {article.views?.toLocaleString()}
                      </span>
                      <span className="flex items-center gap-1 text-pink-500">
                        <Heart className="h-4 w-4" />
                        {article.likes?.toLocaleString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Top Tags */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Tag className="h-5 w-5 text-orange-600" />
                Popular Tags
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {topTags.map((tag, index) => {
                  const sizes = ['text-2xl', 'text-xl', 'text-lg', 'text-base', 'text-sm'];
                  const sizeClass = sizes[Math.min(Math.floor(index / 3), sizes.length - 1)];
                  const colors = [
                    'bg-blue-100 text-blue-700',
                    'bg-green-100 text-green-700',
                    'bg-purple-100 text-purple-700',
                    'bg-orange-100 text-orange-700',
                    'bg-pink-100 text-pink-700'
                  ];
                  return (
                    <span
                      key={index}
                      className={`px-3 py-1 rounded-full ${colors[index % colors.length]} ${sizeClass} font-medium`}
                    >
                      #{tag.name} ({tag.count})
                    </span>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
