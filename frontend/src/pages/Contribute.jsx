import React, { useState } from 'react';
import { PenLine, Plus, Trash2, Send, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { categories, operatingSystems, difficultyLevels } from '../data/mockData';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const emptyStep = () => ({ title: '', description: '', code: '', language: 'bash' });

const Contribute = () => {
  const [form, setForm] = useState({
    contributorName: '',
    contributorEmail: '',
    title: '',
    description: '',
    category: '',
    difficulty: 'beginner',
    os: [],
    tags: '',
    steps: [emptyStep()],
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const updateStep = (idx, field, value) => {
    const steps = [...form.steps];
    steps[idx] = { ...steps[idx], [field]: value };
    setForm({ ...form, steps });
  };

  const addStep = () => setForm({ ...form, steps: [...form.steps, emptyStep()] });

  const removeStep = (idx) => {
    if (form.steps.length <= 1) return;
    setForm({ ...form, steps: form.steps.filter((_, i) => i !== idx) });
  };

  const toggleOS = (os) => {
    const current = form.os;
    if (current.includes(os)) {
      setForm({ ...form, os: current.filter(o => o !== os) });
    } else {
      setForm({ ...form, os: [...current, os] });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title || !form.description || !form.category || form.steps.length === 0 || !form.contributorName || !form.contributorEmail) {
      toast({ title: 'Incomplete', description: 'Please fill all required fields.', variant: 'destructive' });
      return;
    }
    if (form.steps.some(s => !s.title || !s.code)) {
      toast({ title: 'Incomplete Steps', description: 'Every step needs a title and code.', variant: 'destructive' });
      return;
    }
    setSubmitting(true);
    try {
      await axios.post(`${API}/contributions/submit`, {
        ...form,
        tags: form.tags.split(',').map(t => t.trim()).filter(Boolean),
      });
      setSubmitted(true);
      toast({ title: 'Submitted!', description: 'Your article has been submitted for review.' });
    } catch (err) {
      toast({ title: 'Error', description: err.response?.data?.detail || 'Submission failed.', variant: 'destructive' });
    } finally {
      setSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full text-center">
          <CardContent className="py-12">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Send className="h-8 w-8 text-green-600" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Article Submitted!</h2>
            <p className="text-slate-500 mb-6">Your contribution is under review. Once approved by admin, it will appear on the website.</p>
            <Button onClick={() => { setSubmitted(false); setForm({ contributorName: '', contributorEmail: '', title: '', description: '', category: '', difficulty: 'beginner', os: [], tags: '', steps: [emptyStep()] }); }}>
              Submit Another
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      {/* Hero */}
      <section className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-12">
        <div className="container mx-auto px-4 text-center max-w-3xl">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Contribute an Article
          </h1>
          <p className="text-base text-slate-300">
            Share your knowledge with the community. Submit a tutorial or code snippet — it will be published after admin review.
          </p>
        </div>
      </section>

      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="flex items-center gap-2 mb-6 bg-amber-50 border border-amber-200 rounded-lg px-4 py-3">
          <AlertCircle className="h-4 w-4 text-amber-600 flex-shrink-0" />
          <p className="text-sm text-amber-700">Submitted articles will be reviewed by admin before appearing on the website.</p>
        </div>

        <form onSubmit={handleSubmit} data-testid="contribute-form">
          {/* Contributor Info */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">Your Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-slate-600 mb-1 block">Name *</label>
                  <Input placeholder="Your name" value={form.contributorName} onChange={(e) => setForm({ ...form, contributorName: e.target.value })} required data-testid="contributor-name" />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600 mb-1 block">Email *</label>
                  <Input type="email" placeholder="your@email.com" value={form.contributorEmail} onChange={(e) => setForm({ ...form, contributorEmail: e.target.value })} required data-testid="contributor-email" />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Article Info */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">Article Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-slate-600 mb-1 block">Title *</label>
                <Input placeholder="e.g., Install Redis on Ubuntu 22.04" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required data-testid="article-title" />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-600 mb-1 block">Description *</label>
                <Textarea placeholder="Brief description of what this tutorial covers..." value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} rows={3} required data-testid="article-description" />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-slate-600 mb-1 block">Category *</label>
                  <Select value={form.category} onValueChange={(v) => setForm({ ...form, category: v })}>
                    <SelectTrigger data-testid="article-category"><SelectValue placeholder="Select..." /></SelectTrigger>
                    <SelectContent>
                      {categories.map(c => <SelectItem key={c.slug} value={c.slug}>{c.name}</SelectItem>)}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600 mb-1 block">Difficulty</label>
                  <Select value={form.difficulty} onValueChange={(v) => setForm({ ...form, difficulty: v })}>
                    <SelectTrigger data-testid="article-difficulty"><SelectValue /></SelectTrigger>
                    <SelectContent>
                      {difficultyLevels.map(d => <SelectItem key={d.slug} value={d.slug}>{d.name}</SelectItem>)}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-600 mb-1 block">Operating Systems</label>
                <div className="flex flex-wrap gap-2">
                  {operatingSystems.map(os => (
                    <button
                      key={os.slug}
                      type="button"
                      onClick={() => toggleOS(os.slug)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                        form.os.includes(os.slug)
                          ? 'bg-blue-50 text-blue-700 border-blue-300'
                          : 'bg-white text-slate-500 border-slate-200 hover:border-blue-200'
                      }`}
                    >
                      {os.name}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-600 mb-1 block">Tags (comma separated)</label>
                <Input placeholder="e.g., redis, cache, nosql" value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} data-testid="article-tags" />
              </div>
            </CardContent>
          </Card>

          {/* Steps */}
          <Card className="mb-6">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">Tutorial Steps</CardTitle>
                <Button type="button" variant="outline" size="sm" onClick={addStep} data-testid="add-step-btn">
                  <Plus className="h-4 w-4 mr-1" /> Add Step
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {form.steps.map((step, idx) => (
                <div key={idx} className="relative border border-slate-200 rounded-lg p-4" data-testid={`step-${idx}`}>
                  <div className="flex items-center justify-between mb-3">
                    <Badge className="bg-blue-50 text-blue-700 border border-blue-200">Step {idx + 1}</Badge>
                    {form.steps.length > 1 && (
                      <button type="button" onClick={() => removeStep(idx)} className="text-red-400 hover:text-red-600">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                  <div className="space-y-3">
                    <Input placeholder="Step title *" value={step.title} onChange={(e) => updateStep(idx, 'title', e.target.value)} required />
                    <Textarea placeholder="Step description" value={step.description} onChange={(e) => updateStep(idx, 'description', e.target.value)} rows={2} />
                    <Textarea placeholder="Code / commands *" value={step.code} onChange={(e) => updateStep(idx, 'code', e.target.value)} rows={4} className="font-mono text-sm" required />
                    <Select value={step.language} onValueChange={(v) => updateStep(idx, 'language', v)}>
                      <SelectTrigger className="w-32"><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="bash">Bash</SelectItem>
                        <SelectItem value="python">Python</SelectItem>
                        <SelectItem value="javascript">JavaScript</SelectItem>
                        <SelectItem value="yaml">YAML</SelectItem>
                        <SelectItem value="sql">SQL</SelectItem>
                        <SelectItem value="powershell">PowerShell</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          <Button type="submit" disabled={submitting} className="w-full" size="lg" data-testid="submit-contribution-btn">
            {submitting ? 'Submitting...' : <><PenLine className="h-4 w-4 mr-2" /> Submit for Review</>}
          </Button>
        </form>
      </div>
    </div>
  );
};

export default Contribute;
