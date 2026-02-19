// API Configuration
// Update these values after deploying the backend infrastructure

const CONFIG = {
  // API Gateway endpoints - update these after running deploy.sh
  API_INIT_ENDPOINT: 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/default/init',
  API_STATUS_ENDPOINT: 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/default/status',
  
  // Polling configuration
  POLL_INTERVAL_MS: 3000,
  MAX_POLLS: 60, // 3 minutes max
  
  // Environment
  ENVIRONMENT: 'dev'
};

// Export for use in scripts.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
