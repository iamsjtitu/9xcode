import React, { useState, useEffect } from 'react';
import { PlusCircle, Save, X, AlertCircle, BarChart3, Settings, Globe, DollarSign, Lock, FileText, FolderOpen, Eye, ThumbsUp, Users, Layers, Sprout } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { toast } from '../hooks/use-toast';
import { categories, operatingSystems, difficultyLevels } from '../data/mockData';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminPanel = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [statsLoading, setStatsLoading] = useState(true);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    os: [],
    difficulty: '',
    tags: '',
    steps: [{ title: '', description: '', code: '', language: 'bash' }],
    postInstallation: { title: '', content: '' },
  });

  // Fetch dashboard stats on mount with retry logic
  useEffect(() => {
    const fetchStats = async (retryCount = 0) => {
      const maxRetries = 3;
      try {
        // Use public stats endpoint - no auth required
        const response = await axios.get(`${API}/analytics/stats`, {
          timeout: 10000
        });
        if (response.data) {
          setStats(response.data);
        }
      } catch (error) {
        console.error('Error fetching stats:', error);
        // Retry on failure
        if (retryCount < maxRetries) {
          console.log(`Retrying... (${retryCount + 1}/${maxRetries})`);
          setTimeout(() => fetchStats(retryCount + 1), 1000);
          return;
        }
      } finally {
        setStatsLoading(false);
      }
    };
    
    fetchStats();
  }, []);

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleOSToggle = (osSlug) => {
    setFormData((prev) => ({
      ...prev,
      os: prev.os.includes(osSlug)
        ? prev.os.filter((o) => o !== osSlug)
        : [...prev.os, osSlug],
    }));
  };

  const handleStepChange = (index, field, value) => {
    const newSteps = [...formData.steps];
    newSteps[index][field] = value;
    setFormData((prev) => ({ ...prev, steps: newSteps }));
  };

  const addStep = () => {
    setFormData((prev) => ({
      ...prev,
      steps: [...prev.steps, { title: '', description: '', code: '', language: 'bash' }],
    }));
  };

  const removeStep = (index) => {
    if (formData.steps.length > 1) {
      setFormData((prev) => ({
        ...prev,
        steps: prev.steps.filter((_, i) => i !== index),
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.title || !formData.description || !formData.category || formData.os.length === 0 || !formData.difficulty) {
      toast({
        title: 'Validation Error',
        description: 'Please fill in all required fields',
        variant: 'destructive',
      });
      return;
    }

    setLoading(true);
    try {
      // Convert tags string to array
      const tagsArray = formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag);
      
      const payload = {
        ...formData,
        tags: tagsArray,
      };

      await axios.post(`${API}/snippets`, payload);
      
      toast({
        title: 'Success!',
        description: 'Code snippet has been published successfully',
      });

      // Reset form
      setFormData({
        title: '',
        description: '',
        category: '',
        os: [],
        difficulty: '',
        tags: '',
        steps: [{ title: '', description: '', code: '', language: 'bash' }],
        postInstallation: { title: '', content: '' },
      });

      // Redirect to home after a short delay
      setTimeout(() => {
        navigate('/');
      }, 1500);
    } catch (error) {
      console.error('Error creating snippet:', error);
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to create snippet',
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
          <h1 className="text-4xl font-bold text-slate-900 mb-2">Admin Panel</h1>
          <p className="text-slate-600">Create and publish new code snippets and tutorials</p>
        </div>

        {/* Quick Access Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-8">

        {/* Stats Overview Section */}
        {statsLoading ? (
          <Card className="col-span-full mb-0">
            <CardContent className="p-6 flex items-center justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-slate-600">Loading statistics...</span>
            </CardContent>
          </Card>
        ) : !stats ? (
          <Card className="col-span-full mb-0 border-orange-200 bg-orange-50">
            <CardContent className="p-6 flex items-center justify-between">
              <span className="text-orange-700">Stats could not be loaded.</span>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => window.location.reload()}
                className="border-orange-300 text-orange-700 hover:bg-orange-100"
              >
                Retry
              </Button>
            </CardContent>
          </Card>
        ) : stats && (
          <>
            {/* Overview Stats */}
            <Card className="col-span-full mb-0 border-slate-200 bg-gradient-to-r from-blue-50 to-indigo-50">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  Website Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div className="bg-white rounded-lg p-4 shadow-sm border">
                    <div className="flex items-center gap-2 mb-1">
                      <FileText className="h-4 w-4 text-blue-600" />
                      <span className="text-xs text-slate-500 uppercase">Total Articles</span>
                    </div>
                    <p className="text-2xl font-bold text-slate-900">{stats.overview.total_articles}</p>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm border">
                    <div className="flex items-center gap-2 mb-1">
                      <Eye className="h-4 w-4 text-green-600" />
                      <span className="text-xs text-slate-500 uppercase">Total Views</span>
                    </div>
                    <p className="text-2xl font-bold text-slate-900">{stats.overview.total_views.toLocaleString()}</p>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm border">
                    <div className="flex items-center gap-2 mb-1">
                      <ThumbsUp className="h-4 w-4 text-red-600" />
                      <span className="text-xs text-slate-500 uppercase">Total Likes</span>
                    </div>
                    <p className="text-2xl font-bold text-slate-900">{stats.overview.total_likes.toLocaleString()}</p>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm border">
                    <div className="flex items-center gap-2 mb-1">
                      <FolderOpen className="h-4 w-4 text-purple-600" />
                      <span className="text-xs text-slate-500 uppercase">Categories</span>
                    </div>
                    <p className="text-2xl font-bold text-slate-900">{stats.categories.length}</p>
                  </div>
                  <div className="bg-white rounded-lg p-4 shadow-sm border">
                    <div className="flex items-center gap-2 mb-1">
                      <FileText className="h-4 w-4 text-orange-600" />
                      <span className="text-xs text-slate-500 uppercase">This Week</span>
                    </div>
                    <p className="text-2xl font-bold text-slate-900">{stats.overview.articles_this_week}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Category-wise Stats */}
            <Card className="col-span-full mb-0 border-slate-200">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center gap-2">
                  <FolderOpen className="h-5 w-5 text-purple-600" />
                  Articles by Category
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
                  {stats.categories.map((cat, index) => (
                    <div key={index} className="bg-slate-50 rounded-lg p-3 border hover:shadow-md transition-shadow">
                      <p className="text-xs text-slate-500 truncate capitalize">{cat.name?.replace(/-/g, ' ') || 'Unknown'}</p>
                      <p className="text-xl font-bold text-slate-900">{cat.count}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        )}
          <Link to="/admin/analytics">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-blue-200 hover:border-blue-400">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <BarChart3 className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800">Analytics</p>
                  <p className="text-xs text-slate-500">View site statistics</p>
                </div>
              </CardContent>
            </Card>
          </Link>
          
          <Link to="/admin/seo">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-green-200 hover:border-green-400">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Globe className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800">SEO & Tracking</p>
                  <p className="text-xs text-slate-500">Google Analytics, SEO</p>
                </div>
              </CardContent>
            </Card>
          </Link>
          
          <Link to="/admin/ads">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-orange-200 hover:border-orange-400">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <DollarSign className="h-6 w-6 text-orange-600" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800">Google Ads</p>
                  <p className="text-xs text-slate-500">Manage AdSense</p>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/admin/change-password">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-red-200 hover:border-red-400">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="p-2 bg-red-100 rounded-lg">
                  <Lock className="h-6 w-6 text-red-600" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800">Password</p>
                  <p className="text-xs text-slate-500">Change password</p>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/admin/subscribers">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-teal-200 hover:border-teal-400" data-testid="admin-subscribers-link">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="p-2 bg-teal-100 rounded-lg">
                  <Users className="h-6 w-6 text-teal-600" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800">Subscribers</p>
                  <p className="text-xs text-slate-500">Newsletter list</p>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/admin/articles">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-indigo-200 hover:border-indigo-400" data-testid="admin-articles-link">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="p-2 bg-indigo-100 rounded-lg">
                  <Layers className="h-6 w-6 text-indigo-600" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800">Articles</p>
                  <p className="text-xs text-slate-500">Bulk manage</p>
                </div>
              </CardContent>
            </Card>
          </Link>
          
          <Card className="border-purple-200 bg-purple-50">
            <CardContent className="p-4 flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Settings className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="font-semibold text-slate-800">Create Article</p>
                <p className="text-xs text-slate-500">You are here</p>
              </div>
            </CardContent>
          </Card>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Basic Information */}
          <Card className="mb-6 border-slate-200">
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>Enter the basic details of your code snippet</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="title">Title *</Label>
                <Input
                  id="title"
                  placeholder="e.g., Install cPanel on Ubuntu Server"
                  value={formData.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="description">Description *</Label>
                <Textarea
                  id="description"
                  placeholder="Brief description of what this tutorial covers..."
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  rows={3}
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="category">Category *</Label>
                  <Select value={formData.category} onValueChange={(value) => handleInputChange('category', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((cat) => (
                        <SelectItem key={cat.id} value={cat.slug}>
                          {cat.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="difficulty">Difficulty Level *</Label>
                  <Select value={formData.difficulty} onValueChange={(value) => handleInputChange('difficulty', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select difficulty" />
                    </SelectTrigger>
                    <SelectContent>
                      {difficultyLevels.map((level) => (
                        <SelectItem key={level.id} value={level.slug}>
                          {level.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label>Operating Systems *</Label>
                <div className="flex flex-wrap gap-2 mt-2">
                  {operatingSystems.map((os) => (
                    <Badge
                      key={os.id}
                      onClick={() => handleOSToggle(os.slug)}
                      style={{
                        backgroundColor: formData.os.includes(os.slug) ? os.color : '#f1f5f9',
                        color: formData.os.includes(os.slug) ? 'white' : '#64748b',
                        cursor: 'pointer',
                      }}
                      className="border hover:opacity-80 transition-opacity"
                    >
                      {os.name}
                    </Badge>
                  ))}
                </div>
              </div>

              <div>
                <Label htmlFor="tags">Tags (comma-separated)</Label>
                <Input
                  id="tags"
                  placeholder="e.g., cpanel, whm, hosting, installation"
                  value={formData.tags}
                  onChange={(e) => handleInputChange('tags', e.target.value)}
                />
              </div>
            </CardContent>
          </Card>

          {/* Tutorial Steps */}
          <Card className="mb-6 border-slate-200">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Tutorial Steps</CardTitle>
                  <CardDescription>Add step-by-step instructions with code</CardDescription>
                </div>
                <Button type="button" onClick={addStep} variant="outline" size="sm">
                  <PlusCircle className="h-4 w-4 mr-2" />
                  Add Step
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {formData.steps.map((step, index) => (
                <div key={index} className="bg-slate-50 rounded-lg p-4 space-y-4 relative">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-slate-900">Step {index + 1}</span>
                    {formData.steps.length > 1 && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeStep(index)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>

                  <div>
                    <Label>Step Title</Label>
                    <Input
                      placeholder="e.g., Update System Packages"
                      value={step.title}
                      onChange={(e) => handleStepChange(index, 'title', e.target.value)}
                    />
                  </div>

                  <div>
                    <Label>Step Description</Label>
                    <Textarea
                      placeholder="Explain what this step does..."
                      value={step.description}
                      onChange={(e) => handleStepChange(index, 'description', e.target.value)}
                      rows={2}
                    />
                  </div>

                  <div>
                    <Label>Code/Command</Label>
                    <Textarea
                      placeholder="apt update && apt upgrade -y"
                      value={step.code}
                      onChange={(e) => handleStepChange(index, 'code', e.target.value)}
                      rows={4}
                      className="font-mono text-sm"
                    />
                  </div>

                  <div>
                    <Label>Language</Label>
                    <Select
                      value={step.language}
                      onValueChange={(value) => handleStepChange(index, 'language', value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="bash">Bash/Shell</SelectItem>
                        <SelectItem value="python">Python</SelectItem>
                        <SelectItem value="javascript">JavaScript</SelectItem>
                        <SelectItem value="sql">SQL</SelectItem>
                        <SelectItem value="yaml">YAML</SelectItem>
                        <SelectItem value="json">JSON</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Post Installation */}
          <Card className="mb-6 border-slate-200">
            <CardHeader>
              <CardTitle>Post-Installation Notes (Optional)</CardTitle>
              <CardDescription>Add any important notes or next steps</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="postTitle">Title</Label>
                <Input
                  id="postTitle"
                  placeholder="e.g., Post-Installation Steps"
                  value={formData.postInstallation.title}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      postInstallation: { ...prev.postInstallation, title: e.target.value },
                    }))
                  }
                />
              </div>
              <div>
                <Label htmlFor="postContent">Content</Label>
                <Textarea
                  id="postContent"
                  placeholder="What should users do after completing the installation?"
                  value={formData.postInstallation.content}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      postInstallation: { ...prev.postInstallation, content: e.target.value },
                    }))
                  }
                  rows={3}
                />
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4">
            <Button type="button" variant="outline" onClick={() => navigate('/')}>
              Cancel
            </Button>
            <Button 
              type="submit" 
              disabled={loading}
              className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Publishing...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Publish Snippet
                </>
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminPanel;