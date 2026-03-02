import React, { useState } from 'react';
import { Mail, MapPin, Send, MessageSquare } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ContactUs = () => {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await axios.post(`${API}/contact`, form);
      toast({ title: 'Message Sent!', description: 'We will get back to you soon.' });
      setForm({ name: '', email: '', subject: '', message: '' });
    } catch (err) {
      toast({ title: 'Error', description: 'Failed to send message. Please try again.', variant: 'destructive' });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      {/* Hero */}
      <section className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-16">
        <div className="container mx-auto px-4 text-center max-w-3xl">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Contact Us
          </h1>
          <p className="text-base text-slate-300">
            Have a question, suggestion, or just want to say hi? We'd love to hear from you.
          </p>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Contact Info */}
          <div className="space-y-4">
            <Card>
              <CardContent className="p-6 flex items-center gap-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Mail className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-800">Email</p>
                  <p className="text-sm text-slate-500">contact@9xcodes.com</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 flex items-center gap-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <MessageSquare className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-800">Response Time</p>
                  <p className="text-sm text-slate-500">Within 24-48 hours</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 flex items-center gap-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <MapPin className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-800">Location</p>
                  <p className="text-sm text-slate-500">India</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Contact Form */}
          <Card className="md:col-span-2">
            <CardContent className="p-8">
              <h2 className="text-xl font-bold text-slate-900 mb-6">Send us a Message</h2>
              <form onSubmit={handleSubmit} className="space-y-4" data-testid="contact-form">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-slate-600 mb-1 block">Name</label>
                    <Input
                      placeholder="Your name"
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                      required
                      data-testid="contact-name"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-600 mb-1 block">Email</label>
                    <Input
                      type="email"
                      placeholder="your@email.com"
                      value={form.email}
                      onChange={(e) => setForm({ ...form, email: e.target.value })}
                      required
                      data-testid="contact-email"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600 mb-1 block">Subject</label>
                  <Input
                    placeholder="What's this about?"
                    value={form.subject}
                    onChange={(e) => setForm({ ...form, subject: e.target.value })}
                    required
                    data-testid="contact-subject"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600 mb-1 block">Message</label>
                  <Textarea
                    placeholder="Your message..."
                    value={form.message}
                    onChange={(e) => setForm({ ...form, message: e.target.value })}
                    rows={5}
                    required
                    data-testid="contact-message"
                  />
                </div>
                <Button type="submit" disabled={submitting} className="w-full sm:w-auto" data-testid="contact-submit">
                  {submitting ? 'Sending...' : <><Send className="h-4 w-4 mr-2" /> Send Message</>}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ContactUs;
