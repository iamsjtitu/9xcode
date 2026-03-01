import React, { useState, useEffect } from 'react';
import { Users, Download, Trash2, Search, Mail, ChevronLeft, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { toast } from '../hooks/use-toast';
import axios from 'axios';
import { Link } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SubscribersManager = () => {
  const [subscribers, setSubscribers] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchSubscribers(); }, [page, search]);

  const fetchSubscribers = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page, limit: 50 });
      if (search) params.append('search', search);
      const res = await axios.get(`${API}/newsletter/subscribers?${params}`);
      setSubscribers(res.data.subscribers);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (email) => {
    if (!window.confirm(`Remove ${email}?`)) return;
    try {
      await axios.delete(`${API}/newsletter/subscribers/${encodeURIComponent(email)}`);
      toast({ title: 'Removed', description: `${email} unsubscribed` });
      fetchSubscribers();
    } catch (err) {
      toast({ title: 'Error', description: 'Failed to remove', variant: 'destructive' });
    }
  };

  const handleExport = () => {
    window.open(`${API}/newsletter/subscribers/export`, '_blank');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <Link to="/admin" className="text-sm text-blue-600 hover:underline mb-2 inline-block">← Back to Admin</Link>
            <h1 className="text-3xl font-bold text-slate-900">Newsletter Subscribers</h1>
            <p className="text-slate-500 mt-1">{total} total subscribers</p>
          </div>
          <Button onClick={handleExport} variant="outline" data-testid="export-csv-btn">
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
        </div>

        {/* Search */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <Input
                placeholder="Search by email..."
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1); }}
                className="pl-10"
                data-testid="search-subscribers"
              />
            </div>
          </CardContent>
        </Card>

        {/* Subscribers List */}
        <Card>
          <CardContent className="p-0">
            {loading ? (
              <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : subscribers.length === 0 ? (
              <div className="text-center py-12 text-slate-500">
                <Mail className="h-12 w-12 mx-auto mb-3 text-slate-300" />
                <p>No subscribers found</p>
              </div>
            ) : (
              <div className="divide-y divide-slate-100">
                {subscribers.map((sub, idx) => (
                  <div key={idx} className="flex items-center justify-between px-6 py-4 hover:bg-slate-50" data-testid={`subscriber-${sub.email}`}>
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center">
                        <Mail className="h-4 w-4 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium text-slate-900">{sub.email}</p>
                        <p className="text-xs text-slate-400">{new Date(sub.subscribedAt).toLocaleDateString()}</p>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(sub.email)}
                      className="text-red-500 hover:text-red-700 hover:bg-red-50"
                      data-testid={`delete-${sub.email}`}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
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

export default SubscribersManager;
