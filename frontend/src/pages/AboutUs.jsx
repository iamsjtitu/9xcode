import React from 'react';
import { Terminal, Users, Target, Heart, BookOpen, Shield, Globe, Award } from 'lucide-react';
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
          <p className="text-base text-slate-300 leading-relaxed">
            Your trusted resource for production-ready code snippets, server administration guides, and step-by-step technical tutorials. Helping developers and system administrators work smarter since 2024.
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
            <p className="text-slate-600 leading-relaxed mb-4">
              9xCodes was founded with a clear mission: to provide developers, system administrators, and IT professionals with the most reliable, well-documented, and easy-to-follow technical tutorials available on the internet.
            </p>
            <p className="text-slate-600 leading-relaxed mb-4">
              We understand the frustration of searching for a simple command or configuration guide, only to find outdated documentation, incomplete instructions, or forum posts that no longer work. That's why every tutorial on 9xCodes is carefully structured with step-by-step instructions, accurate commands, and detailed explanations that help you understand not just the "how" but also the "why."
            </p>
            <p className="text-slate-600 leading-relaxed">
              Whether you're setting up your first Linux server, configuring a complex networking environment, deploying containerized applications, or managing CCTV surveillance systems, 9xCodes has you covered with tutorials that just work.
            </p>
          </CardContent>
        </Card>

        {/* What We Cover */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-green-100 rounded-lg">
                <Terminal className="h-6 w-6 text-green-600" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">What We Cover</h2>
            </div>
            <p className="text-slate-600 leading-relaxed mb-6">
              Our content library spans across multiple domains of IT infrastructure and software development. Each article is written to be practical, actionable, and beginner-friendly while still being valuable for experienced professionals.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { title: 'Linux Server Administration', desc: 'Ubuntu, CentOS, Debian setup, configuration, and management' },
                { title: 'Copy-Paste Ready Snippets', desc: 'Tested commands you can use immediately in production' },
                { title: 'Security Hardening Guides', desc: 'Firewall rules, SSH configuration, and best practices' },
                { title: 'Database Management', desc: 'MySQL, PostgreSQL, MongoDB installation and optimization' },
                { title: 'Docker & Virtualization', desc: 'Container deployment, Docker Compose, and VM management' },
                { title: 'Networking & Firewall', desc: 'iptables, UFW, DNS configuration, and VPN setup' },
                { title: 'Web Hosting & Deployment', desc: 'Nginx, Apache, SSL certificates, and CI/CD pipelines' },
                { title: 'CCTV & Surveillance', desc: 'IP camera setup, NVR configuration, and remote access' },
                { title: 'Billing & Business Tools', desc: 'WHMCS, billing system configuration and automation' },
                { title: 'Monitoring & Backup', desc: 'System monitoring, automated backups, and disaster recovery' },
              ].map((item, idx) => (
                <div key={idx} className="p-3 rounded-lg border border-slate-100 hover:border-blue-200 transition-colors">
                  <h3 className="font-semibold text-slate-800 text-sm mb-1">{item.title}</h3>
                  <p className="text-xs text-slate-500">{item.desc}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Content Quality */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-amber-100 rounded-lg">
                <Award className="h-6 w-6 text-amber-600" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">Our Content Quality Standards</h2>
            </div>
            <p className="text-slate-600 leading-relaxed mb-4">
              Quality is at the heart of everything we publish. Every article on 9xCodes goes through a rigorous quality assurance process:
            </p>
            <div className="space-y-3">
              {[
                { title: 'Technically Verified', desc: 'All commands and code snippets are tested on real systems before publishing.' },
                { title: 'Regularly Updated', desc: 'Articles are reviewed and updated to ensure compatibility with the latest software versions.' },
                { title: 'Beginner-Friendly', desc: 'Each guide includes prerequisites, detailed explanations, and step-by-step instructions.' },
                { title: 'SEO Optimized', desc: 'Content is structured for easy discoverability while maintaining readability.' },
                { title: 'Community Reviewed', desc: 'Reader feedback helps us continuously improve our tutorials.' },
              ].map((item, idx) => (
                <div key={idx} className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                  <Shield className="h-4 w-4 text-green-500 mt-1 flex-shrink-0" />
                  <div>
                    <span className="font-medium text-slate-800 text-sm">{item.title}</span>
                    <span className="text-sm text-slate-500 ml-1">— {item.desc}</span>
                  </div>
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
            <p className="text-slate-600 leading-relaxed mb-4">
              9xCodes is more than just a website — it's a growing community of IT professionals, developers, and technology enthusiasts who believe in sharing knowledge openly.
            </p>
            <p className="text-slate-600 leading-relaxed mb-4">
              We welcome contributions from experienced professionals who want to share their expertise with the community. Whether you're a seasoned system administrator, a DevOps engineer, or a networking specialist, your knowledge can help thousands of others solve real-world problems.
            </p>
            <p className="text-slate-600 leading-relaxed">
              Every submission goes through our editorial review process to ensure accuracy, completeness, and adherence to our quality standards before being published on the platform.
            </p>
          </CardContent>
        </Card>

        {/* Stats */}
        <Card className="mb-8 bg-gradient-to-r from-blue-600 to-blue-700">
          <CardContent className="p-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center text-white">
              <div>
                <div className="text-3xl font-bold mb-1">290+</div>
                <div className="text-blue-200 text-sm">Technical Tutorials</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-1">10+</div>
                <div className="text-blue-200 text-sm">Categories</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-1">24/7</div>
                <div className="text-blue-200 text-sm">Free Access</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-1">100%</div>
                <div className="text-blue-200 text-sm">Tested Content</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Values */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-red-100 rounded-lg">
                <Heart className="h-6 w-6 text-red-600" />
              </div>
              <h2 className="text-xl font-bold text-slate-900">Our Core Values</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-4 bg-slate-50 rounded-lg">
                <h3 className="font-semibold text-slate-800 mb-2">Accuracy First</h3>
                <p className="text-sm text-slate-500 leading-relaxed">Every command, configuration, and code snippet is tested on real systems before publishing. We never publish untested content.</p>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <h3 className="font-semibold text-slate-800 mb-2">Simplicity Always</h3>
                <p className="text-sm text-slate-500 leading-relaxed">We believe complex topics can be explained simply. Our step-by-step approach makes even advanced concepts accessible to beginners.</p>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <h3 className="font-semibold text-slate-800 mb-2">Open Knowledge</h3>
                <p className="text-sm text-slate-500 leading-relaxed">All our tutorials and code snippets are freely accessible. We believe technical knowledge should be available to everyone, everywhere.</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Contact CTA */}
        <Card>
          <CardContent className="p-8 text-center">
            <Globe className="h-10 w-10 text-blue-600 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-slate-900 mb-2">Get in Touch</h2>
            <p className="text-slate-600 mb-4 max-w-lg mx-auto">
              Have a question, suggestion, or want to contribute? We'd love to hear from you. Reach out to us through our contact page or submit your article through the contribute section.
            </p>
            <div className="flex justify-center gap-4">
              <a href="/contact" className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
                Contact Us
              </a>
              <a href="/contribute" className="inline-flex items-center px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-sm font-medium">
                Contribute
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AboutUs;
