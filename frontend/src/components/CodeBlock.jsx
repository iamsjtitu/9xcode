import React, { useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { Button } from './ui/button';

const CodeBlock = ({ code, language = 'bash', title }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group">
      {title && (
        <div className="bg-slate-700 px-4 py-2 rounded-t-lg text-sm text-slate-300 font-medium">
          {title}
        </div>
      )}
      <div className="relative bg-slate-900 rounded-lg overflow-hidden">
        <Button
          size="sm"
          variant="ghost"
          onClick={handleCopy}
          className="absolute top-2 right-2 text-slate-400 hover:text-white hover:bg-slate-700 transition-all opacity-0 group-hover:opacity-100"
        >
          {copied ? (
            <>
              <Check className="h-4 w-4 mr-1" />
              Copied!
            </>
          ) : (
            <>
              <Copy className="h-4 w-4 mr-1" />
              Copy
            </>
          )}
        </Button>
        <pre className="p-4 overflow-x-auto">
          <code className="text-sm text-slate-300 font-mono">{code}</code>
        </pre>
      </div>
    </div>
  );
};

export default CodeBlock;