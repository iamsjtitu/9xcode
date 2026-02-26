import React, { useState, useEffect } from 'react';
import { Save, AlertCircle, CheckCircle2, Settings } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Switch } from '../components/ui/switch';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const GoogleAdsManager = () => {
  const [loading, setLoading] = useState(false);
  const [adsConfig, setAdsConfig] = useState({
    enabled: false,
    headerAdCode: '',
    sidebarAdCode: '',
    betweenSnippetsAdCode: '',
    footerAdCode: '',
  });

  useEffect(() => {
    fetchAdsConfig();
  }, []);

  const fetchAdsConfig = async () => {
    try {
      const response = await axios.get(`${API}/ads/config`);
      setAdsConfig(response.data);
    } catch (error) {
      console.error('Error fetching ads config:', error);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      await axios.post(`${API}/ads/config`, adsConfig);
      toast({
        title: 'Success!',
        description: 'Google Ads configuration has been saved successfully',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to save ads configuration',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 mb-2">
            <Settings className="h-8 w-8 text-blue-600" />
            <h1 className="text-4xl font-bold text-slate-900">Google Ads Manager</h1>
          </div>
          <p className="text-slate-600">
            Configure Google AdSense codes to monetize your website and generate revenue.
          </p>
        </div>

        {/* Enable/Disable Ads */}
        <Card className="mb-6 border-slate-200">
          <CardHeader>
            <CardTitle>Ad Status</CardTitle>
            <CardDescription>Enable or disable all ads across the website</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
              <div>
                <p className="font-semibold text-slate-900">Display Ads</p>
                <p className="text-sm text-slate-600">
                  {adsConfig.enabled ? 'Ads are currently active' : 'Ads are currently disabled'}
                </p>
              </div>
              <Switch
                checked={adsConfig.enabled}
                onCheckedChange={(checked) =>
                  setAdsConfig((prev) => ({ ...prev, enabled: checked }))
                }
              />
            </div>
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card className="mb-6 border-blue-200 bg-blue-50">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-3">
              <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-blue-900">
                <p className="font-semibold mb-1">How to use Google AdSense:</p>
                <ol className="list-decimal list-inside space-y-1 text-blue-800">
                  <li>Sign up for Google AdSense at adsense.google.com</li>
                  <li>Create ad units in your AdSense dashboard</li>
                  <li>Copy the ad code provided by Google</li>
                  <li>Paste the code in the appropriate fields below</li>
                  <li>Enable ads and save the configuration</li>
                </ol>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Ad Placement Cards */}
        <div className="space-y-6">
          {/* Header Ad */}
          <Card className="border-slate-200">
            <CardHeader>
              <CardTitle>Header Ad (Top of Page)</CardTitle>
              <CardDescription>
                Displays at the top of every page. Recommended: 728x90 Leaderboard or Responsive
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Paste your Google AdSense code here..."
                value={adsConfig.headerAdCode || ''}
                onChange={(e) =>
                  setAdsConfig((prev) => ({ ...prev, headerAdCode: e.target.value }))
                }
                rows={6}
                className="font-mono text-sm"
              />
            </CardContent>
          </Card>

          {/* Sidebar Ad */}
          <Card className="border-slate-200">
            <CardHeader>
              <CardTitle>Sidebar Ad</CardTitle>
              <CardDescription>
                Displays in the sidebar on larger screens. Recommended: 300x250 Medium Rectangle or 300x600 Half Page
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Paste your Google AdSense code here..."
                value={adsConfig.sidebarAdCode || ''}
                onChange={(e) =>
                  setAdsConfig((prev) => ({ ...prev, sidebarAdCode: e.target.value }))
                }
                rows={6}
                className="font-mono text-sm"
              />
            </CardContent>
          </Card>

          {/* Between Snippets Ad */}
          <Card className="border-slate-200">
            <CardHeader>
              <CardTitle>Between Snippets Ad</CardTitle>
              <CardDescription>
                Displays between code snippet listings. Recommended: Responsive or 728x90 Leaderboard
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Paste your Google AdSense code here..."
                value={adsConfig.betweenSnippetsAdCode || ''}
                onChange={(e) =>
                  setAdsConfig((prev) => ({ ...prev, betweenSnippetsAdCode: e.target.value }))
                }
                rows={6}
                className="font-mono text-sm"
              />
            </CardContent>
          </Card>

          {/* Footer Ad */}
          <Card className="border-slate-200">
            <CardHeader>
              <CardTitle>Footer Ad (Bottom of Page)</CardTitle>
              <CardDescription>
                Displays at the bottom of every page. Recommended: 728x90 Leaderboard or Responsive
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Paste your Google AdSense code here..."
                value={adsConfig.footerAdCode || ''}
                onChange={(e) =>
                  setAdsConfig((prev) => ({ ...prev, footerAdCode: e.target.value }))
                }
                rows={6}
                className="font-mono text-sm"
              />
            </CardContent>
          </Card>
        </div>

        {/* Success Info */}
        <Card className="mt-6 border-green-200 bg-green-50">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-3">
              <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-green-900">
                <p className="font-semibold mb-1">Best Practices:</p>
                <ul className="list-disc list-inside space-y-1 text-green-800">
                  <li>Don't place too many ads - it can hurt user experience</li>
                  <li>Use responsive ad units for better mobile experience</li>
                  <li>Monitor your AdSense performance regularly</li>
                  <li>Follow Google's AdSense policies to avoid account suspension</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end mt-6">
          <Button
            onClick={handleSave}
            disabled={loading}
            className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-8"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Saving...
              </>
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                Save Configuration
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default GoogleAdsManager;
