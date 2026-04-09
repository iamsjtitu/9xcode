import React from 'react';
import { FileText, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';

const TermsOfService = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Helmet>
        <title>Terms of Service - 9xCodes</title>
        <meta name="description" content="Terms of Service for 9xCodes.com - Read the terms and conditions governing your use of our website." />
      </Helmet>

      <section className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-12">
        <div className="container mx-auto px-4 text-center max-w-3xl">
          <FileText className="h-10 w-10 mx-auto text-blue-400 mb-3" />
          <h1 className="text-4xl font-bold mb-3">Terms of Service</h1>
          <p className="text-slate-300 text-sm">Last updated: March 2026</p>
        </div>
      </section>

      <div className="container mx-auto px-4 py-10 max-w-3xl">
        <Link to="/" className="inline-flex items-center text-sm text-blue-600 hover:underline mb-6">
          <ArrowLeft className="h-4 w-4 mr-1" /> Back to Home
        </Link>

        <div className="prose prose-slate max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">1. Acceptance of Terms</h2>
            <p className="text-slate-600 leading-relaxed">
              By accessing and using 9xCodes.com (the "Site"), you accept and agree to be bound by these Terms of Service. 
              If you do not agree to these terms, please do not use the Site. We reserve the right to modify these terms at 
              any time, and your continued use of the Site constitutes acceptance of any changes.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">2. Description of Service</h2>
            <p className="text-slate-600 leading-relaxed">
              9xCodes.com is an educational platform that provides code snippets, server commands, tutorials, and technical 
              guides for developers, system administrators, and IT professionals. Our content covers topics including but not 
              limited to Linux administration, networking, web hosting, virtualization, databases, and programming.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">3. Use of Content</h2>
            <p className="text-slate-600 leading-relaxed mb-3">
              The code snippets, commands, and tutorials on this Site are provided for educational and informational purposes. 
              You may:
            </p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1">
              <li>Use the code snippets and commands in your own projects</li>
              <li>Share links to our articles</li>
              <li>Reference our content with proper attribution</li>
            </ul>
            <p className="text-slate-600 leading-relaxed mt-3">
              You may not reproduce, distribute, or republish our articles in their entirety without written permission.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">4. User Contributions</h2>
            <p className="text-slate-600 leading-relaxed">
              Users may submit articles, comments, and other content to the Site. By submitting content, you grant 9xCodes.com 
              a non-exclusive, royalty-free license to use, modify, and display your contribution. You represent that your 
              submitted content is original and does not infringe on any third-party rights. We reserve the right to review, 
              edit, or remove any user-submitted content at our discretion.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">5. Disclaimer of Warranties</h2>
            <p className="text-slate-600 leading-relaxed">
              The content on this Site is provided "as is" without warranties of any kind, either express or implied. While we 
              strive to provide accurate and up-to-date information, we do not guarantee that:
            </p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1 mt-2">
              <li>All code snippets and commands will work in every environment</li>
              <li>The content is free of errors or omissions</li>
              <li>The Site will be available at all times without interruption</li>
            </ul>
            <p className="text-slate-600 leading-relaxed mt-3">
              Always test code in a safe environment before using it in production systems.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">6. Limitation of Liability</h2>
            <p className="text-slate-600 leading-relaxed">
              9xCodes.com and its administrators shall not be liable for any direct, indirect, incidental, consequential, 
              or punitive damages arising from your use of the Site or any code, commands, or instructions provided herein. 
              You use all content at your own risk. We are not responsible for any damage to your systems or data resulting 
              from the implementation of any content found on this Site.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">7. Intellectual Property</h2>
            <p className="text-slate-600 leading-relaxed">
              The Site's design, logo, original content, and compilation of information are the intellectual property of 
              9xCodes.com and are protected by applicable copyright and trademark laws. Third-party trademarks, product 
              names, and logos mentioned on the Site are the property of their respective owners.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">8. Third-Party Links and Advertisements</h2>
            <p className="text-slate-600 leading-relaxed">
              The Site may contain links to third-party websites and display advertisements through Google AdSense. We are 
              not responsible for the content, accuracy, or practices of third-party sites. Clicking on advertisements or 
              third-party links is at your own discretion and risk.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">9. Prohibited Activities</h2>
            <p className="text-slate-600 leading-relaxed">You agree not to:</p>
            <ul className="list-disc pl-6 text-slate-600 space-y-1 mt-2">
              <li>Scrape or copy our content in bulk for redistribution</li>
              <li>Use the Site for any unlawful purpose</li>
              <li>Attempt to gain unauthorized access to the Site's systems</li>
              <li>Submit malicious code, spam, or misleading content</li>
              <li>Interfere with the Site's operation or other users' experience</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">10. Governing Law</h2>
            <p className="text-slate-600 leading-relaxed">
              These Terms shall be governed by and construed in accordance with applicable laws. Any disputes arising from 
              these Terms or your use of the Site shall be resolved through appropriate legal channels.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">11. Contact</h2>
            <p className="text-slate-600 leading-relaxed">
              For questions about these Terms of Service, please <Link to="/contact" className="text-blue-600 hover:underline">contact us</Link> or 
              email <a href="mailto:contact@9xcodes.com" className="text-blue-600 hover:underline">contact@9xcodes.com</a>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default TermsOfService;
