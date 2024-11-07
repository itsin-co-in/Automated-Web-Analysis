import lighthouse from 'lighthouse';
import chromeLauncher from 'chrome-launcher';

// const lighthouse = require('lighthouse');
// const chromeLauncher = require('chrome-launcher');

async function runLighthouse(url) {
  try {

    const lighthouse = await import('lighthouse');
    const chromeLauncher = await import('chrome-launcher');

    const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
    const options = { port: chrome.port };
    const runnerResult = await lighthouse(url, options);

    // Extract the Lighthouse metrics
    const { categories } = runnerResult.lhr;
    const metrics = {
      performanceScore: categories.performance.score,
      accessibilityScore: categories.accessibility.score,
      bestPracticesScore: categories['best-practices'].score,
      seoScore: categories.seo.score,
      progressiveWebAppScore: categories.pwa.score
    };

    await chrome.kill();
    return metrics;
  } catch (err) {
    console.error('Lighthouse error:', err);
    throw err;
  }
}

async function main() {
  const url = 'https://www.rayatt.com.au';
  const metrics = await runLighthouse(url);
  console.log('Lighthouse metrics:', metrics);
}

main();