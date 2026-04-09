import React, { useState } from 'react';
import { Globe, Search, Download, Save, ExternalLink, ArrowLeft, ChevronDown, ChevronUp, AlertTriangle, CheckCircle2, Loader2, Copy, Trash2, Edit3, Sparkles } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from '../hooks/use-toast';
import axios from 'axios';
import { Link } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SOURCES = [
  { id: 'tecmint', name: 'TecMint', desc: 'Linux articles' },
  { id: 'phoenixnap', name: 'PhoenixNAP', desc: 'Server tutorials' },
  { id: 'digitalocean', name: 'DigitalOcean', desc: 'Community tutorials' },
];

const ArticleScraper = () => {
  const [url, setUrl] = useState('');
  const [scraping, setScraping] = useState(false);
  const [saving, setSaving] = useState(false);
  const [preview, setPreview] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [editData, setEditData] = useState(null);
  const [discoverUrls, setDiscoverUrls] = useState([]);
  const [discoverSource, setDiscoverSource] = useState('tecmint');
  const [discovering, setDiscovering] = useState(false);
  const [expandedStep, setExpandedStep] = useState(null);
  const [scrapeHistory, setScrapeHistory] = useState([]);
  const [rewriting, setRewriting] = useState(false);

  const handleScrape = async () => {
    if (!url.trim()) {
      toast({ title: 'URL Required', description: 'Please enter a URL to scrape', variant: 'destructive' });
      return;
    }
    setScraping(true);
    setPreview(null);
    setEditMode(false);
    try {
      const resp = await axios.post(`${API}/scraper/from-url`, { url: url.trim() });
      setPreview(resp.data);
      setEditData(resp.data.full_article);
      setScrapeHistory(prev => [{ url: url.trim(), title: resp.data.article.title, time: new Date().toLocaleTimeString() }, ...prev.slice(0, 9)]);
      toast({ title: 'Scraped!', description: `Found "${resp.data.article.title}" with ${resp.data.article.steps_count} steps` });
    } catch (err) {
      toast({ title: 'Scrape Failed', description: err.response?.data?.detail || 'Could not scrape the URL', variant: 'destructive' });
    } finally {
      setScraping(false);
    }
  };

  const handleSave = async () => {
    const articleToSave = editData || preview?.full_article;
    if (!articleToSave) return;
    setSaving(true);
    try {
      const resp = await axios.post(`${API}/scraper/save`, articleToSave);
      toast({ title: 'Saved!', description: `Article saved as "${resp.data.slug}"` });
      setPreview(null);
      setEditData(null);
      setEditMode(false);
      setUrl('');
    } catch (err) {
      toast({ title: 'Save Failed', description: err.response?.data?.detail || 'Could not save article', variant: 'destructive' });
    } finally {
      setSaving(false);
    }
  };

  const handleDiscover = async () => {
    setDiscovering(true);
    try {
      const resp = await axios.post(`${API}/scraper/discover?source=${discoverSource}`);
      setDiscoverUrls(resp.data.urls || []);
      toast({ title: 'Discovered!', description: `Found ${resp.data.count} URLs from ${resp.data.source}` });
    } catch (err) {
      toast({ title: 'Discover Failed', description: 'Could not discover URLs', variant: 'destructive' });
    } finally {
      setDiscovering(false);
    }
  };

  const handleEditStep = (index, field, value) => {
    setEditData(prev => {
      const newSteps = [...prev.steps];
      newSteps[index] = { ...newSteps[index], [field]: value };
      return { ...prev, steps: newSteps };
    });
  };

  const handleRemoveStep = (index) => {
    setEditData(prev => ({
      ...prev,
      steps: prev.steps.filter((_, i) => i !== index),
    }));
  };

  const handleEditField = (field, value) => {
    setEditData(prev => ({ ...prev, [field]: value }));
  };

  const handleAIRewrite = async () => {
    const source = editData || preview?.full_article;
    if (!source) return;
    setRewriting(true);
    try {
      const resp = await axios.post(`${API}/ai-rewrite/rewrite`, {
        title: source.title,
        description: source.description,
        steps: source.steps,
      });
      const rewritten = resp.data.rewritten;
      setEditData(prev => ({
        ...prev,
        title: rewritten.title || prev.title,
        description: rewritten.description || prev.description,
        steps: rewritten.steps || prev.steps,
      }));
      setEditMode(true);
      toast({ title: 'AI Rewrite Done!', description: 'Content has been rewritten in 9xCodes style. Review and save.' });
    } catch (err) {
      const detail = err.response?.data?.detail || 'AI rewrite failed';
      toast({ title: 'Rewrite Failed', description: detail, variant: 'destructive' });
    } finally {
      setRewriting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50" data-testid="scraper-page">
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link to="/admin">
            <Button variant="outline" size="sm" data-testid="back-to-admin-btn">
              <ArrowLeft className="h-4 w-4 mr-1" /> Admin
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-2">
              <Globe className="h-8 w-8 text-cyan-600" />
              Article Scraper
            </h1>
            <p className="text-slate-600 text-sm mt-1">Scrape articles from external websites and save them in 9xCodes format</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Scrape Input & Discover */}
          <div className="space-y-6">
            {/* Scrape by URL */}
            <Card className="border-cyan-200" data-testid="scrape-url-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Search className="h-5 w-5 text-cyan-600" />
                  Scrape URL
                </CardTitle>
                <CardDescription>Paste any article URL to convert it</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Input
                  data-testid="scrape-url-input"
                  placeholder="https://example.com/tutorial..."
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleScrape()}
                />
                <Button
                  data-testid="scrape-btn"
                  onClick={handleScrape}
                  disabled={scraping || !url.trim()}
                  className="w-full bg-cyan-600 hover:bg-cyan-700"
                >
                  {scraping ? (
                    <><Loader2 className="h-4 w-4 mr-2 animate-spin" /> Scraping...</>
                  ) : (
                    <><Download className="h-4 w-4 mr-2" /> Scrape Article</>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Discover URLs */}
            <Card className="border-slate-200" data-testid="discover-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Globe className="h-5 w-5 text-indigo-600" />
                  Discover Articles
                </CardTitle>
                <CardDescription>Browse popular open-source tutorial sites</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex gap-2">
                  <Select value={discoverSource} onValueChange={setDiscoverSource}>
                    <SelectTrigger data-testid="discover-source-select">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {SOURCES.map(s => (
                        <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button
                    data-testid="discover-btn"
                    onClick={handleDiscover}
                    disabled={discovering}
                    variant="outline"
                  >
                    {discovering ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Browse'}
                  </Button>
                </div>

                {discoverUrls.length > 0 && (
                  <div className="space-y-2 max-h-60 overflow-y-auto" data-testid="discover-urls-list">
                    {discoverUrls.map((dUrl, i) => (
                      <div key={i} className="flex items-center gap-2 p-2 bg-slate-50 rounded-md text-xs group hover:bg-slate-100">
                        <button
                          className="flex-1 text-left text-blue-600 hover:underline truncate"
                          onClick={() => { setUrl(dUrl); }}
                          data-testid={`discover-url-${i}`}
                        >
                          {dUrl.replace(/https?:\/\/(www\.)?/, '').slice(0, 60)}...
                        </button>
                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-6 w-6 p-0 opacity-0 group-hover:opacity-100"
                          onClick={() => { setUrl(dUrl); handleScrape(); }}
                        >
                          <Download className="h-3 w-3" />
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Recent Scrapes */}
            {scrapeHistory.length > 0 && (
              <Card className="border-slate-200">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm text-slate-600">Recent Scrapes</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-1">
                    {scrapeHistory.map((h, i) => (
                      <div key={i} className="text-xs p-2 bg-slate-50 rounded flex justify-between items-center">
                        <span className="truncate flex-1 text-slate-700">{h.title}</span>
                        <span className="text-slate-400 ml-2">{h.time}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Preview & Edit */}
          <div className="lg:col-span-2 space-y-6">
            {!preview && !scraping && (
              <Card className="border-dashed border-2 border-slate-300">
                <CardContent className="p-12 text-center">
                  <Globe className="h-16 w-16 mx-auto text-slate-300 mb-4" />
                  <p className="text-slate-500 text-lg">Paste a URL and click "Scrape Article"</p>
                  <p className="text-slate-400 text-sm mt-2">The scraper will extract title, code blocks, and convert to 9xCodes format</p>
                </CardContent>
              </Card>
            )}

            {scraping && (
              <Card>
                <CardContent className="p-12 text-center">
                  <Loader2 className="h-12 w-12 mx-auto text-cyan-600 mb-4 animate-spin" />
                  <p className="text-slate-600">Fetching and parsing article...</p>
                  <p className="text-slate-400 text-sm mt-1">This may take a few seconds</p>
                </CardContent>
              </Card>
            )}

            {preview && (
              <>
                {/* Article Meta */}
                <Card className="border-green-200" data-testid="preview-card">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="h-5 w-5 text-green-600" />
                        <CardTitle className="text-lg">Scraped Article Preview</CardTitle>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          data-testid="ai-rewrite-btn"
                          size="sm"
                          variant="outline"
                          disabled={rewriting}
                          onClick={handleAIRewrite}
                          className="border-purple-300 text-purple-700 hover:bg-purple-50"
                        >
                          {rewriting ? (
                            <><Loader2 className="h-3 w-3 mr-1 animate-spin" /> Rewriting...</>
                          ) : (
                            <><Sparkles className="h-3 w-3 mr-1" /> AI Rewrite</>
                          )}
                        </Button>
                        <Button
                          data-testid="toggle-edit-btn"
                          size="sm"
                          variant={editMode ? 'default' : 'outline'}
                          onClick={() => setEditMode(!editMode)}
                        >
                          <Edit3 className="h-3 w-3 mr-1" />
                          {editMode ? 'Preview' : 'Edit'}
                        </Button>
                        <Button
                          data-testid="save-article-btn"
                          size="sm"
                          disabled={saving || preview.is_duplicate}
                          onClick={handleSave}
                          className="bg-green-600 hover:bg-green-700"
                        >
                          {saving ? (
                            <><Loader2 className="h-3 w-3 mr-1 animate-spin" /> Saving...</>
                          ) : (
                            <><Save className="h-3 w-3 mr-1" /> Save to DB</>
                          )}
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    {preview.is_duplicate && (
                      <div className="flex items-center gap-2 p-3 bg-amber-50 border border-amber-200 rounded-lg mb-4" data-testid="duplicate-warning">
                        <AlertTriangle className="h-4 w-4 text-amber-600" />
                        <span className="text-sm text-amber-700">An article with this title already exists. Change the title to save.</span>
                      </div>
                    )}

                    {editMode ? (
                      <div className="space-y-4" data-testid="edit-form">
                        <div>
                          <Label>Title</Label>
                          <Input
                            data-testid="edit-title"
                            value={editData?.title || ''}
                            onChange={(e) => handleEditField('title', e.target.value)}
                          />
                        </div>
                        <div>
                          <Label>Description</Label>
                          <Textarea
                            data-testid="edit-description"
                            value={editData?.description || ''}
                            onChange={(e) => handleEditField('description', e.target.value)}
                            rows={2}
                          />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <Label>Category</Label>
                            <Input
                              data-testid="edit-category"
                              value={editData?.category || ''}
                              onChange={(e) => handleEditField('category', e.target.value)}
                            />
                          </div>
                          <div>
                            <Label>Difficulty</Label>
                            <Select value={editData?.difficulty || 'intermediate'} onValueChange={(v) => handleEditField('difficulty', v)}>
                              <SelectTrigger data-testid="edit-difficulty">
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="beginner">Beginner</SelectItem>
                                <SelectItem value="intermediate">Intermediate</SelectItem>
                                <SelectItem value="advanced">Advanced</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                        </div>
                        <div>
                          <Label>Tags (comma-separated)</Label>
                          <Input
                            data-testid="edit-tags"
                            value={(editData?.tags || []).join(', ')}
                            onChange={(e) => handleEditField('tags', e.target.value.split(',').map(t => t.trim()).filter(Boolean))}
                          />
                        </div>
                      </div>
                    ) : (
                      <div className="space-y-3" data-testid="preview-meta">
                        <h2 className="text-xl font-bold text-slate-900" data-testid="preview-title">{preview.article.title}</h2>
                        <p className="text-sm text-slate-600">{preview.article.description}</p>
                        <div className="flex flex-wrap gap-2">
                          <Badge className="bg-cyan-100 text-cyan-800">{preview.article.category}</Badge>
                          <Badge variant="outline">{preview.article.difficulty}</Badge>
                          {preview.article.os?.map((o, i) => (
                            <Badge key={i} variant="secondary">{o}</Badge>
                          ))}
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {preview.article.tags?.map((t, i) => (
                            <Badge key={i} variant="outline" className="text-xs">{t}</Badge>
                          ))}
                        </div>
                        <div className="text-xs text-slate-400 flex items-center gap-1">
                          <ExternalLink className="h-3 w-3" />
                          <a href={preview.article.source_url} target="_blank" rel="noopener noreferrer" className="hover:underline truncate">
                            {preview.article.source_url}
                          </a>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Steps */}
                <Card className="border-slate-200" data-testid="steps-card">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg">
                      Steps ({editMode ? editData?.steps?.length : preview.article.steps_count})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {(editMode ? editData?.steps : preview.article.steps)?.map((step, i) => (
                      <div key={i} className="border rounded-lg overflow-hidden" data-testid={`step-${i}`}>
                        <div
                          className="flex items-center justify-between p-3 bg-slate-50 cursor-pointer hover:bg-slate-100"
                          onClick={() => setExpandedStep(expandedStep === i ? null : i)}
                        >
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold bg-cyan-600 text-white rounded-full w-6 h-6 flex items-center justify-center">{i + 1}</span>
                            {editMode ? (
                              <Input
                                className="h-8 text-sm"
                                value={step.title}
                                onChange={(e) => handleEditStep(i, 'title', e.target.value)}
                                onClick={(e) => e.stopPropagation()}
                                data-testid={`edit-step-title-${i}`}
                              />
                            ) : (
                              <span className="font-medium text-slate-800 text-sm">{step.title}</span>
                            )}
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className="text-xs">{step.language}</Badge>
                            {editMode && (
                              <Button size="sm" variant="ghost" className="h-6 w-6 p-0 text-red-500" onClick={(e) => { e.stopPropagation(); handleRemoveStep(i); }}>
                                <Trash2 className="h-3 w-3" />
                              </Button>
                            )}
                            {expandedStep === i ? <ChevronUp className="h-4 w-4 text-slate-400" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
                          </div>
                        </div>
                        {expandedStep === i && (
                          <div className="p-3 border-t space-y-2">
                            {step.description && (
                              editMode ? (
                                <Textarea
                                  className="text-sm"
                                  rows={2}
                                  value={step.description}
                                  onChange={(e) => handleEditStep(i, 'description', e.target.value)}
                                  data-testid={`edit-step-desc-${i}`}
                                />
                              ) : (
                                <p className="text-sm text-slate-600">{step.description}</p>
                              )
                            )}
                            {editMode ? (
                              <Textarea
                                className="font-mono text-xs bg-slate-900 text-green-400 p-3 rounded"
                                rows={6}
                                value={step.code}
                                onChange={(e) => handleEditStep(i, 'code', e.target.value)}
                                data-testid={`edit-step-code-${i}`}
                              />
                            ) : (
                              <div className="relative group">
                                <pre className="bg-slate-900 text-green-400 p-3 rounded text-xs overflow-x-auto max-h-48">
                                  <code>{step.code}</code>
                                </pre>
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  className="absolute top-2 right-2 h-7 w-7 p-0 bg-slate-700 text-slate-300 opacity-0 group-hover:opacity-100"
                                  onClick={() => { navigator.clipboard.writeText(step.code); toast({ title: 'Copied!' }); }}
                                >
                                  <Copy className="h-3 w-3" />
                                </Button>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleScraper;
