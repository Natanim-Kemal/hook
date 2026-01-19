// popup.js - Updated & Fixed Version

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('checkBtn').addEventListener('click', rescanCurrentTab);
  loadCurrentTabResult(); // Load on open
});

// Load result (from cache or trigger scan via background)
async function loadCurrentTabResult() {
  const statusDiv = document.getElementById('status');
  const urlDiv = document.getElementById('url');
  const detailsDiv = document.getElementById('details');

  statusDiv.textContent = "Loading...";
  statusDiv.className = "status-text checking";
  detailsDiv.textContent = "--";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url) {
    statusDiv.textContent = "No URL";
    return;
  }

  urlDiv.textContent = tab.url;

  // First, try to get cached result (same as background uses)
  const cacheKey = `scan_${tab.url}`;
  const cached = await chrome.storage.local.get(cacheKey);

  if (cached[cacheKey] && Date.now() - cached[cacheKey].timestamp < 24*60*60*1000) {
    displayResult(cached[cacheKey].payload);
    return;
  }

  // No cache → ask background to scan (respects whitelist, cache, etc.)
  statusDiv.textContent = "Scanning...";
  chrome.runtime.sendMessage({ action: "SCAN_CURRENT_TAB" });
}

// Listen for updates from background script
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "UPDATE_DETAILS" && message.data) {
    displayResult(message.data);
  }
});

function displayResult(data) {
  const statusDiv = document.getElementById('status');
  const detailsDiv = document.getElementById('details');

  statusDiv.classList.remove('checking');

  if (data.error) {
    statusDiv.textContent = "Error";
    statusDiv.style.color = "#FF3B30";
    detailsDiv.textContent = "Server error";
    return;
  }

  const isPhishing = data.result.toUpperCase() === "PHISHING";

  if (isPhishing) {
    statusDiv.textContent = "Phishing";
    statusDiv.className = "status-text phishing";
  } else {
    statusDiv.textContent = "Safe";
    statusDiv.className = "status-text safe";
  }

  // Show confidence (how sure the model is)
  const confidencePercent = data.confidence ? (data.confidence * 100).toFixed(1) : "--";
  detailsDiv.textContent = `${confidencePercent}% confident`;
}

function rescanCurrentTab() {
  chrome.runtime.sendMessage({ action: "SCAN_CURRENT_TAB" });
}