const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8766;

// Simple static file server
function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let filePath = '.' + (req.url === '/' ? '/index.html' : req.url);
      const extname = path.extname(filePath);
      const contentType = {
        '.html': 'text/html',
        '.js': 'text/javascript',
        '.css': 'text/css',
      }[extname] || 'text/plain';

      fs.readFile(filePath, (error, content) => {
        if (error) {
          res.writeHead(404);
          res.end('File not found');
        } else {
          res.writeHead(200, { 'Content-Type': contentType });
          res.end(content, 'utf-8');
        }
      });
    });

    server.listen(PORT, () => {
      console.log(`Test server running at http://localhost:${PORT}/`);
      resolve(server);
    });
  });
}

async function runTests() {
  let server;
  let browser;
  let passed = 0;
  let failed = 0;

  try {
    console.log('🚀 Starting Box of Mac and Cheese Tests\n');
    
    server = await startServer();
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // Listen for console errors
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await page.goto(`http://localhost:${PORT}/`);
    await page.waitForTimeout(1000);

    // Test 1: DOM elements exist
    try {
      const statusEl = await page.$('#status');
      const imageEl = await page.$('#image');
      const generateBtn = await page.$('#generate-btn');
      const downloadBtn = await page.$('#download-btn');

      if (!statusEl || !imageEl || !generateBtn || !downloadBtn) {
        throw new Error('Missing DOM elements');
      }
      console.log('✅ Test 1: All DOM elements exist');
      passed++;
    } catch (e) {
      console.log('❌ Test 1: DOM elements check failed -', e.message);
      failed++;
    }

    // Test 2: Generate button is enabled
    try {
      const isDisabled = await page.$eval('#generate-btn', el => el.disabled);
      if (isDisabled) throw new Error('Generate button should not be disabled');
      console.log('✅ Test 2: Generate button is enabled');
      passed++;
    } catch (e) {
      console.log('❌ Test 2: Generate button state failed -', e.message);
      failed++;
    }

    // Test 3: Download button is disabled initially
    try {
      const isDisabled = await page.$eval('#download-btn', el => el.disabled);
      if (!isDisabled) throw new Error('Download button should be disabled initially');
      console.log('✅ Test 3: Download button is disabled initially');
      passed++;
    } catch (e) {
      console.log('❌ Test 3: Download button state failed -', e.message);
      failed++;
    }

    // Test 4: Status element has text
    try {
      const statusText = await page.$eval('#status', el => el.textContent);
      if (!statusText || statusText.length === 0) {
        throw new Error('Status should have text content');
      }
      console.log('✅ Test 4: Status element has text');
      passed++;
    } catch (e) {
      console.log('❌ Test 4: Status text check failed -', e.message);
      failed++;
    }

    // Test 5: Image is hidden initially
    try {
      const isVisible = await page.$eval('#image', el => {
        return window.getComputedStyle(el).display !== 'none';
      });
      if (isVisible) throw new Error('Image should be hidden initially');
      console.log('✅ Test 5: Image is hidden initially');
      passed++;
    } catch (e) {
      console.log('❌ Test 5: Image visibility check failed -', e.message);
      failed++;
    }

    // Test 6: No JavaScript errors
    try {
      if (errors.length > 0) {
        throw new Error(`JavaScript errors detected: ${errors.join(', ')}`);
      }
      console.log('✅ Test 6: No JavaScript errors');
      passed++;
    } catch (e) {
      console.log('❌ Test 6: JavaScript error check failed -', e.message);
      failed++;
    }

    console.log(`\n📊 Summary: ${passed} passed, ${failed} failed`);
    
    if (failed > 0) {
      process.exit(1);
    }

  } catch (error) {
    console.error('Test suite error:', error);
    process.exit(1);
  } finally {
    if (browser) await browser.close();
    if (server) server.close();
  }
}

runTests();
