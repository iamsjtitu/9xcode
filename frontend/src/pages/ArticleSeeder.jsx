import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Sprout, Play, Eye, Check, AlertCircle, Loader2, ChevronDown } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from '../hooks/use-toast';
import { categories, operatingSystems } from '../data/mockData';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ArticleSeeder = () => {
  const [selectedCat, setSelectedCat] = useState('');
  const [selectedOS, setSelectedOS] = useState('');
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [seedResult, setSeedResult] = useState(null);
  const [history, setHistory] = useState([]);

  const getCategoryName = (slug) => {
    const c = categories.find(cat => cat.slug === slug);
    return c ? c.name : slug;
  };

  const getOSName = (slug) => {
    const o = operatingSystems.find(os => os.slug === slug);
    return o ? o.name : slug;
  };

  const handlePreview = async () => {
    if (!selectedCat) return;
    setLoading(true);
    setPreview(null);
    setSeedResult(null);
    try {
      const body = { category: selectedCat };
      if (selectedOS) body.os = selectedOS;
      const res = await axios.post(`${API}/seeder/preview`, body);
      setPreview(res.data);
    } catch (err) {
      toast({ title: 'Error', description: err.response?.data?.detail || 'Failed to preview', variant: 'destructive' });
    } finally {
      setLoading(false);
    }
  };

  const handleSeed = async () => {
    if (!selectedCat) return;
    setSeeding(true);
    setSeedResult(null);
    try {
      const body = { category: selectedCat };
      if (selectedOS) body.os = selectedOS;
      const res = await axios.post(`${API}/seeder/seed`, body);
      setSeedResult(res.data);
      setHistory(prev => [{
        category: getCategoryName(selectedCat),
        os: selectedOS ? getOSName(selectedOS) : 'Ubuntu',
        added: res.data.added,
        skipped: res.data.skipped,
        time: new Date().toLocaleTimeString(),
      }, ...prev]);
      toast({ title: 'Seeded!', description: res.data.message });
      // Refresh preview
      handlePreview();
    } catch (err) {
      toast({ title: 'Error', description: err.response?.data?.detail || 'Failed to seed', variant: 'destructive' });
    } finally {
      setSeeding(false);
    }
  };

  const handleSeedAll = async () => {
    if (!window.confirm('Seed articles for ALL categories with selected OS? This may add many articles.')) return;
    setSeeding(true);
    setSeedResult(null);
    let totalAdded = 0, totalSkipped = 0;
    const catSlugs = categories.map(c => c.slug);
    for (const cat of catSlugs) {
      try {
        const body = { category: cat };
        if (selectedOS) body.os = selectedOS;
        const res = await axios.post(`${API}/seeder/seed`, body);
        totalAdded += res.data.added;
        totalSkipped += res.data.skipped;
      } catch (err) {
        // Some categories may not have templates, skip
      }
    }
    setSeedResult({ added: totalAdded, skipped: totalSkipped, message: `${totalAdded} articles added, ${totalSkipped} skipped` });
    setHistory(prev => [{
      category: 'All Categories',
      os: selectedOS ? getOSName(selectedOS) : 'Ubuntu',
      added: totalAdded,
      skipped: totalSkipped,
      time: new Date().toLocaleTimeString(),
    }, ...prev]);
    toast({ title: 'Bulk Seed Complete', description: `${totalAdded} new articles added!` });
    setSeeding(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <Link to="/admin" className="text-sm text-blue-600 hover:underline mb-2 inline-block">← Back to Admin</Link>
          <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
            <Sprout className="h-8 w-8 text-green-600" />
            Article Seeder
          </h1>
          <p className="text-slate-500 mt-1">Generate and seed articles by category and operating system</p>
        </div>

        {/* Controls */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-lg">Select Category & OS</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row gap-4 mb-4">
              <div className="flex-1">
                <label className="text-sm font-medium text-slate-600 mb-1 block">Category</label>
                <Select value={selectedCat} onValueChange={(v) => { setSelectedCat(v); setPreview(null); setSeedResult(null); }}>
                  <SelectTrigger data-testid="seeder-category-select">
                    <SelectValue placeholder="Select category..." />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map(c => (
                      <SelectItem key={c.slug} value={c.slug}>{c.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex-1">
                <label className="text-sm font-medium text-slate-600 mb-1 block">Operating System</label>
                <Select value={selectedOS} onValueChange={(v) => { setSelectedOS(v); setPreview(null); setSeedResult(null); }}>
                  <SelectTrigger data-testid="seeder-os-select">
                    <SelectValue placeholder="Ubuntu (default)" />
                  </SelectTrigger>
                  <SelectContent>
                    {operatingSystems.map(os => (
                      <SelectItem key={os.slug} value={os.slug}>{os.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button
                onClick={handlePreview}
                disabled={!selectedCat || loading}
                variant="outline"
                data-testid="preview-btn"
              >
                {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Eye className="h-4 w-4 mr-2" />}
                Preview
              </Button>
              <Button
                onClick={handleSeed}
                disabled={!selectedCat || seeding}
                data-testid="seed-btn"
                className="bg-green-600 hover:bg-green-700"
              >
                {seeding ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Play className="h-4 w-4 mr-2" />}
                Seed Selected
              </Button>
              <Button
                onClick={handleSeedAll}
                disabled={seeding}
                variant="outline"
                data-testid="seed-all-btn"
                className="border-green-300 text-green-700 hover:bg-green-50"
              >
                {seeding ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Sprout className="h-4 w-4 mr-2" />}
                Seed ALL Categories
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Seed Result */}
        {seedResult && (
          <Card className="mb-6 border-green-200 bg-green-50" data-testid="seed-result">
            <CardContent className="p-4 flex items-center gap-3">
              <Check className="h-5 w-5 text-green-600" />
              <span className="text-green-800 font-medium">{seedResult.message}</span>
              {seedResult.total_articles && (
                <Badge variant="outline" className="ml-auto text-green-700 border-green-300">
                  Total: {seedResult.total_articles} articles
                </Badge>
              )}
            </CardContent>
          </Card>
        )}

        {/* Preview */}
        {preview && (
          <Card className="mb-6" data-testid="preview-results">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">Preview: {preview.total} articles ({preview.new} new)</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="divide-y divide-slate-100">
                {preview.articles.map((art, idx) => (
                  <div key={idx} className={`px-6 py-3 flex items-center gap-3 ${art.exists ? 'opacity-50' : ''}`}>
                    <div className="flex-1">
                      <p className="font-medium text-slate-900 text-sm">{art.title}</p>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {art.tags.slice(0, 4).map((t, i) => (
                          <span key={i} className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded">#{t}</span>
                        ))}
                      </div>
                    </div>
                    <Badge variant="outline" className="capitalize text-xs">{art.difficulty}</Badge>
                    {art.exists ? (
                      <Badge className="bg-amber-50 text-amber-600 border border-amber-200 text-xs">Exists</Badge>
                    ) : (
                      <Badge className="bg-green-50 text-green-600 border border-green-200 text-xs">New</Badge>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Seed History */}
        {history.length > 0 && (
          <Card data-testid="seed-history">
            <CardHeader>
              <CardTitle className="text-lg">Seed History (this session)</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="divide-y divide-slate-100">
                {history.map((h, idx) => (
                  <div key={idx} className="px-6 py-3 flex items-center gap-4 text-sm">
                    <span className="text-slate-400 w-16">{h.time}</span>
                    <span className="font-medium text-slate-800">{h.category}</span>
                    <Badge variant="outline" className="text-xs">{h.os}</Badge>
                    <span className="text-green-600 ml-auto">+{h.added} added</span>
                    {h.skipped > 0 && <span className="text-amber-500">{h.skipped} skipped</span>}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ArticleSeeder;
