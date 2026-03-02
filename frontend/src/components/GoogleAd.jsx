import React, { useEffect, useRef } from 'react';

const GoogleAd = ({ adCode, className = '' }) => {
  const adRef = useRef(null);
  const pushed = useRef(false);

  useEffect(() => {
    if (!adCode || !adRef.current || pushed.current) return;
    
    // Check if adsbygoogle script is loaded
    const tryPush = () => {
      try {
        if (window.adsbygoogle && adRef.current.querySelector('ins.adsbygoogle')) {
          (window.adsbygoogle = window.adsbygoogle || []).push({});
          pushed.current = true;
        }
      } catch (e) {
        console.error('Ad push error:', e);
      }
    };

    // Try immediately, then retry after script loads
    tryPush();
    if (!pushed.current) {
      const timer = setTimeout(tryPush, 2000);
      return () => clearTimeout(timer);
    }
  }, [adCode]);

  if (!adCode || adCode.trim() === '') return null;

  return (
    <div className={`google-ad-container ${className}`} ref={adRef}>
      <div dangerouslySetInnerHTML={{ __html: adCode }} />
    </div>
  );
};

export default GoogleAd;
