chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "SHOW_WARNING") {
        showWarningBanner(request.data);  // Now passing the full API response data
    } else if (request.action === "HIDE_WARNING") {
        hideWarningBanner();
    }
});

function showWarningBanner(data) {
    // Prevent multiple banners
    hideWarningBanner();

    const banner = document.createElement('div');
    banner.id = 'phish-guard-warning';
    banner.style.position = 'fixed';
    banner.style.top = '0';
    banner.style.left = '0';
    banner.style.width = '100%';
    banner.style.backgroundColor = '#FF3B30';
    banner.style.color = 'white';
    banner.style.textAlign = 'center';
    banner.style.padding = '15px';
    banner.style.fontSize = '18px';
    banner.style.fontWeight = 'bold';
    banner.style.zIndex = '999999';
    banner.style.boxShadow = '0 4px 10px rgba(0,0,0,0.3)';
    banner.style.transition = 'opacity 0.3s';

    // Use actual result and confidence from API
    const phishingPercent = data.phishing_score ? (data.phishing_score * 100).toFixed(1) : 'High';
    const confidencePercent = data.confidence ? (data.confidence * 100).toFixed(1) : '';

    banner.innerHTML = `
        ⚠️ PHISHING SITE DETECTED ⚠️<br>
        <span style="font-size: 15px; font-weight: normal;">
            Our AI model is ${confidencePercent}% confident this is a phishing attempt.<br>
            Phishing likelihood: <strong>${phishingPercent}%</strong> • URL: ${escapeHtml(data.url || 'unknown')}
        </span>
        <button id="phish-guard-close" style="margin-left: 20px; padding: 6px 12px; background: white; color: #FF3B30; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">
            I Understand, Dismiss
        </button>
    `;

    document.body.prepend(banner);

    // Close button
    document.getElementById('phish-guard-close').addEventListener('click', () => {
        banner.style.opacity = '0';
        setTimeout(() => banner.remove(), 300);
    });
}

function hideWarningBanner() {
    const existing = document.getElementById('phish-guard-warning');
    if (existing) {
        existing.remove();
    }
}

// Simple HTML escape to prevent XSS if URL has weird chars
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}