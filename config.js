// API Configuration
// Update these values after deploying the backend infrastructure

const CONFIG = {
  // API Gateway endpoints - update these after running deploy.sh
  API_INIT_ENDPOINT: 'https://2gotexgdyd.execute-api.us-east-1.amazonaws.com/default/aBoxOfMacAndCheeseInit',
  API_STATUS_ENDPOINT: 'https://mcvwsqrip4.execute-api.us-east-1.amazonaws.com/default/aBoxOfMacAndCheeseStatus',
  
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
