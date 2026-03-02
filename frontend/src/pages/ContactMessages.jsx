import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Trash2, Search, ChevronLeft, ChevronRight, Inbox, Clock } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ContactMessages = () => {
  const [messages, setMessages] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => { fetchMessages(); }, [page, search]);

  const fetchMessages = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page, limit: 20 });
      if (search) params.append('search', search);
      const res = await axios.get(`${API}/contact/messages?${params}`);
      setMessages(res.data.messages);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this message?')) return;
    try {
      await axios.delete(`${API}/contact/messages/${id}`);
      toast({ title: 'Deleted', description: 'Message removed' });
      fetchMessages();
    } catch (err) {
      toast({ title: 'Error', description: 'Failed to delete', variant: 'destructive' });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Link to="/admin" className="text-sm text-blue-600 hover:underline mb-2 inline-block">← Back to Admin</Link>
          <h1 className="text-3xl font-bold text-slate-900">Contact Messages</h1>
          <p className="text-slate-500 mt-1">{total} messages</p>
        </div>

        {/* Search */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <Input
                placeholder="Search by name, email, subject..."
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1); }}
                className="pl-10"
                data-testid="search-messages"
              />
            </div>
          </CardContent>
        </Card>

        {/* Messages */}
        {loading ? (
          <Card><CardContent className="py-12 text-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div></CardContent></Card>
        ) : messages.length === 0 ? (
          <Card><CardContent className="py-12 text-center text-slate-500"><Inbox className="h-12 w-12 mx-auto mb-3 text-slate-300" /><p>No messages found</p></CardContent></Card>
        ) : (
          <div className="space-y-3">
            {messages.map((msg) => (
              <Card key={msg.id} data-testid={`message-${msg.id}`}>
                <CardContent className="p-5">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0 cursor-pointer" onClick={() => setExpandedId(expandedId === msg.id ? null : msg.id)}>
                      <div className="flex items-center gap-3 mb-1">
                        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                          <Mail className="h-4 w-4 text-blue-600" />
                        </div>
                        <div className="min-w-0">
                          <p className="font-semibold text-slate-900 text-sm">{msg.name}</p>
                          <p className="text-xs text-slate-400">{msg.email}</p>
                        </div>
                        <div className="flex items-center gap-1 ml-auto text-xs text-slate-400">
                          <Clock className="h-3 w-3" />
                          {new Date(msg.createdAt).toLocaleDateString()}
                        </div>
                      </div>
                      <p className="font-medium text-slate-800 text-sm mt-2">{msg.subject}</p>
                      {expandedId !== msg.id && (
                        <p className="text-sm text-slate-500 mt-1 truncate">{msg.message}</p>
                      )}
                    </div>
                    <Button variant="ghost" size="sm" onClick={() => handleDelete(msg.id)} className="text-red-400 hover:text-red-600 hover:bg-red-50 flex-shrink-0">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                  {expandedId === msg.id && (
                    <div className="mt-3 pt-3 border-t border-slate-100">
                      <p className="text-sm text-slate-700 whitespace-pre-wrap">{msg.message}</p>
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

export default ContactMessages;
