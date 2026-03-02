import React from 'react';
import { Terminal, Users, Target, Heart } from 'lucide-react';
import { Card, CardContent } from '../components/ui/card';

const AboutUs = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      {/* Hero */}
      <section className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-16">
        <div className="container mx-auto px-4 text-center max-w-3xl">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            About 9xCodes
          </h1>
          <p className="text-base text-slate-300">
            Helping developers and sysadmins solve problems 9x faster with ready-to-use code snippets and server commands.
          </p>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        {/* Mission */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Target className="h-6 w-6 text-blue-600" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">Our Mission</h2>
            </div>
            <p className="text-slate-600 leading-relaxed">
              9xCodes was built with a simple idea — every developer and system administrator should have instant access to reliable, copy-paste ready commands and tutorials. No more digging through outdated documentation or unreliable forum posts. We provide step-by-step guides that just work.
            </p>
          </CardContent>
        </Card>

        {/* What We Offer */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-green-100 rounded-lg">
                <Terminal className="h-6 w-6 text-green-600" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">What We Offer</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                'Linux server administration tutorials',
                'Copy-paste ready code snippets',
                'Security hardening guides',
                'Database setup and management',
                'Docker and virtualization',
                'Networking and firewall configuration',
                'Web hosting and deployment',
                'CCTV and surveillance system setup',
                'Billing system configuration',
                'Monitoring and backup solutions',
              ].map((item, idx) => (
                <div key={idx} className="flex items-center gap-2 text-slate-600">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full flex-shrink-0" />
                  <span className="text-sm">{item}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Community */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">Community Driven</h2>
            </div>
            <p className="text-slate-600 leading-relaxed">
              9xCodes is not just a website — it's a community. We welcome contributors who want to share their knowledge. If you have expertise in server management, coding, or DevOps, you can submit your articles through our Contribute page. Every submission is reviewed by our team to ensure quality before publishing.
            </p>
          </CardContent>
        </Card>

        {/* Values */}
        <Card>
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-red-100 rounded-lg">
                <Heart className="h-6 w-6 text-red-600" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">Our Values</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h3 className="font-semibold text-slate-800 mb-1">Accuracy</h3>
                <p className="text-sm text-slate-500">Every command and tutorial is tested before publishing.</p>
              </div>
              <div>
                <h3 className="font-semibold text-slate-800 mb-1">Simplicity</h3>
                <p className="text-sm text-slate-500">Step-by-step guides anyone can follow, beginner to advanced.</p>
              </div>
              <div>
                <h3 className="font-semibold text-slate-800 mb-1">Open Knowledge</h3>
                <p className="text-sm text-slate-500">Free access to all tutorials and code snippets forever.</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AboutUs;
