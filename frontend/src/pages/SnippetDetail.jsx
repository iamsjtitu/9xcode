import React, { useState, useEffect, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
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
  Bookmark,
  BookmarkCheck,
  List,
  Clock,
} from 'lucide-react';
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Separator } from '../components/ui/separator';
import { Textarea } from '../components/ui/textarea';
import { Input } from '../components/ui/input';
import CodeBlock from '../components/CodeBlock';
import GoogleAd from '../components/GoogleAd';
import SocialShare from '../components/SocialShare';
import { categories, difficultyLevels, operatingSystems } from '../data/mockData';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const getBookmarks = () => {
  try { return JSON.parse(localStorage.getItem('9xcodes_bookmarks') || '[]'); }
  catch { return []; }
};

const SnippetDetail = ({ adsConfig }) => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [snippet, setSnippet] = useState(null);
  const [liked, setLiked] = useState(false);
  const [comment, setComment] = useState('');
  const [userName, setUserName] = useState('');
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [relatedSnippets, setRelatedSnippets] = useState([]);
  const [bookmarked, setBookmarked] = useState(false);
  const [activeTocStep, setActiveTocStep] = useState(0);

  useEffect(() => {
    fetchSnippet();
    window.scrollTo(0, 0);
  }, [slug]);

  useEffect(() => {
    if (snippet) {
      fetchComments();
      fetchRelated();
      setBookmarked(getBookmarks().some(b => b.slug === snippet.slug));
    }
  }, [snippet]);

  // TOC scroll spy
  useEffect(() => {
    const handleScroll = () => {
      const stepElements = document.querySelectorAll('[data-step-index]');
      let current = 0;
      stepElements.forEach((el, idx) => {
        if (el.getBoundingClientRect().top < 200) current = idx;
      });
      setActiveTocStep(current);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
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

  const fetchRelated = async () => {
    try {
      const response = await axios.get(`${API}/snippets/${slug}/related?limit=4`);
      setRelatedSnippets(response.data);
    } catch (error) {
      console.error('Error fetching related:', error);
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
      toast({ title: 'Error', description: 'Failed to update like', variant: 'destructive' });
    }
  };

  const handleBookmark = () => {
    const bookmarks = getBookmarks();
    const exists = bookmarks.find(b => b.slug === snippet.slug);
    let updated;
    if (exists) {
      updated = bookmarks.filter(b => b.slug !== snippet.slug);
      setBookmarked(false);
      toast({ title: 'Bookmark removed', description: 'Article removed from saved list' });
    } else {
      updated = [...bookmarks, { slug: snippet.slug, title: snippet.title, category: snippet.category, description: snippet.description }];
      setBookmarked(true);
      toast({ title: 'Bookmarked!', description: 'Article saved for later reading' });
    }
    localStorage.setItem('9xcodes_bookmarks', JSON.stringify(updated));
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
        toast({ title: 'Comment posted!', description: 'Your comment has been added successfully' });
      } catch (error) {
        toast({ title: 'Error', description: 'Failed to post comment', variant: 'destructive' });
      }
    } else {
      toast({ title: 'Validation Error', description: 'Please enter your name and comment', variant: 'destructive' });
    }
  };

  const readingTime = useMemo(() => {
    if (!snippet) return 0;
    const totalCode = snippet.steps.reduce((acc, step) => acc + step.code.length + step.description.length + step.title.length, 0);
    return Math.max(1, Math.ceil(totalCode / 800));
  }, [snippet]);

  const scrollToStep = (idx) => {
    const el = document.querySelector(`[data-step-index="${idx}"]`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
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
            <Link to="/"><Button>Back to Home</Button></Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    toast({ title: 'Link copied!', description: 'Share this tutorial with your team' });
  };

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
        <div className="flex gap-8">
          {/* Table of Contents - Desktop Sidebar */}
          {snippet.steps.length > 2 && (
            <aside className="hidden xl:block w-64 flex-shrink-0" data-testid="table-of-contents">
              <div className="sticky top-24 bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                <div className="flex items-center gap-2 mb-4">
                  <List className="h-4 w-4 text-blue-600" />
                  <h3 className="text-sm font-bold text-slate-800">Table of Contents</h3>
                </div>
                <nav className="space-y-1">
                  {snippet.steps.map((step, idx) => (
                    <button
                      key={idx}
                      onClick={() => scrollToStep(idx)}
                      data-testid={`toc-step-${idx}`}
                      className={`w-full text-left px-3 py-2 rounded-lg text-xs transition-all flex items-start gap-2 ${
                        activeTocStep === idx
                          ? 'bg-blue-50 text-blue-700 font-medium'
                          : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      <span className={`flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold mt-0.5 ${
                        activeTocStep === idx ? 'bg-blue-600 text-white' : 'bg-slate-200 text-slate-500'
                      }`}>
                        {idx + 1}
                      </span>
                      <span className="line-clamp-2">{step.title}</span>
                    </button>
                  ))}
                </nav>
              </div>
            </aside>
          )}

          {/* Main Content */}
          <div className="flex-1 max-w-5xl">
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
                <CardTitle className="text-3xl md:text-4xl font-bold text-slate-900" data-testid="snippet-title">
                  {snippet.title}
                </CardTitle>
                <CardDescription className="text-base md:text-lg text-slate-600">
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
                  <div className="flex items-center space-x-2">
                    <Clock className="h-4 w-4" />
                    <span>{readingTime} min read</span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col gap-4 pt-4">
                  <div className="flex flex-wrap gap-3">
                    <Button
                      variant={liked ? 'default' : 'outline'}
                      onClick={handleLike}
                      data-testid="like-btn"
                      className={liked ? 'bg-red-500 hover:bg-red-600 text-white' : ''}
                    >
                      <Heart className={`h-4 w-4 mr-2 ${liked ? 'fill-current' : ''}`} />
                      {liked ? 'Liked' : 'Like'} ({snippet.likes + (liked ? 1 : 0)})
                    </Button>
                    <Button
                      variant="outline"
                      onClick={handleBookmark}
                      data-testid="bookmark-btn"
                      className={bookmarked ? 'border-amber-300 text-amber-600 bg-amber-50' : ''}
                    >
                      {bookmarked ? <BookmarkCheck className="h-4 w-4 mr-2" /> : <Bookmark className="h-4 w-4 mr-2" />}
                      {bookmarked ? 'Saved' : 'Save'}
                    </Button>
                    <Button variant="outline" onClick={handleShare} data-testid="share-btn">
                      <Share2 className="h-4 w-4 mr-2" />
                      Copy Link
                    </Button>
                    <Button variant="outline">
                      <MessageCircle className="h-4 w-4 mr-2" />
                      Comments ({comments.length})
                    </Button>
                  </div>
                  <Separator />
                  <SocialShare title={snippet.title} url={window.location.href} />
                </div>
              </CardHeader>
            </Card>

            {/* Tags - Clickable */}
            <Card className="mb-8 border-slate-200">
              <CardHeader>
                <CardTitle className="text-sm font-semibold text-slate-700">Tags</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {snippet.tags.map((tag, idx) => (
                    <Link
                      key={idx}
                      to={`/?tag=${encodeURIComponent(tag)}`}
                      data-testid={`tag-link-${tag}`}
                      className="text-sm bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg hover:bg-blue-100 hover:text-blue-700 transition-colors cursor-pointer"
                    >
                      #{tag}
                    </Link>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Mobile TOC */}
            {snippet.steps.length > 2 && (
              <Card className="mb-8 border-slate-200 xl:hidden" data-testid="mobile-toc">
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <List className="h-5 w-5 text-blue-600" />
                    <CardTitle className="text-base">Table of Contents</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <nav className="space-y-1">
                    {snippet.steps.map((step, idx) => (
                      <button
                        key={idx}
                        onClick={() => scrollToStep(idx)}
                        className="w-full text-left px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-blue-50 hover:text-blue-700 flex items-center gap-2 transition-colors"
                      >
                        <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold flex-shrink-0">
                          {idx + 1}
                        </span>
                        {step.title}
                      </button>
                    ))}
                  </nav>
                </CardContent>
              </Card>
            )}

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
                  <div key={idx} className="relative" data-step-index={idx}>
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

            {/* Related Articles */}
            {relatedSnippets.length > 0 && (
              <Card className="mb-8 border-slate-200" data-testid="related-articles-section">
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <BookOpen className="h-5 w-5 text-blue-600" />
                    <CardTitle className="text-xl">Related Articles</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {relatedSnippets.map((related) => (
                      <Link
                        key={related.slug}
                        to={`/snippet/${related.slug}`}
                        data-testid={`related-article-${related.slug}`}
                        className="block p-4 rounded-lg border border-slate-200 hover:border-blue-300 hover:shadow-md transition-all group"
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <Badge className="bg-blue-50 text-blue-700 border border-blue-200 text-xs">
                            {getCategoryName(related.category)}
                          </Badge>
                          <Badge
                            style={{
                              backgroundColor: `${getDifficultyColor(related.difficulty)}15`,
                              color: getDifficultyColor(related.difficulty),
                              borderColor: `${getDifficultyColor(related.difficulty)}30`,
                            }}
                            className="border capitalize text-xs"
                          >
                            {related.difficulty}
                          </Badge>
                        </div>
                        <h4 className="font-bold text-slate-900 group-hover:text-blue-600 transition-colors mb-1 line-clamp-2">
                          {related.title}
                        </h4>
                        <p className="text-sm text-slate-500 line-clamp-2">{related.description}</p>
                        <div className="flex items-center gap-3 mt-2 text-xs text-slate-400">
                          <span className="flex items-center gap-1"><Eye className="h-3 w-3" />{related.views.toLocaleString()}</span>
                          <span className="flex items-center gap-1"><Heart className="h-3 w-3" />{related.likes}</span>
                        </div>
                      </Link>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Comments Section */}
            <Card className="border-slate-200">
              <CardHeader>
                <CardTitle className="text-xl">Comments ({comments.length})</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCommentSubmit} className="mb-6 space-y-3">
                  <Input
                    placeholder="Your name"
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    required
                    data-testid="comment-name-input"
                  />
                  <Textarea
                    placeholder="Share your thoughts or ask a question..."
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    rows={3}
                    required
                    data-testid="comment-text-input"
                  />
                  <Button type="submit" disabled={!comment.trim() || !userName.trim()} data-testid="post-comment-btn">
                    Post Comment
                  </Button>
                </form>
                <Separator className="my-6" />
                <div className="space-y-4">
                  {comments.length === 0 ? (
                    <p className="text-center text-slate-500 py-8">No comments yet. Be the first to comment!</p>
                  ) : (
                    comments.map((c) => (
                      <div key={c.id} className="bg-slate-50 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-semibold text-slate-900">{c.user}</span>
                          <span className="text-sm text-slate-500">{new Date(c.createdAt).toLocaleString()}</span>
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
    </div>
  );
};

export default SnippetDetail;
