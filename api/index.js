// Main status endpoint for Vercel - n8n Trends API
module.exports = (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');
  
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow GET requests for status
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Return API status and available endpoints
  res.status(200).json({
    ok: true,
    service: 'n8n-trends-api',
    runtime: 'nodejs',
    framework: 'vercel',
    version: '2.0.0',
    description: 'Google Trends API using Node.js and google-trends-api',
    endpoints: [
      {
        path: '/api/health',
        method: 'GET',
        description: 'Health check endpoint'
      },
      {
        path: '/api/trends',
        method: 'GET',
        description: 'Get trends data for keywords',
        parameters: {
          keywords: 'Comma-separated list of keywords (required)',
          geo: 'Geographic location (default: US)',
          timeframe: 'Time range (default: today 5-y)'
        }
      },
      {
        path: '/api/compare',
        method: 'GET',
        description: 'Compare multiple keywords (min 2)',
        parameters: {
          keywords: 'Comma-separated list of keywords (required, min 2)',
          geo: 'Geographic location (default: US)',
          timeframe: 'Time range (default: today 5-y)'
        }
      },
      {
        path: '/api/related',
        method: 'GET',
        description: 'Get related topics and queries for a keyword',
        parameters: {
          keyword: 'Single keyword (required)',
          geo: 'Geographic location (default: US)',
          timeframe: 'Time range (default: today 5-y)'
        }
      }
    ],
    timestamp: new Date().toISOString(),
    author: 'AmirAliTheGoat'
  });
};
