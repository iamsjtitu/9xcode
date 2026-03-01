import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import {
  Trash2, Search, ChevronLeft, ChevronRight, Download, FolderOpen,
  CheckSquare, Square, AlertCircle, FileText,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { toast } from '../hooks/use-toast';
import { categories } from '../data/mockData';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ManageArticles = () => {
  const [articles, setArticles] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [search, setSearch] = useState('');
  const [filterCat, setFilterCat] = useState('all');
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(new Set());
  const [bulkCategory, setBulkCategory] = useState('');

  const fetchArticles = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page, limit: 20 });
      if (search) params.append('search', search);
      if (filterCat && filterCat !== 'all') params.append('category', filterCat);
      const res = await axios.get(`${API}/articles/list?${params}`);
      setArticles(res.data.articles);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [page, search, filterCat]);

  useEffect(() => { fetchArticles(); }, [fetchArticles]);

  const toggleSelect = (slug) => {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug); else next.add(slug);
      return next;
    });
  };

  const selectAll = () => {
    if (selected.size === articles.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(articles.map(a => a.slug)));
    }
  };

  const handleBulkDelete = async () => {
    if (selected.size === 0) return;
    if (!window.confirm(`Delete ${selected.size} articles? This cannot be undone.`)) return;
    try {
      const res = await axios.post(`${API}/articles/bulk-delete`, { slugs: Array.from(selected) });
      toast({ title: 'Deleted', description: res.data.message });
      setSelected(new Set());
      fetchArticles();
    } catch (err) {
      toast({ title: 'Error', description: 'Failed to delete', variant: 'destructive' });
    }
  };

  const handleBulkCategory = async () => {
    if (selected.size === 0 || !bulkCategory) return;
    try {
      const res = await axios.post(`${API}/articles/bulk-category`, {
        slugs: Array.from(selected),
        category: bulkCategory,
      });
      toast({ title: 'Updated', description: res.data.message });
      setSelected(new Set());
      setBulkCategory('');
      fetchArticles();
    } catch (err) {
      toast({ title: 'Error', description: 'Failed to update', variant: 'destructive' });
    }
  };

  const handleExport = (format) => {
    window.open(`${API}/articles/export?format=${format}`, '_blank');
  };

  const getCategoryName = (slug) => {
    const cat = categories.find(c => c.slug === slug);
    return cat ? cat.name : slug;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <Link to="/admin" className="text-sm text-blue-600 hover:underline mb-2 inline-block">← Back to Admin</Link>
            <h1 className="text-3xl font-bold text-slate-900">Manage Articles</h1>
            <p className="text-slate-500 mt-1">{total} total articles</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => handleExport('csv')} data-testid="export-csv-btn">
              <Download className="h-4 w-4 mr-1" /> CSV
            </Button>
            <Button variant="outline" size="sm" onClick={() => handleExport('json')} data-testid="export-json-btn">
              <Download className="h-4 w-4 mr-1" /> JSON
            </Button>
          </div>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  placeholder="Search articles..."
                  value={search}
                  onChange={(e) => { setSearch(e.target.value); setPage(1); }}
                  className="pl-10"
                  data-testid="search-articles"
                />
              </div>
              <Select value={filterCat} onValueChange={(v) => { setFilterCat(v); setPage(1); }}>
                <SelectTrigger className="w-48" data-testid="filter-category">
                  <SelectValue placeholder="All Categories" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {categories.map(c => (
                    <SelectItem key={c.slug} value={c.slug}>{c.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Bulk Actions */}
        {selected.size > 0 && (
          <Card className="mb-4 border-blue-200 bg-blue-50" data-testid="bulk-actions-bar">
            <CardContent className="p-4">
              <div className="flex flex-wrap items-center gap-3">
                <span className="text-sm font-medium text-blue-700">{selected.size} selected</span>
                <div className="flex items-center gap-2">
                  <Select value={bulkCategory} onValueChange={setBulkCategory}>
                    <SelectTrigger className="w-40 h-9 text-xs" data-testid="bulk-category-select">
                      <SelectValue placeholder="Move to..." />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map(c => (
                        <SelectItem key={c.slug} value={c.slug}>{c.name}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button size="sm" variant="outline" onClick={handleBulkCategory} disabled={!bulkCategory} data-testid="bulk-category-btn">
                    <FolderOpen className="h-3.5 w-3.5 mr-1" /> Move
                  </Button>
                </div>
                <Button size="sm" variant="destructive" onClick={handleBulkDelete} data-testid="bulk-delete-btn">
                  <Trash2 className="h-3.5 w-3.5 mr-1" /> Delete ({selected.size})
                </Button>
                <Button size="sm" variant="ghost" onClick={() => setSelected(new Set())} className="text-slate-500">
                  Clear
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Articles Table */}
        <Card>
          <CardContent className="p-0">
            {/* Header */}
            <div className="flex items-center gap-3 px-6 py-3 bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
              <button onClick={selectAll} className="flex-shrink-0" data-testid="select-all-btn">
                {selected.size === articles.length && articles.length > 0 ? (
                  <CheckSquare className="h-4 w-4 text-blue-600" />
                ) : (
                  <Square className="h-4 w-4" />
                )}
              </button>
              <span className="flex-1">Title</span>
              <span className="w-28 text-center">Category</span>
              <span className="w-20 text-center">Views</span>
              <span className="w-20 text-center">Likes</span>
            </div>
            {loading ? (
              <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : articles.length === 0 ? (
              <div className="text-center py-12 text-slate-500">
                <FileText className="h-12 w-12 mx-auto mb-3 text-slate-300" />
                <p>No articles found</p>
              </div>
            ) : (
              <div className="divide-y divide-slate-100">
                {articles.map((art) => (
                  <div
                    key={art.slug}
                    className={`flex items-center gap-3 px-6 py-3 hover:bg-slate-50 transition-colors ${selected.has(art.slug) ? 'bg-blue-50/50' : ''}`}
                    data-testid={`article-row-${art.slug}`}
                  >
                    <button onClick={() => toggleSelect(art.slug)} className="flex-shrink-0">
                      {selected.has(art.slug) ? (
                        <CheckSquare className="h-4 w-4 text-blue-600" />
                      ) : (
                        <Square className="h-4 w-4 text-slate-400" />
                      )}
                    </button>
                    <div className="flex-1 min-w-0">
                      <Link to={`/snippet/${art.slug}`} className="text-sm font-medium text-slate-900 hover:text-blue-600 truncate block">
                        {art.title}
                      </Link>
                      <p className="text-xs text-slate-400 truncate">{art.description}</p>
                    </div>
                    <div className="w-28 text-center">
                      <Badge variant="outline" className="text-xs capitalize">{getCategoryName(art.category)}</Badge>
                    </div>
                    <div className="w-20 text-center text-sm text-slate-600">{(art.views || 0).toLocaleString()}</div>
                    <div className="w-20 text-center text-sm text-slate-600">{art.likes || 0}</div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Pagination */}
        {pages > 1 && (
          <div className="flex items-center justify-center gap-3 mt-6">
            <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-sm text-slate-600">Page {page} of {pages}</span>
            <Button variant="outline" size="sm" disabled={page >= pages} onClick={() => setPage(p => p + 1)}>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ManageArticles;
