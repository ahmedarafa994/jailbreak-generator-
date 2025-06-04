// Simple copy button functionality fix
let currentJailbreakResult = null;

// Store result data for copying
function storeResultData(result) {
    currentJailbreakResult = result;
}

// Copy jailbreak text with proper error handling
function copyJailbreakText() {
    if (!currentJailbreakResult || !currentJailbreakResult.jailbreak) {
        alert('No jailbreak text available to copy');
        return;
    }
    
    const button = document.getElementById('copyJailbreakBtn');
    if (!button) {
        alert('Copy button not found');
        return;
    }
    
    const originalText = button.innerHTML;
    
    // Use modern clipboard API with fallback
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(currentJailbreakResult.jailbreak).then(() => {
            button.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-success');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-primary');
            }, 2000);
        }).catch(() => {
            fallbackCopy(currentJailbreakResult.jailbreak);
        });
    } else {
        fallbackCopy(currentJailbreakResult.jailbreak);
    }
}

// Fallback copy method for older browsers
function fallbackCopy(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        const button = document.getElementById('copyJailbreakBtn');
        if (button) {
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-success');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-primary');
            }, 2000);
        }
    } catch (err) {
        alert('Failed to copy to clipboard');
    }
    
    document.body.removeChild(textArea);
}