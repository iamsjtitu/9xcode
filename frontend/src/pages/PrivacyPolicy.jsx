import React from 'react';
import { Shield, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';

const PrivacyPolicy = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Helmet>
        <title>Privacy Policy - 9xCodes</title>
        <meta name="description" content="Privacy Policy for 9xCodes.com - Learn how we collect, use, and protect your personal information." />
      </Helmet>

      <section className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-12">
        <div className="container mx-auto px-4 text-center max-w-3xl">
          <Shield className="h-10 w-10 mx-auto text-blue-400 mb-3" />
          <h1 className="text-4xl font-bold mb-3">Privacy Policy</h1>
          <p className="text-slate-300 text-sm">Last updated: March 2026</p>
        </div>
      </section>

      <div className="container mx-auto px-4 py-10 max-w-3xl">
        <Link to="/" className="inline-flex items-center text-sm text-blue-600 hover:underline mb-6">
          <ArrowLeft className="h-4 w-4 mr-1" /> Back to Home
        </Link>

        <div className="prose prose-slate max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">1. Introduction</h2>
            <p className="text-slate-600 leading-relaxed">
              Welcome to 9xCodes.com ("we," "our," or "us"). We are committed to protecting your privacy and personal information. 
              This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website 
              9xCodes.com (the "Site"). Please read this policy carefully. By using the Site, you agree to the collection and use 
              of information in accordance with this policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">2. Information We Collect</h2>
            <h3 className="text-lg font-semibold text-slate-800 mb-2">Personal Information</h3>
            <p className="text-slate-600 leading-relaxed mb-3">
              We may collect personal information that you voluntarily provide when you:
            </p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1">
              <li>Subscribe to our newsletter (email address)</li>
              <li>Submit a contact form (name, email, message)</li>
              <li>Contribute articles (name, email)</li>
              <li>Leave comments on articles (name)</li>
            </ul>

            <h3 className="text-lg font-semibold text-slate-800 mb-2 mt-4">Automatically Collected Information</h3>
            <p className="text-slate-600 leading-relaxed">
              When you visit our Site, we may automatically collect certain information, including your IP address, browser type, 
              operating system, referring URLs, pages viewed, and the dates/times of your visits. This information is used to 
              analyze trends, administer the Site, and improve user experience.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">3. Cookies and Tracking Technologies</h2>
            <p className="text-slate-600 leading-relaxed">
              We use cookies and similar tracking technologies to enhance your browsing experience. Cookies are small data files 
              stored on your device. We use:
            </p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1 mt-2">
              <li><strong>Essential Cookies:</strong> Required for basic site functionality (e.g., theme preferences, bookmarks)</li>
              <li><strong>Analytics Cookies:</strong> Help us understand how visitors interact with the Site</li>
              <li><strong>Advertising Cookies:</strong> Used by Google AdSense to serve relevant advertisements</li>
            </ul>
            <p className="text-slate-600 leading-relaxed mt-3">
              You can control cookies through your browser settings. Disabling cookies may affect your experience on the Site.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">4. Google AdSense</h2>
            <p className="text-slate-600 leading-relaxed">
              We use Google AdSense to display advertisements on our Site. Google AdSense uses cookies to serve ads based on 
              your prior visits to our Site and other websites. Google's use of advertising cookies enables it and its partners 
              to serve ads based on your visit to our Site and/or other sites on the Internet. You may opt out of personalized 
              advertising by visiting <a href="https://www.google.com/settings/ads" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">Google Ads Settings</a>.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">5. How We Use Your Information</h2>
            <p className="text-slate-600 leading-relaxed">We use the information we collect to:</p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1 mt-2">
              <li>Provide, maintain, and improve our Site</li>
              <li>Send newsletter updates (only if you subscribe)</li>
              <li>Respond to your inquiries and contact form submissions</li>
              <li>Analyze Site usage and optimize performance</li>
              <li>Display relevant advertisements through Google AdSense</li>
              <li>Prevent fraud and ensure security</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">6. Data Sharing</h2>
            <p className="text-slate-600 leading-relaxed">
              We do not sell, trade, or rent your personal information to third parties. We may share information with:
            </p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1 mt-2">
              <li><strong>Google AdSense:</strong> For advertising purposes (see Section 4)</li>
              <li><strong>Analytics Providers:</strong> To help analyze Site usage</li>
              <li><strong>Legal Requirements:</strong> If required by law or to protect our rights</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">7. Data Security</h2>
            <p className="text-slate-600 leading-relaxed">
              We implement appropriate security measures to protect your personal information. However, no method of transmission 
              over the Internet is 100% secure. While we strive to protect your data, we cannot guarantee absolute security.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">8. Your Rights</h2>
            <p className="text-slate-600 leading-relaxed">You have the right to:</p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1 mt-2">
              <li>Access the personal information we hold about you</li>
              <li>Request correction or deletion of your personal information</li>
              <li>Unsubscribe from our newsletter at any time</li>
              <li>Opt out of personalized advertising</li>
            </ul>
            <p className="text-slate-600 leading-relaxed mt-3">
              To exercise these rights, please contact us at <a href="mailto:contact@9xcodes.com" className="text-blue-600 hover:underline">contact@9xcodes.com</a>.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">9. Children's Privacy</h2>
            <p className="text-slate-600 leading-relaxed">
              Our Site is not directed to children under 13. We do not knowingly collect personal information from children. 
              If we learn we have collected such information, we will take steps to delete it promptly.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">10. Changes to This Policy</h2>
            <p className="text-slate-600 leading-relaxed">
              We may update this Privacy Policy from time to time. Changes will be posted on this page with an updated date. 
              Continued use of the Site after changes constitutes acceptance of the updated policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">11. Contact Us</h2>
            <p className="text-slate-600 leading-relaxed">
              If you have questions about this Privacy Policy, please <Link to="/contact" className="text-blue-600 hover:underline">contact us</Link> or 
              email us at <a href="mailto:contact@9xcodes.com" className="text-blue-600 hover:underline">contact@9xcodes.com</a>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;
