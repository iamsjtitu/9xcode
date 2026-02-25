import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Eye,
  Heart,
  MessageCircle,
  Share2,
  Calendar,
  User,
  ArrowLeft,
  BookOpen,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Separator } from '../components/ui/separator';
import { Textarea } from '../components/ui/textarea';
import { Input } from '../components/ui/input';
import CodeBlock from '../components/CodeBlock';
import GoogleAd from '../components/GoogleAd';
import { categories, difficultyLevels, operatingSystems } from '../data/mockData';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SnippetDetail = ({ adsConfig }) => {
  const { slug } = useParams();
  const [snippet, setSnippet] = useState(null);
  const [liked, setLiked] = useState(false);
  const [comment, setComment] = useState('');
  const [userName, setUserName] = useState('');
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSnippet();
  }, [slug]);

  useEffect(() => {
    if (snippet) {
      fetchComments();
    }
  }, [snippet]);

  const fetchSnippet = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/snippets/${slug}`);
      setSnippet(response.data);
    } catch (error) {
      console.error('Error fetching snippet:', error);
      setSnippet(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchComments = async () => {
    try {
      const response = await axios.get(`${API}/comments/${snippet.id}`);
      setComments(response.data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  const handleLike = async () => {
    try {
      const response = await axios.post(`${API}/snippets/${slug}/like`);
      setSnippet((prev) => ({ ...prev, likes: response.data.likes }));
      setLiked(!liked);
      toast({
        title: liked ? 'Removed from favorites' : 'Added to favorites',
        description: liked ? 'Snippet removed from your favorites' : 'Snippet saved to your favorites',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update like',
        variant: 'destructive',
      });
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (comment.trim() && userName.trim()) {
      try {
        const response = await axios.post(`${API}/comments`, {
          snippetId: snippet.id,
          user: userName,
          text: comment,
        });
        setComments([response.data, ...comments]);
        setComment('');
        toast({
          title: 'Comment posted!',
          description: 'Your comment has been added successfully',
        });
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to post comment',
          variant: 'destructive',
        });
      }
    } else {
      toast({
        title: 'Validation Error',
        description: 'Please enter your name and comment',
        variant: 'destructive',
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Card className="max-w-md w-full mx-4">
          <CardContent className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-slate-600">Loading tutorial...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!snippet) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Card className="max-w-md w-full mx-4">
          <CardContent className="text-center py-12">
            <AlertCircle className="h-12 w-12 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-600 mb-4">Code snippet not found.</p>
            <Link to="/">
              <Button>Back to Home</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const getCategoryName = (slug) => {
    const category = categories.find((c) => c.slug === slug);
    return category ? category.name : slug;
  };

  const getDifficultyColor = (slug) => {
    const difficulty = difficultyLevels.find((d) => d.slug === slug);
    return difficulty ? difficulty.color : '#6B7280';
  };

  const getOSColor = (slug) => {
    const os = operatingSystems.find((o) => o.slug === slug);
    return os ? os.color : '#6B7280';
  };

  const handleLike = () => {
    setLiked(!liked);
    toast({
      title: liked ? 'Removed from favorites' : 'Added to favorites',
      description: liked ? 'Snippet removed from your favorites' : 'Snippet saved to your favorites',
    });
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    toast({
      title: 'Link copied!',
      description: 'Share this tutorial with your team',
    });
  };

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    if (comment.trim()) {
      setComments([
        { id: comments.length + 1, user: 'You', text: comment, time: 'Just now' },
        ...comments,
      ]);
      setComment('');
      toast({
        title: 'Comment posted!',
        description: 'Your comment has been added successfully',
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      {/* Breadcrumb */}
      <div className="bg-white border-b border-slate-200">
        <div className="container mx-auto px-4 py-4">
          <Link to="/" className="inline-flex items-center text-sm text-slate-600 hover:text-blue-600 transition-colors">
            <ArrowLeft className="h-4 w-4 mr-1" />
            Back to Home
          </Link>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-5xl mx-auto">
          {/* Header Card */}
          <Card className="mb-8 border-slate-200 shadow-lg">
            <CardHeader className="space-y-4">
              {/* Badges */}
              <div className="flex flex-wrap items-center gap-2">
                <Badge className="bg-blue-50 text-blue-700 border border-blue-200">
                  {getCategoryName(snippet.category)}
                </Badge>
                <Badge
                  style={{
                    backgroundColor: `${getDifficultyColor(snippet.difficulty)}15`,
                    color: getDifficultyColor(snippet.difficulty),
                    borderColor: `${getDifficultyColor(snippet.difficulty)}30`,
                  }}
                  className="border capitalize"
                >
                  {snippet.difficulty}
                </Badge>
                {snippet.os.map((os, idx) => (
                  <Badge
                    key={idx}
                    style={{
                      backgroundColor: `${getOSColor(os)}15`,
                      color: getOSColor(os),
                      borderColor: `${getOSColor(os)}30`,
                    }}
                    className="border capitalize"
                  >
                    {os}
                  </Badge>
                ))}
              </div>

              {/* Title */}
              <CardTitle className="text-3xl md:text-4xl font-bold text-slate-900">
                {snippet.title}
              </CardTitle>
              <CardDescription className="text-lg text-slate-600">
                {snippet.description}
              </CardDescription>

              {/* Meta Info */}
              <div className="flex flex-wrap items-center gap-6 text-sm text-slate-500 pt-4 border-t border-slate-200">
                <div className="flex items-center space-x-2">
                  <User className="h-4 w-4" />
                  <span>By {snippet.author}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Calendar className="h-4 w-4" />
                  <span>{new Date(snippet.createdAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Eye className="h-4 w-4" />
                  <span>{snippet.views.toLocaleString()} views</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-3 pt-4">
                <Button
                  variant={liked ? 'default' : 'outline'}
                  onClick={handleLike}
                  className={liked ? 'bg-red-500 hover:bg-red-600 text-white' : ''}
                >
                  <Heart className={`h-4 w-4 mr-2 ${liked ? 'fill-current' : ''}`} />
                  {liked ? 'Liked' : 'Like'} ({snippet.likes + (liked ? 1 : 0)})
                </Button>
                <Button variant="outline" onClick={handleShare}>
                  <Share2 className="h-4 w-4 mr-2" />
                  Share
                </Button>
                <Button variant="outline">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Comments ({comments.length})
                </Button>
              </div>
            </CardHeader>
          </Card>

          {/* Tags */}
          <Card className="mb-8 border-slate-200">
            <CardHeader>
              <CardTitle className="text-sm font-semibold text-slate-700">Tags</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {snippet.tags.map((tag, idx) => (
                  <span
                    key={idx}
                    className="text-sm bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg hover:bg-slate-200 transition-colors cursor-pointer"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Tutorial Steps */}
          <Card className="mb-8 border-slate-200">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <BookOpen className="h-5 w-5 text-blue-600" />
                <CardTitle className="text-2xl">Step-by-Step Tutorial</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-8">
              {snippet.steps.map((step, idx) => (
                <div key={idx} className="relative">
                  {/* Step Number */}
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-full font-bold shadow-md">
                        {idx + 1}
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-slate-900 mb-2">{step.title}</h3>
                      <p className="text-slate-600 mb-4">{step.description}</p>
                      <CodeBlock code={step.code} language={step.language} />
                    </div>
                  </div>
                  {/* Connector Line */}
                  {idx < snippet.steps.length - 1 && (
                    <div className="absolute left-5 top-12 bottom-0 w-0.5 bg-gradient-to-b from-blue-500 to-blue-300 -translate-x-1/2"></div>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Post Installation */}
          {snippet.postInstallation && (
            <Card className="mb-8 border-green-200 bg-green-50">
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                  <CardTitle className="text-xl text-green-900">{snippet.postInstallation.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-green-800">{snippet.postInstallation.content}</p>
              </CardContent>
            </Card>
          )}

          {/* Comments Section */}
          <Card className="border-slate-200">
            <CardHeader>
              <CardTitle className="text-xl">Comments ({comments.length})</CardTitle>
            </CardHeader>
            <CardContent>
              {/* Comment Form */}
              <form onSubmit={handleCommentSubmit} className="mb-6 space-y-3">
                <Input
                  placeholder="Your name"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  required
                />
                <Textarea
                  placeholder="Share your thoughts or ask a question..."
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  rows={3}
                  required
                />
                <Button type="submit" disabled={!comment.trim() || !userName.trim()}>
                  Post Comment
                </Button>
              </form>

              <Separator className="my-6" />

              {/* Comments List */}
              <div className="space-y-4">
                {comments.length === 0 ? (
                  <p className="text-center text-slate-500 py-8">No comments yet. Be the first to comment!</p>
                ) : (
                  comments.map((c) => (
                    <div key={c.id} className="bg-slate-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-slate-900">{c.user}</span>
                        <span className="text-sm text-slate-500">
                          {new Date(c.createdAt).toLocaleString()}
                        </span>
                      </div>
                      <p className="text-slate-700">{c.text}</p>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SnippetDetail;