import React from 'react';
import { AlertTriangle, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';

const Disclaimer = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Helmet>
        <title>Disclaimer - 9xCodes</title>
        <meta name="description" content="Disclaimer for 9xCodes.com - Important information about the use of code snippets and tutorials on our site." />
      </Helmet>

      <section className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-12">
        <div className="container mx-auto px-4 text-center max-w-3xl">
          <AlertTriangle className="h-10 w-10 mx-auto text-amber-400 mb-3" />
          <h1 className="text-4xl font-bold mb-3">Disclaimer</h1>
          <p className="text-slate-300 text-sm">Last updated: March 2026</p>
        </div>
      </section>

      <div className="container mx-auto px-4 py-10 max-w-3xl">
        <Link to="/" className="inline-flex items-center text-sm text-blue-600 hover:underline mb-6">
          <ArrowLeft className="h-4 w-4 mr-1" /> Back to Home
        </Link>

        <div className="prose prose-slate max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">General Disclaimer</h2>
            <p className="text-slate-600 leading-relaxed">
              The information provided on 9xCodes.com is for general educational and informational purposes only. All code 
              snippets, server commands, tutorials, and technical guides are provided "as is" without any representations 
              or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, 
              or availability of the information contained on the Site.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">Use at Your Own Risk</h2>
            <p className="text-slate-600 leading-relaxed">
              Any reliance you place on the information provided on this Site is strictly at your own risk. We strongly 
              recommend that you:
            </p>
            <ul className="list-disc pl-6 text-slate-600 space-y-2 mt-2">
              <li><strong>Test in a safe environment:</strong> Always test code snippets and commands in a development or staging environment before deploying to production systems.</li>
              <li><strong>Back up your data:</strong> Create backups before making system changes based on our tutorials.</li>
              <li><strong>Verify compatibility:</strong> Check that commands and configurations are compatible with your specific operating system version and environment.</li>
              <li><strong>Read documentation:</strong> Supplement our guides with official documentation for the software or tools being discussed.</li>
              <li><strong>Understand the commands:</strong> Never blindly copy and paste commands without understanding what they do, especially commands that require root/sudo access.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">No Professional Advice</h2>
            <p className="text-slate-600 leading-relaxed">
              The content on this Site does not constitute professional IT consulting, system administration advice, or 
              technical support. For critical systems and infrastructure, we recommend consulting with qualified IT 
              professionals who can assess your specific requirements and environment.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">Third-Party Content</h2>
            <p className="text-slate-600 leading-relaxed">
              Our Site may include content contributed by community members and references to third-party tools, software, 
              and services. We do not endorse or guarantee the reliability of any third-party products or services mentioned. 
              External links are provided for convenience and do not signify endorsement.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">Advertising Disclaimer</h2>
            <p className="text-slate-600 leading-relaxed">
              This Site displays advertisements through Google AdSense. These advertisements are provided by third-party 
              advertisers and do not constitute endorsement or recommendation by 9xCodes.com. We have no control over the 
              content of advertisements and are not responsible for any claims made in them.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">Content Accuracy</h2>
            <p className="text-slate-600 leading-relaxed">
              Technology evolves rapidly, and while we strive to keep our content up to date, some articles may reference 
              older software versions or deprecated commands. Always verify that the instructions are applicable to your 
              current software versions. If you find outdated or incorrect information, please <Link to="/contact" className="text-blue-600 hover:underline">contact us</Link> so 
              we can update it.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">Limitation of Liability</h2>
            <p className="text-slate-600 leading-relaxed">
              In no event shall 9xCodes.com, its owner, or contributors be liable for any loss or damage including without 
              limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of 
              data or profits arising out of, or in connection with, the use of this Site.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-900 mb-3">Contact</h2>
            <p className="text-slate-600 leading-relaxed">
              If you have any concerns about the content on this Site, please <Link to="/contact" className="text-blue-600 hover:underline">contact us</Link> or 
              email <a href="mailto:contact@9xcodes.com" className="text-blue-600 hover:underline">contact@9xcodes.com</a>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Disclaimer;
