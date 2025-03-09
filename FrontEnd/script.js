// script.js
document.addEventListener('DOMContentLoaded', () => {
    const emailForm = document.getElementById('emailForm');
    const result = document.getElementById('result');
    const emailContent = document.getElementById('emailContent');
    const copyButton = document.getElementById('copyButton');
    const sendButton = document.getElementById('sendButton');
    const regenerateButton = document.getElementById('regenerateButton');

    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            recipient_name: document.getElementById('recipientName').value,
            recipient_email: document.getElementById('recipientEmail').value,
            context: document.getElementById('context').value,
            purpose: document.getElementById('purpose').value,
            tone: document.getElementById('tone').value
        };
    
        try {
            const API_URL = "http://127.0.0.1:8000";
            const response = await fetch(`${API_URL}/generate-email`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
    
            if (!response.ok) {
                const errorText = await response.text();  // Get error message
                throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
            }
    
            const responseData = await response.json();
            emailContent.innerHTML = `<p><strong>Generated Email:</strong></p>${responseData.email_content.replace(/\n/g, '<br>')}`;
            result.style.display = "block";  // Force show result
        } catch (error) {
            console.error('Error:', error);
            alert(`Failed to generate email. Reason: ${error.message}`);
        }
    });      

    copyButton.addEventListener('click', () => {
        const range = document.createRange();
        range.selectNode(emailContent);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        window.getSelection().removeAllRanges();
        alert('Email copied to clipboard!');
    });
    
    // Additional event handlers would go here
});