import React, { useState, useEffect, useRef, useCallback } from 'react';
import { ArrowLeft, Zap, CheckCircle2, XCircle, Loader2, Square, Play, Filter, ChevronLeft, ChevronRight, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from '../hooks/use-toast';
import axios from 'axios';
import { Link } from 'react-router-dom';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const BulkOptimize = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [optimizedCount, setOptimizedCount] = useState(0);
  const [totalArticles, setTotalArticles] = useState(0);

  const [selected, setSelected] = useState(new Set());
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState({});
  const [currentSlug, setCurrentSlug] = useState('');
  const [doneCount, setDoneCount] = useState(0);
  const [failCount, setFailCount] = useState(0);
  const stopRef = useRef(false);

  const fetchArticles = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page, limit: 50 });
      if (selectedCategory) params.append('category', selectedCategory);
      if (filterStatus) params.append('filter_status', filterStatus);
      const resp = await axios.get(`${API}/ai-rewrite/articles-for-optimize?${params}`);
      setArticles(resp.data.articles || []);
      setTotalPages(resp.data.pages || 1);
      setTotal(resp.data.total || 0);
      setCategories(resp.data.categories || []);
      setOptimizedCount(resp.data.optimized_count || 0);
      setTotalArticles(resp.data.total_articles || 0);
    } catch {
      toast({ title: 'Error', description: 'Could not load articles', variant: 'destructive' });
    } finally {
      setLoading(false);
    }
  }, [page, selectedCategory, filterStatus]);

  useEffect(() => { fetchArticles(); }, [fetchArticles]);

  const toggleSelect = (slug) => {
    setSelected(prev => {
      const next = new Set(prev);
      next.has(slug) ? next.delete(slug) : next.add(slug);
      return next;
    });
  };

  const selectAll = () => {
    const allSlugs = articles.map(a => a.slug);
    const allSelected = allSlugs.every(s => selected.has(s));
    if (allSelected) {
      setSelected(prev => {
        const next = new Set(prev);
        allSlugs.forEach(s => next.delete(s));
        return next;
      });
    } else {
      setSelected(prev => {
        const next = new Set(prev);
        allSlugs.forEach(s => next.add(s));
        return next;
      });
    }
  };

  const selectPending = () => {
    const pendingSlugs = articles.filter(a => !a.ai_optimized).map(a => a.slug);
    setSelected(new Set(pendingSlugs));
  };

  const startOptimize = async () => {
    const slugs = [...selected];
    if (slugs.length === 0) {
      toast({ title: 'No Selection', description: 'Select articles to optimize first', variant: 'destructive' });
      return;
    }
    setRunning(true);
    stopRef.current = false;
    setDoneCount(0);
    setFailCount(0);
    setResults({});

    let done = 0;
    let fail = 0;

    for (const slug of slugs) {
      if (stopRef.current) break;
      setCurrentSlug(slug);
      setResults(prev => ({ ...prev, [slug]: 'processing' }));

      try {
        await axios.post(`${API}/ai-rewrite/optimize-existing`, { slug });
        setResults(prev => ({ ...prev, [slug]: 'done' }));
        done++;
      } catch (err) {
        const detail = err.response?.data?.detail || 'Failed';
        setResults(prev => ({ ...prev, [slug]: `error:${detail}` }));
        fail++;
        if (err.response?.status === 402) {
          toast({ title: 'Balance Low', description: 'LLM key balance low. Go to Profile > Universal Key > Add Balance.', variant: 'destructive' });
          stopRef.current = true;
        }
      }
      setDoneCount(done);
      setFailCount(fail);
    }

    setRunning(false);
    setCurrentSlug('');
    if (!stopRef.current) {
      toast({ title: 'Bulk Optimize Complete!', description: `${done} optimized, ${fail} failed out of ${slugs.length}` });
    } else {
      toast({ title: 'Stopped', description: `Stopped after ${done + fail} articles. ${done} done, ${fail} failed.` });
    }
    fetchArticles();
  };

  const stopOptimize = () => {
    stopRef.current = true;
    toast({ title: 'Stopping...', description: 'Will stop after current article finishes' });
  };

  const getStatusIcon = (slug) => {
    const r = results[slug];
    if (!r) return null;
    if (r === 'processing') return <Loader2 className="h-4 w-4 animate-spin text-amber-500" />;
    if (r === 'done') return <CheckCircle2 className="h-4 w-4 text-green-500" />;
    if (r?.startsWith('error:')) return <XCircle className="h-4 w-4 text-red-500" />;
    return null;
  };

  const pendingPercent = totalArticles > 0 ? Math.round((optimizedCount / totalArticles) * 100) : 0;
  const processTotal = selected.size;
  const processPercent = processTotal > 0 ? Math.round(((doneCount + failCount) / processTotal) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50" data-testid="bulk-optimize-page">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <Link to="/admin">
            <Button variant="outline" size="sm" data-testid="back-to-admin-btn">
              <ArrowLeft className="h-4 w-4 mr-1" /> Admin
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-2">
              <Zap className="h-8 w-8 text-amber-500" />
              Bulk AI Optimize
            </h1>
            <p className="text-slate-600 text-sm mt-1">Optimize all articles with AI for unique content & better SEO</p>
          </div>
        </div>

        {/* Stats Bar */}
        <Card className="mb-6 border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50" data-testid="stats-bar">
          <CardContent className="p-4">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex items-center gap-6">
                <div>
                  <span className="text-xs text-slate-500 uppercase font-semibold">Total Articles</span>
                  <p className="text-2xl font-bold text-slate-900">{totalArticles}</p>
                </div>
                <div>
                  <span className="text-xs text-slate-500 uppercase font-semibold">AI Optimized</span>
                  <p className="text-2xl font-bold text-green-600">{optimizedCount}</p>
                </div>
                <div>
                  <span className="text-xs text-slate-500 uppercase font-semibold">Pending</span>
                  <p className="text-2xl font-bold text-amber-600">{totalArticles - optimizedCount}</p>
                </div>
              </div>
              <div className="w-48">
                <div className="flex justify-between text-xs text-slate-500 mb-1">
                  <span>Overall Progress</span>
                  <span>{pendingPercent}%</span>
                </div>
                <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all duration-500" style={{ width: `${pendingPercent}%` }} data-testid="overall-progress-bar" />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Running Progress */}
        {running && (
          <Card className="mb-6 border-blue-300 bg-blue-50/50" data-testid="running-progress-card">
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                  <div>
                    <p className="font-semibold text-slate-800">Processing: {doneCount + failCount} / {processTotal}</p>
                    <p className="text-xs text-slate-500">Current: {currentSlug}</p>
                  </div>
                </div>
                <Button size="sm" variant="destructive" onClick={stopOptimize} data-testid="stop-optimize-btn">
                  <Square className="h-3 w-3 mr-1 fill-current" /> Stop
                </Button>
              </div>
              <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full transition-all duration-300"
                  style={{ width: `${processPercent}%` }}
                  data-testid="process-progress-bar"
                />
              </div>
              {failCount > 0 && (
                <p className="text-xs text-red-500 mt-2 flex items-center gap-1">
                  <AlertTriangle className="h-3 w-3" /> {failCount} failed
                </p>
              )}
            </CardContent>
          </Card>
        )}

        {/* Controls */}
        <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
          <div className="flex items-center gap-2 flex-wrap">
            <Select value={selectedCategory} onValueChange={(v) => { setSelectedCategory(v === 'all' ? '' : v); setPage(1); }}>
              <SelectTrigger className="w-44" data-testid="category-filter">
                <Filter className="h-3 w-3 mr-1" />
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map(c => <SelectItem key={c} value={c}>{c.replace(/-/g, ' ')}</SelectItem>)}
              </SelectContent>
            </Select>
            <Select value={filterStatus} onValueChange={(v) => { setFilterStatus(v === 'all' ? '' : v); setPage(1); }}>
              <SelectTrigger className="w-40" data-testid="status-filter">
                <SelectValue placeholder="All Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="optimized">Optimized</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" size="sm" onClick={selectAll} data-testid="select-all-btn">
              {articles.length > 0 && articles.every(a => selected.has(a.slug)) ? 'Deselect All' : 'Select All'}
            </Button>
            <Button variant="outline" size="sm" onClick={selectPending} data-testid="select-pending-btn">
              Select Pending
            </Button>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="secondary" data-testid="selected-count">{selected.size} selected</Badge>
            <Button
              onClick={startOptimize}
              disabled={running || selected.size === 0}
              className="bg-amber-500 hover:bg-amber-600 text-white"
              data-testid="start-optimize-btn"
            >
              {running ? (
                <><Loader2 className="h-4 w-4 mr-2 animate-spin" /> Processing...</>
              ) : (
                <><Play className="h-4 w-4 mr-2" /> Optimize ({selected.size})</>
              )}
            </Button>
          </div>
        </div>

        {/* Articles Table */}
        <Card data-testid="articles-table-card">
          <CardContent className="p-0">
            {loading ? (
              <div className="flex items-center justify-center p-12">
                <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
              </div>
            ) : articles.length === 0 ? (
              <div className="text-center p-12 text-slate-500">No articles found</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b bg-slate-50 text-left">
                      <th className="p-3 w-10">
                        <input type="checkbox" checked={articles.every(a => selected.has(a.slug))} onChange={selectAll} className="rounded" data-testid="header-checkbox" />
                      </th>
                      <th className="p-3 text-xs font-semibold text-slate-600 uppercase">Title</th>
                      <th className="p-3 text-xs font-semibold text-slate-600 uppercase">Category</th>
                      <th className="p-3 text-xs font-semibold text-slate-600 uppercase">Views</th>
                      <th className="p-3 text-xs font-semibold text-slate-600 uppercase w-28">Status</th>
                      <th className="p-3 text-xs font-semibold text-slate-600 uppercase w-16">Result</th>
                    </tr>
                  </thead>
                  <tbody>
                    {articles.map((a) => (
                      <tr
                        key={a.slug}
                        className={`border-b hover:bg-slate-50 transition-colors ${currentSlug === a.slug ? 'bg-blue-50' : ''} ${results[a.slug] === 'done' ? 'bg-green-50/50' : ''}`}
                        data-testid={`article-row-${a.slug}`}
                      >
                        <td className="p-3">
                          <input
                            type="checkbox"
                            checked={selected.has(a.slug)}
                            onChange={() => toggleSelect(a.slug)}
                            disabled={running}
                            className="rounded"
                            data-testid={`checkbox-${a.slug}`}
                          />
                        </td>
                        <td className="p-3">
                          <span className="text-sm font-medium text-slate-800 line-clamp-1">{a.title}</span>
                        </td>
                        <td className="p-3">
                          <Badge variant="outline" className="text-xs capitalize">{(a.category || '').replace(/-/g, ' ')}</Badge>
                        </td>
                        <td className="p-3 text-sm text-slate-600">{a.views || 0}</td>
                        <td className="p-3">
                          {a.ai_optimized ? (
                            <Badge className="bg-green-100 text-green-700 text-xs">Optimized</Badge>
                          ) : (
                            <Badge className="bg-amber-100 text-amber-700 text-xs">Pending</Badge>
                          )}
                        </td>
                        <td className="p-3">
                          {getStatusIcon(a.slug)}
                          {results[a.slug]?.startsWith('error:') && (
                            <span className="text-xs text-red-500 block mt-0.5" title={results[a.slug].slice(6)}>Failed</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between p-3 border-t">
                <span className="text-xs text-slate-500">Page {page} of {totalPages} ({total} articles)</span>
                <div className="flex gap-1">
                  <Button size="sm" variant="outline" disabled={page <= 1} onClick={() => setPage(p => p - 1)} data-testid="prev-page-btn">
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="outline" disabled={page >= totalPages} onClick={() => setPage(p => p + 1)} data-testid="next-page-btn">
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Warning */}
        <p className="text-xs text-slate-400 mt-4 text-center">
          Each article uses AI credits. Optimize in batches to manage costs. You can stop anytime.
        </p>
      </div>
    </div>
  );
};

export default BulkOptimize;
