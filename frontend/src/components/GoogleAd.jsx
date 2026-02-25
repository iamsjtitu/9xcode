import React, { useEffect } from 'react';

const GoogleAd = ({ adCode, className = '' }) => {
  useEffect(() => {
    // Load ads after component mounts
    if (adCode && window) {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      } catch (e) {
        console.error('Error loading ad:', e);
      }
    }
  }, [adCode]);

  if (!adCode || adCode.trim() === '') {
    return null;
  }

  return (
    <div className={`google-ad-container ${className}`}>
      <div dangerouslySetInnerHTML={{ __html: adCode }} />
    </div>
  );
};

export default GoogleAd;
