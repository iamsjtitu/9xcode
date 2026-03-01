import React, { useState } from 'react';
import { Check, Copy } from 'lucide-react';

const CodeBlock = ({ code, language = 'bash', title }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group" data-testid="code-block">
      {title && (
        <div className="bg-slate-700 px-4 py-2 rounded-t-lg text-sm text-slate-300 font-medium">
          {title}
        </div>
      )}
      <div className="relative bg-slate-900 rounded-lg overflow-hidden">
        <button
          onClick={handleCopy}
          data-testid="copy-code-btn"
          className={`absolute top-2 right-2 flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-300 ${
            copied
              ? 'bg-green-500/20 text-green-400 border border-green-500/30'
              : 'bg-slate-700/80 text-slate-300 hover:bg-slate-600 hover:text-white border border-slate-600'
          }`}
        >
          {copied ? (
            <>
              <Check className="h-3.5 w-3.5" />
              Copied!
            </>
          ) : (
            <>
              <Copy className="h-3.5 w-3.5" />
              Copy
            </>
          )}
        </button>
        <pre className="p-4 pr-24 overflow-x-auto">
          <code className="text-sm text-slate-300 font-mono">{code}</code>
        </pre>
      </div>
    </div>
  );
};

export default CodeBlock;