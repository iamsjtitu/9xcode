import { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Helmet } from "react-helmet";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import SnippetDetail from "./pages/SnippetDetail";
import AdminPanel from "./pages/AdminPanel";
import GoogleAdsManager from "./pages/GoogleAdsManager";
import AnalyticsDashboard from "./pages/AnalyticsDashboard";
import SEOSettings from "./pages/SEOSettings";
import ChangePassword from "./pages/ChangePassword";
import SubscribersManager from "./pages/SubscribersManager";
import ManageArticles from "./pages/ManageArticles";
import ArticleSeeder from "./pages/ArticleSeeder";
import AboutUs from "./pages/AboutUs";
import ContactUs from "./pages/ContactUs";
import Contribute from "./pages/Contribute";
import ContributionsManager from "./pages/ContributionsManager";
import ContactMessages from "./pages/ContactMessages";
import ArticleScraper from "./pages/ArticleScraper";
import PerArticleAnalytics from "./pages/PerArticleAnalytics";
import BulkOptimize from "./pages/BulkOptimize";
import Login from "./pages/Login";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import TermsOfService from "./pages/TermsOfService";
import Disclaimer from "./pages/Disclaimer";
import ProtectedRoute from "./components/ProtectedRoute";
import { Toaster } from "./components/ui/toaster";
import { ThemeProvider } from "./contexts/ThemeContext";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [adsConfig, setAdsConfig] = useState(null);

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

  return (
    <ThemeProvider>
    <div className="App">
      <Helmet>
        <title>9xCodes - Linux Server Commands, Ubuntu, CentOS Tutorials & Code Snippets</title>
        <meta
          name="description"
          content="Discover ready-to-use Linux server commands, tutorials, and code snippets for Ubuntu, CentOS, Debian. Learn how to install cPanel, configure SSH, setup firewalls, and master server administration with copy-paste commands."
        />
        <meta
          name="keywords"
          content="linux commands, ubuntu tutorial, centos commands, server administration, cpanel installation, ssh security, firewall configuration, nginx setup, mysql installation, docker commands, linux tutorial, bash commands, server commands, system administration"
        />
        <meta name="author" content="9xCodes" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://9xcodes.com" />
        
        {/* Open Graph Tags */}
        <meta property="og:type" content="website" />
        <meta property="og:title" content="9xCodes - Linux Server Commands & Tutorials" />
        <meta
          property="og:description"
          content="Your ultimate resource for Linux server commands, code snippets, and step-by-step tutorials for Ubuntu, CentOS, and Debian."
        />
        <meta property="og:url" content="https://9xcodes.com" />
        <meta property="og:site_name" content="9xCodes" />
        
        {/* Twitter Card Tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="9xCodes - Linux Server Commands & Tutorials" />
        <meta
          name="twitter:description"
          content="Ready-to-use Linux commands and tutorials for server administration"
        />
        
        {/* Additional SEO */}
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta httpEquiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="language" content="English" />
        
        {/* Google AdSense Script */}
        {adsConfig?.enabled && (
          <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
        )}
      </Helmet>

      <BrowserRouter>
        <div className="flex flex-col min-h-screen">
          <Header onSearch={setSearchQuery} />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home searchQuery={searchQuery} adsConfig={adsConfig} />} />
              <Route path="/snippet/:slug" element={<SnippetDetail adsConfig={adsConfig} />} />
              <Route path="/about" element={<AboutUs />} />
              <Route path="/contact" element={<ContactUs />} />
              <Route path="/contribute" element={<Contribute />} />
              <Route path="/privacy-policy" element={<PrivacyPolicy />} />
              <Route path="/terms-of-service" element={<TermsOfService />} />
              <Route path="/disclaimer" element={<Disclaimer />} />
              <Route path="/login" element={<Login />} />
              <Route
                path="/admin"
                element={
                  <ProtectedRoute>
                    <AdminPanel />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/ads"
                element={
                  <ProtectedRoute>
                    <GoogleAdsManager />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/analytics"
                element={
                  <ProtectedRoute>
                    <AnalyticsDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/seo"
                element={
                  <ProtectedRoute>
                    <SEOSettings />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/change-password"
                element={
                  <ProtectedRoute>
                    <ChangePassword />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/subscribers"
                element={
                  <ProtectedRoute>
                    <SubscribersManager />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/articles"
                element={
                  <ProtectedRoute>
                    <ManageArticles />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/seeder"
                element={
                  <ProtectedRoute>
                    <ArticleSeeder />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/contributions"
                element={
                  <ProtectedRoute>
                    <ContributionsManager />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/messages"
                element={
                  <ProtectedRoute>
                    <ContactMessages />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/scraper"
                element={
                  <ProtectedRoute>
                    <ArticleScraper />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/per-article-analytics"
                element={
                  <ProtectedRoute>
                    <PerArticleAnalytics />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/bulk-optimize"
                element={
                  <ProtectedRoute>
                    <BulkOptimize />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </main>
          <Footer />
        </div>
        <Toaster />
      </BrowserRouter>

      {/* JSON-LD Structured Data for SEO */}
      <script type="application/ld+json">
        {JSON.stringify({
          "@context": "https://schema.org",
          "@type": "WebSite",
          "name": "9xCodes",
          "url": "https://9xcodes.com",
          "description": "Linux server commands, tutorials, and code snippets for Ubuntu, CentOS, and Debian",
          "potentialAction": {
            "@type": "SearchAction",
            "target": "https://9xcodes.com?search={search_term_string}",
            "query-input": "required name=search_term_string"
          }
        })}
      </script>
    </div>
    </ThemeProvider>
  );
}

export default App;
