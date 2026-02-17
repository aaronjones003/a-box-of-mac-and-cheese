let interval = null;
let currentImageUrl = null;
let pollCount = 0;
const MAX_POLLS = 60; // 3 minutes max (60 * 3 seconds)

let statusEl, imageEl, generateBtn, downloadBtn;

function setStatus(message) {
    statusEl.textContent = message;
    statusEl.style.display = 'block';
}

function showImage(src) {
    currentImageUrl = src;
    imageEl.src = src;
    imageEl.style.display = 'block';
    statusEl.style.display = 'none';
    downloadBtn.disabled = false;
}

function hideImage() {
    imageEl.style.display = 'none';
    downloadBtn.disabled = true;
}

function setButtonLoading() {
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner"></span><span>Generating...</span>';
}

function setButtonFinished() {
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<span>✨</span><span>Generate</span>';
}

function setButtonError() {
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<span>🔄</span><span>Try Again</span>';
}

async function generate() {
    try {
        hideImage();
        setButtonLoading();
        setStatus('Initializing generation...');
        pollCount = 0;

        const initResponse = await fetch('https://2gotexgdyd.execute-api.us-east-1.amazonaws.com/default/aBoxOfMacAndCheeseInit');
        
        if (!initResponse.ok) {
            throw new Error(`Failed to initialize: ${initResponse.status}`);
        }

        const initData = await initResponse.json();
        console.log('Init response:', initData);

        if (!initData.executionArn) {
            throw new Error('No execution ARN received');
        }

        setStatus('Creating your masterpiece... This may take 30-60 seconds.');

        clearInterval(interval);
        interval = setInterval(async () => {
            try {
                pollCount++;

                if (pollCount > MAX_POLLS) {
                    clearInterval(interval);
                    setStatus('Generation timed out. Please try again.');
                    setButtonError();
                    return;
                }

                const statusResponse = await fetch(
                    "https://mcvwsqrip4.execute-api.us-east-1.amazonaws.com/default/aBoxOfMacAndCheeseStatus",
                    {
                        method: "POST",
                        body: JSON.stringify({
                            arn: initData.executionArn
                        })
                    }
                );

                if (!statusResponse.ok) {
                    throw new Error(`Status check failed: ${statusResponse.status}`);
                }

                const statusData = await statusResponse.json();
                console.log('Status response:', statusData);

                const elapsed = Math.floor(pollCount * 3);
                setStatus(`Generating... (${elapsed}s elapsed)`);

                if (statusData.status === 'SUCCEEDED') {
                    clearInterval(interval);
                    
                    const output = JSON.parse(statusData.output);
                    const imageUrl = output.body.output.replaceAll('+', '%2B');
                    
                    showImage(imageUrl);
                    setButtonFinished();
                    setStatus('');
                    
                } else if (statusData.status === 'FAILED' || statusData.status === 'TIMED_OUT' || statusData.status === 'ABORTED') {
                    clearInterval(interval);
                    setStatus(`Generation failed: ${statusData.status}. Please try again.`);
                    setButtonError();
                }

            } catch (pollError) {
                console.error('Polling error:', pollError);
                clearInterval(interval);
                setStatus('Error checking status. Please try again.');
                setButtonError();
            }
        }, 3000);

    } catch (error) {
        console.error('Generation error:', error);
        clearInterval(interval);
        setStatus(`Error: ${error.message}. Please try again.`);
        setButtonError();
    }
}

function downloadImage() {
    if (!currentImageUrl) return;

    const link = document.createElement('a');
    link.href = currentImageUrl;
    link.download = `mac-and-cheese-${Date.now()}.png`;
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function init() {
    statusEl = document.getElementById('status');
    imageEl = document.getElementById('image');
    generateBtn = document.getElementById('generate-btn');
    downloadBtn = document.getElementById('download-btn');

    if (!statusEl || !imageEl || !generateBtn || !downloadBtn) {
        console.error('Required DOM elements not found');
        return;
    }

    generateBtn.addEventListener('click', generate);
    downloadBtn.addEventListener('click', downloadImage);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}