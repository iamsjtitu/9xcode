import React, { useEffect, useRef } from 'react';

const AD_CONFIGS = {
  native: {
    key: '83ec8ce2be72cec0f7bef76d294d8e19',
    src: 'https://pl29263904.profitablecpmratenetwork.com/83ec8ce2be72cec0f7bef76d294d8e19/invoke.js',
    type: 'container',
  },
  banner728: {
    key: 'c50c0760451505e6fd921fd064d9f9a6',
    src: 'https://www.highperformanceformat.com/c50c0760451505e6fd921fd064d9f9a6/invoke.js',
    type: 'atOptions',
    height: 90,
    width: 728,
  },
  banner300: {
    key: '58908c24ba7fcad2fb3e52d6374a8fd9',
    src: 'https://www.highperformanceformat.com/58908c24ba7fcad2fb3e52d6374a8fd9/invoke.js',
    type: 'atOptions',
    height: 250,
    width: 300,
  },
};

const AdsterraAd = ({ variant = 'native', className = '' }) => {
  const containerRef = useRef(null);
  const loaded = useRef(false);

  useEffect(() => {
    if (loaded.current || !containerRef.current) return;
    loaded.current = true;

    const config = AD_CONFIGS[variant];
    if (!config) return;

    if (config.type === 'container') {
      // Native banner - async script + container div
      const container = document.createElement('div');
      container.id = `container-${config.key}`;
      containerRef.current.appendChild(container);

      const script = document.createElement('script');
      script.async = true;
      script.dataset.cfasync = 'false';
      script.src = config.src;
      containerRef.current.appendChild(script);
    } else {
      // atOptions banner (728x90 or 300x250)
      const optScript = document.createElement('script');
      optScript.text = `
        atOptions = {
          'key' : '${config.key}',
          'format' : 'iframe',
          'height' : ${config.height},
          'width' : ${config.width},
          'params' : {}
        };
      `;
      containerRef.current.appendChild(optScript);

      const invokeScript = document.createElement('script');
      invokeScript.src = config.src;
      containerRef.current.appendChild(invokeScript);
    }

    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
      loaded.current = false;
    };
  }, [variant]);

  return (
    <div
      ref={containerRef}
      className={`adsterra-ad flex justify-center items-center overflow-hidden ${className}`}
      data-testid={`adsterra-${variant}`}
      style={{ position: 'relative', zIndex: 1 }}
    />
  );
};

export default AdsterraAd;
