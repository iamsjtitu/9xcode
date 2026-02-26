import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, Save, BarChart, Globe, Code, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useToast } from '../hooks/use-toast';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const SEOSettings = () => {
  const [settings, setSettings] = useState({
    googleAnalyticsId: '',
    googleTagManagerId: '',
    googleSearchConsoleVerification: '',
    bingVerification: '',
    facebookPixelId: '',
    customHeadCode: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await axios.get(`${API}/ads/config`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.data) {
        setSettings(prev => ({
          ...prev,
          googleAnalyticsId: response.data.googleAnalyticsId || '',
          googleTagManagerId: response.data.googleTagManagerId || '',
          googleSearchConsoleVerification: response.data.googleSearchConsoleVerification || '',
          bingVerification: response.data.bingVerification || '',
          facebookPixelId: response.data.facebookPixelId || '',
          customHeadCode: response.data.customHeadCode || ''
        }));
      }
    } catch (error) {
      console.error('Error fetching settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem('adminToken');
      await axios.post(`${API}/ads/config`, settings, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast({
        title: "Settings Saved",
        description: "SEO & tracking settings have been updated successfully."
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save settings. Please try again.",
        variant: "destructive"
      });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-8" data-testid="seo-settings">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button
            variant="ghost"
            onClick={() => navigate('/admin')}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Admin
          </Button>
          <h1 className="text-2xl font-bold text-slate-800">SEO & Tracking Settings</h1>
        </div>

        <div className="space-y-6">
          {/* Google Analytics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart className="h-5 w-5 text-orange-500" />
                Google Analytics
              </CardTitle>
              <CardDescription>
                Add your Google Analytics tracking ID to monitor website traffic
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="gaId">Google Analytics 4 Measurement ID</Label>
                <Input
                  id="gaId"
                  placeholder="G-XXXXXXXXXX"
                  value={settings.googleAnalyticsId}
                  onChange={(e) => setSettings({ ...settings, googleAnalyticsId: e.target.value })}
                  className="mt-1"
                />
                <p className="text-xs text-slate-500 mt-1">
                  Find this in Google Analytics → Admin → Data Streams → Web
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Google Tag Manager */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="h-5 w-5 text-blue-500" />
                Google Tag Manager
              </CardTitle>
              <CardDescription>
                Manage all your tags in one place with Google Tag Manager
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="gtmId">GTM Container ID</Label>
                <Input
                  id="gtmId"
                  placeholder="GTM-XXXXXXX"
                  value={settings.googleTagManagerId}
                  onChange={(e) => setSettings({ ...settings, googleTagManagerId: e.target.value })}
                  className="mt-1"
                />
              </div>
            </CardContent>
          </Card>

          {/* Search Console Verification */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5 text-green-500" />
                Search Engine Verification
              </CardTitle>
              <CardDescription>
                Verify your site ownership with search engines
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="gscVerify">Google Search Console Verification</Label>
                <Input
                  id="gscVerify"
                  placeholder="google-site-verification=XXXXX"
                  value={settings.googleSearchConsoleVerification}
                  onChange={(e) => setSettings({ ...settings, googleSearchConsoleVerification: e.target.value })}
                  className="mt-1"
                />
              </div>
              <div>
                <Label htmlFor="bingVerify">Bing Webmaster Verification</Label>
                <Input
                  id="bingVerify"
                  placeholder="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                  value={settings.bingVerification}
                  onChange={(e) => setSettings({ ...settings, bingVerification: e.target.value })}
                  className="mt-1"
                />
              </div>
            </CardContent>
          </Card>

          {/* Social Tracking */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart className="h-5 w-5 text-blue-600" />
                Social Media Tracking
              </CardTitle>
              <CardDescription>
                Track conversions from social media
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="fbPixel">Facebook Pixel ID</Label>
                <Input
                  id="fbPixel"
                  placeholder="XXXXXXXXXXXXXXX"
                  value={settings.facebookPixelId}
                  onChange={(e) => setSettings({ ...settings, facebookPixelId: e.target.value })}
                  className="mt-1"
                />
              </div>
            </CardContent>
          </Card>

          {/* Custom Code */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="h-5 w-5 text-purple-500" />
                Custom Head Code
              </CardTitle>
              <CardDescription>
                Add custom scripts to the head section (be careful with this)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <textarea
                className="w-full h-32 p-3 border border-slate-200 rounded-lg font-mono text-sm"
                placeholder="<!-- Custom scripts, meta tags, etc. -->"
                value={settings.customHeadCode}
                onChange={(e) => setSettings({ ...settings, customHeadCode: e.target.value })}
              />
            </CardContent>
          </Card>

          {/* SEO Resources */}
          <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-blue-800">
                <CheckCircle className="h-5 w-5" />
                SEO Features Enabled
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-blue-700">
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Dynamic XML Sitemap: <code className="bg-white px-2 py-0.5 rounded">/api/seo/sitemap.xml</code>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Robots.txt: <code className="bg-white px-2 py-0.5 rounded">/api/seo/robots.txt</code>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Open Graph meta tags for social sharing
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Twitter Card meta tags
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  JSON-LD structured data for rich snippets
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Canonical URLs
                </li>
              </ul>
            </CardContent>
          </Card>

          {/* Save Button */}
          <div className="flex justify-end">
            <Button
              onClick={handleSave}
              disabled={saving}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {saving ? (
                <>Saving...</>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Save Settings
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SEOSettings;
