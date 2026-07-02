(function () {
  'use strict';

  const host = window.location.hostname;

  if (host === '127.0.0.1' || host === 'localhost') {
    window.SWAT_API_BASE = window.location.origin;
    return;
  }

  if (host.endsWith('.github.io')) {
    window.SWAT_API_BASE = 'https://swat-lvpd-api.onrender.com';
    return;
  }

  window.SWAT_API_BASE = window.location.origin;
})();
