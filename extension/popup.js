document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('checkBtn').addEventListener('click', rescanCurrentTab);
  loadCurrentTabResult();
});

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

  const cacheKey = `scan_${tab.url}`;
  const cached = await chrome.storage.local.get(cacheKey);

  if (cached[cacheKey] && Date.now() - cached[cacheKey].timestamp < 24 * 60 * 60 * 1000) {
    displayResult(cached[cacheKey].payload);
    return;
  }

  statusDiv.textContent = "Scanning...";
  chrome.runtime.sendMessage({ action: "SCAN_CURRENT_TAB" });
}

chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "UPDATE_DETAILS" && message.data) {
    displayResult(message.data);
  }
});

function displayResult(data) {
  console.log('displayResult called with data:', data); // Debug log
  
  const statusDiv = document.getElementById('status');
  const detailsDiv = document.getElementById('details');
  const explanationsCard = document.getElementById('explanations-card');
  const explanationsDiv = document.getElementById('explanations');

  statusDiv.classList.remove('checking');

  if (data.error) {
    statusDiv.textContent = "Error";
    statusDiv.style.color = "#FF3B30";
    detailsDiv.textContent = "Server error";
    explanationsCard.style.display = "none";
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

  // Show confidence - use either confidence or probability
  const confidence = data.confidence || data.probability || 0;
  console.log('Confidence value:', confidence, 'from data.confidence:', data.confidence, 'data.probability:', data.probability); // Debug log
  const confidencePercent = (confidence * 100).toFixed(1);
  detailsDiv.textContent = `${confidencePercent}% confident`;

  // Show explanations for phishing sites
  if (isPhishing && data.explanations && data.explanations.length > 0) {
    explanationsCard.style.display = "block";
    const explanationsList = data.explanations.map(exp => `<li>${exp}</li>`).join('');
    explanationsDiv.innerHTML = `<ul>${explanationsList}</ul>`;
  } else {
    explanationsCard.style.display = "none";
  }
}

function rescanCurrentTab() {
  chrome.runtime.sendMessage({ action: "SCAN_CURRENT_TAB" });
}