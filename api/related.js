// Related endpoint for Vercel using google-trends-api
const googleTrends = require('google-trends-api');

module.exports = async (req, res) => {
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

  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { keyword, geo = 'US', timeframe = 'today 5-y' } = req.query;

    if (!keyword) {
      return res.status(400).json({ error: 'keyword parameter is required' });
    }

    // Get related topics and queries using google-trends-api
    const relatedTopics = await googleTrends.relatedTopics({
      keyword: keyword,
      startTime: getStartTime(timeframe),
      geo: geo,
    });

    const relatedQueries = await googleTrends.relatedQueries({
      keyword: keyword,
      startTime: getStartTime(timeframe),
      geo: geo,
    });

    const result = {
      keyword: keyword,
      geo: geo,
      timeframe: timeframe,
      related_topics: JSON.parse(relatedTopics),
      related_queries: JSON.parse(relatedQueries)
    };

    res.status(200).json(result);
  } catch (error) {
    console.error('Error fetching related data:', error);
    res.status(500).json({ error: error.message || 'Failed to fetch related data' });
  }
};

// Helper function to convert timeframe to Date
function getStartTime(timeframe) {
  const now = new Date();
  
  switch (timeframe) {
    case 'now 1-H':
      return new Date(now.getTime() - (1 * 60 * 60 * 1000));
    case 'now 4-H':
      return new Date(now.getTime() - (4 * 60 * 60 * 1000));
    case 'now 1-d':
      return new Date(now.getTime() - (1 * 24 * 60 * 60 * 1000));
    case 'now 7-d':
      return new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000));
    case 'today 1-m':
      return new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000));
    case 'today 3-m':
      return new Date(now.getTime() - (90 * 24 * 60 * 60 * 1000));
    case 'today 12-m':
      return new Date(now.getTime() - (365 * 24 * 60 * 60 * 1000));
    case 'today 5-y':
    default:
      return new Date(now.getTime() - (5 * 365 * 24 * 60 * 60 * 1000));
  }
}
