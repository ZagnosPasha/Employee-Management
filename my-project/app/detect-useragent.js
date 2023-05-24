if ('userAgentData' in navigator) {
    const ua = navigator.userAgentData;
    const browserName = ua.brands.filter(b => b.brand === 'Google Chrome')[0].version;
    const osName = ua.platform;
    // Use browserName and osName as needed.
  } else {
    // Fallback to using navigator.userAgent, navigator.appVersion, and navigator.platform.
  }