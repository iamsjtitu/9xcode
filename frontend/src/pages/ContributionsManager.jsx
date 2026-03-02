import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Check, X, Eye, ChevronLeft, ChevronRight, Inbox, Clock } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { toast } from '../hooks/use-toast';
import { categories } from '../data/mockData';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ContributionsManager = () => {
  const [contributions, setContributions] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [statusFilter, setStatusFilter] = useState('pending');
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => { fetchContributions(); }, [page, statusFilter]);

  const fetchContributions = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page, limit: 10, status: statusFilter });
      const res = await axios.get(`${API}/contributions?${params}`);
      setContributions(res.data.contributions);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (id, action) => {
    try {
      await axios.post(`${API}/contributions/${id}/${action}`);
      toast({ title: action === 'approve' ? 'Approved!' : 'Rejected', description: action === 'approve' ? 'Article published to website.' : 'Contribution rejected.' });
      fetchContributions();
    } catch (err) {
      toast({ title: 'Error', description: `Failed to ${action}`, variant: 'destructive' });
    }
  };

  const getCategoryName = (slug) => {
    const c = categories.find(cat => cat.slug === slug);
    return c ? c.name : slug;
  };

  const statusColors = { pending: 'bg-amber-50 text-amber-700 border-amber-200', approved: 'bg-green-50 text-green-700 border-green-200', rejected: 'bg-red-50 text-red-700 border-red-200' };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Link to="/admin" className="text-sm text-blue-600 hover:underline mb-2 inline-block">← Back to Admin</Link>
          <h1 className="text-3xl font-bold text-slate-900">Contributions</h1>
          <p className="text-slate-500 mt-1">{total} {statusFilter} contributions</p>
        </div>

        {/* Status Tabs */}
        <div className="flex gap-2 mb-6">
          {['pending', 'approved', 'rejected'].map(s => (
            <button
              key={s}
              onClick={() => { setStatusFilter(s); setPage(1); }}
              data-testid={`tab-${s}`}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all capitalize ${
                statusFilter === s ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200 hover:border-blue-300'
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        {/* Contributions List */}
        {loading ? (
          <Card><CardContent className="py-12 text-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div></CardContent></Card>
        ) : contributions.length === 0 ? (
          <Card><CardContent className="py-12 text-center text-slate-500"><Inbox className="h-12 w-12 mx-auto mb-3 text-slate-300" /><p>No {statusFilter} contributions</p></CardContent></Card>
        ) : (
          <div className="space-y-4">
            {contributions.map((c) => (
              <Card key={c.id} data-testid={`contribution-${c.id}`}>
                <CardContent className="p-5">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge className={`border capitalize text-xs ${statusColors[c.status]}`}>{c.status}</Badge>
                        <Badge variant="outline" className="capitalize text-xs">{getCategoryName(c.category)}</Badge>
                        <Badge variant="outline" className="capitalize text-xs">{c.difficulty}</Badge>
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">{c.title}</h3>
                      <p className="text-sm text-slate-500 mt-1">{c.description}</p>
                      <div className="flex items-center gap-4 mt-2 text-xs text-slate-400">
                        <span>By: {c.contributorName} ({c.contributorEmail})</span>
                        <span className="flex items-center gap-1"><Clock className="h-3 w-3" />{new Date(c.submittedAt).toLocaleDateString()}</span>
                        <span>{c.steps?.length || 0} steps</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <Button variant="outline" size="sm" onClick={() => setExpandedId(expandedId === c.id ? null : c.id)} data-testid={`preview-${c.id}`}>
                        <Eye className="h-4 w-4" />
                      </Button>
                      {c.status === 'pending' && (
                        <>
                          <Button size="sm" className="bg-green-600 hover:bg-green-700" onClick={() => handleAction(c.id, 'approve')} data-testid={`approve-${c.id}`}>
                            <Check className="h-4 w-4" />
                          </Button>
                          <Button size="sm" variant="destructive" onClick={() => handleAction(c.id, 'reject')} data-testid={`reject-${c.id}`}>
                            <X className="h-4 w-4" />
                          </Button>
                        </>
                      )}
                    </div>
                  </div>
                  {/* Expanded Preview */}
                  {expandedId === c.id && c.steps && (
                    <div className="mt-4 pt-4 border-t border-slate-200 space-y-3">
                      {c.steps.map((step, idx) => (
                        <div key={idx} className="bg-slate-50 rounded-lg p-3">
                          <p className="text-sm font-semibold text-slate-800 mb-1">Step {idx + 1}: {step.title}</p>
                          {step.description && <p className="text-xs text-slate-500 mb-2">{step.description}</p>}
                          <pre className="bg-slate-900 text-slate-300 rounded-md p-3 text-xs overflow-x-auto"><code>{step.code}</code></pre>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}

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

export default ContributionsManager;
