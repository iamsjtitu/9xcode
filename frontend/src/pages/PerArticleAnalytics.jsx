import React, { useState, useEffect } from 'react';
import { BarChart3, Eye, ThumbsUp, TrendingUp, ArrowLeft, Search, ArrowUpDown, FileText, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { toast } from '../hooks/use-toast';
import axios from 'axios';
import { Link } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PerArticleAnalytics = () => {
  const [overview, setOverview] = useState(null);
  const [topArticles, setTopArticles] = useState([]);
  const [categoryStats, setCategoryStats] = useState([]);
  const [sortBy, setSortBy] = useState('views');
  const [searchFilter, setSearchFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleDetail, setArticleDetail] = useState(null);

  useEffect(() => {
    fetchData();
  }, [sortBy]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [overviewRes, articlesRes, catRes] = await Promise.all([
        axios.get(`${API}/article-analytics/overview`),
        axios.get(`${API}/article-analytics/top-articles?limit=50&sort_by=${sortBy}`),
        axios.get(`${API}/article-analytics/category-stats`),
      ]);
      setOverview(overviewRes.data);
      setTopArticles(articlesRes.data);
      setCategoryStats(catRes.data);
    } catch (err) {
      toast({ title: 'Error', description: 'Failed to load analytics', variant: 'destructive' });
    } finally {
      setLoading(false);
    }
  };

  const fetchArticleDetail = async (slug) => {
    try {
      const resp = await axios.get(`${API}/article-analytics/article/${slug}`);
      setArticleDetail(resp.data);
      setSelectedArticle(slug);
    } catch {
      toast({ title: 'Error', description: 'Failed to load article detail', variant: 'destructive' });
    }
  };

  const filtered = topArticles.filter(a =>
    a.title?.toLowerCase().includes(searchFilter.toLowerCase()) ||
    a.category?.toLowerCase().includes(searchFilter.toLowerCase())
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50" data-testid="article-analytics-page">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link to="/admin">
            <Button variant="outline" size="sm" data-testid="back-to-admin-btn">
              <ArrowLeft className="h-4 w-4 mr-1" /> Admin
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-2">
              <BarChart3 className="h-8 w-8 text-blue-600" />
              Per-Article Analytics
            </h1>
            <p className="text-slate-600 text-sm mt-1">Detailed performance metrics for every article</p>
          </div>
        </div>

        {/* Overview Cards */}
        {overview && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8" data-testid="overview-cards">
            <Card>
              <CardContent className="p-4 text-center">
                <FileText className="h-5 w-5 mx-auto text-blue-600 mb-1" />
                <p className="text-2xl font-bold text-slate-900">{overview.total_articles}</p>
                <p className="text-xs text-slate-500">Total Articles</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <Eye className="h-5 w-5 mx-auto text-green-600 mb-1" />
                <p className="text-2xl font-bold text-slate-900">{overview.total_views?.toLocaleString()}</p>
                <p className="text-xs text-slate-500">Total Views</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <ThumbsUp className="h-5 w-5 mx-auto text-red-600 mb-1" />
                <p className="text-2xl font-bold text-slate-900">{overview.total_likes?.toLocaleString()}</p>
                <p className="text-xs text-slate-500">Total Likes</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <TrendingUp className="h-5 w-5 mx-auto text-purple-600 mb-1" />
                <p className="text-2xl font-bold text-slate-900">{overview.avg_views}</p>
                <p className="text-xs text-slate-500">Avg Views</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <ThumbsUp className="h-5 w-5 mx-auto text-orange-600 mb-1" />
                <p className="text-2xl font-bold text-slate-900">{overview.avg_likes}</p>
                <p className="text-xs text-slate-500">Avg Likes</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <Eye className="h-5 w-5 mx-auto text-slate-400 mb-1" />
                <p className="text-2xl font-bold text-amber-600">{overview.zero_view_articles}</p>
                <p className="text-xs text-slate-500">Zero Views</p>
              </CardContent>
            </Card>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left - Category Stats */}
          <div className="space-y-6">
            <Card data-testid="category-stats-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Category Performance</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {categoryStats.map((cat, i) => {
                  const maxViews = Math.max(...categoryStats.map(c => c.total_views), 1);
                  const barWidth = (cat.total_views / maxViews) * 100;
                  return (
                    <div key={i} className="space-y-1" data-testid={`cat-stat-${cat.category}`}>
                      <div className="flex justify-between text-xs">
                        <span className="text-slate-700 capitalize font-medium">{cat.category?.replace(/-/g, ' ')}</span>
                        <span className="text-slate-500">{cat.count} articles</span>
                      </div>
                      <div className="h-5 bg-slate-100 rounded-full overflow-hidden relative">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all"
                          style={{ width: `${barWidth}%` }}
                        />
                        <span className="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-slate-700">
                          {cat.total_views.toLocaleString()} views
                        </span>
                      </div>
                    </div>
                  );
                })}
              </CardContent>
            </Card>

            {/* Article Detail */}
            {articleDetail && (
              <Card className="border-blue-200" data-testid="article-detail-card">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Article Detail</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <h3 className="font-bold text-slate-900 text-sm">{articleDetail.title}</h3>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="bg-blue-50 p-2 rounded">
                      <span className="text-slate-500">Views</span>
                      <p className="font-bold text-blue-700">{articleDetail.views?.toLocaleString()}</p>
                    </div>
                    <div className="bg-red-50 p-2 rounded">
                      <span className="text-slate-500">Likes</span>
                      <p className="font-bold text-red-700">{articleDetail.likes?.toLocaleString()}</p>
                    </div>
                    <div className="bg-green-50 p-2 rounded">
                      <span className="text-slate-500">Engagement</span>
                      <p className="font-bold text-green-700">{articleDetail.engagement_rate}%</p>
                    </div>
                    <div className="bg-purple-50 p-2 rounded">
                      <span className="text-slate-500">Steps</span>
                      <p className="font-bold text-purple-700">{articleDetail.steps_count}</p>
                    </div>
                    <div className="bg-orange-50 p-2 rounded col-span-2">
                      <span className="text-slate-500">Code Lines</span>
                      <p className="font-bold text-orange-700">{articleDetail.total_code_lines}</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    <Badge variant="outline" className="text-xs capitalize">{articleDetail.category?.replace(/-/g, ' ')}</Badge>
                    <Badge variant="outline" className="text-xs">{articleDetail.difficulty}</Badge>
                    {articleDetail.os?.map((o, j) => (
                      <Badge key={j} variant="secondary" className="text-xs">{o}</Badge>
                    ))}
                  </div>
                  <Link to={`/snippet/${articleDetail.slug}`} target="_blank">
                    <Button size="sm" variant="outline" className="w-full text-xs">
                      <ExternalLink className="h-3 w-3 mr-1" /> View Article
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right - Article Table */}
          <div className="lg:col-span-2">
            <Card data-testid="articles-table-card">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between flex-wrap gap-3">
                  <CardTitle className="text-lg">All Articles ({filtered.length})</CardTitle>
                  <div className="flex gap-2">
                    <div className="relative">
                      <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-3 w-3 text-slate-400" />
                      <Input
                        data-testid="article-search-input"
                        placeholder="Search articles..."
                        value={searchFilter}
                        onChange={(e) => setSearchFilter(e.target.value)}
                        className="pl-7 h-8 text-xs w-48"
                      />
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setSortBy(sortBy === 'views' ? 'likes' : 'views')}
                      data-testid="sort-toggle-btn"
                      className="text-xs h-8"
                    >
                      <ArrowUpDown className="h-3 w-3 mr-1" />
                      {sortBy === 'views' ? 'Views' : 'Likes'}
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs" data-testid="articles-table">
                    <thead>
                      <tr className="border-b text-left text-slate-500">
                        <th className="pb-2 pr-2">#</th>
                        <th className="pb-2 pr-4">Title</th>
                        <th className="pb-2 pr-2">Category</th>
                        <th className="pb-2 pr-2 text-right">Views</th>
                        <th className="pb-2 text-right">Likes</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filtered.map((a, i) => (
                        <tr
                          key={a.slug || i}
                          className={`border-b border-slate-100 hover:bg-blue-50/50 cursor-pointer transition-colors ${selectedArticle === a.slug ? 'bg-blue-50' : ''}`}
                          onClick={() => fetchArticleDetail(a.slug)}
                          data-testid={`article-row-${i}`}
                        >
                          <td className="py-2 pr-2 text-slate-400">{i + 1}</td>
                          <td className="py-2 pr-4">
                            <span className="font-medium text-slate-800 line-clamp-1">{a.title}</span>
                          </td>
                          <td className="py-2 pr-2">
                            <Badge variant="outline" className="text-[10px] capitalize">{a.category?.replace(/-/g, ' ')}</Badge>
                          </td>
                          <td className="py-2 pr-2 text-right font-mono text-slate-700">{a.views?.toLocaleString()}</td>
                          <td className="py-2 text-right font-mono text-slate-700">{a.likes?.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {filtered.length === 0 && (
                  <p className="text-center text-slate-400 py-8">No articles found</p>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerArticleAnalytics;
