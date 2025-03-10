// script.js
document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript Loaded!");
    const sendButton = document.getElementById("sendButton");
    const regenerateButton = document.getElementById("regenerateButton");
    if (sendButton) 
        {
        sendButton.addEventListener("click", async () => {
            console.log("SendGrid button clicked!");  // ✅ Debugging Step
            alert(" feature is not implemented yet.");
            const recipientEmail = document.getElementById("recipientEmail").value;
            const senderEmail = document.getElementById("senderEmail").value;
            const fullContent = document.getElementById("emailContent").innerText.trim();
            
            if (!recipientEmail || !fullContent) {
                alert("Recipient email or content is missing!");
                return;
            }

            const sendData = {
                from_email: senderEmail,     // ✅ Match backend expected key
                to_email: recipientEmail,    // ✅ Match backend expected key
                subject: "AI-Generated Email",
                content: fullContent         // ✅ Match backend expected key
            };
    
            try {
                const API_URL = "http://127.0.0.1:8000";
                const response = await fetch(`${API_URL}/email/send-email`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(sendData),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                console.log("Email sent successfully!");
                alert("Email sent successfully!");
            } catch (error) {
                console.error("Error:", error);
                alert(`Failed to send email: ${error.message}`);
            }
        });
    } 
    else {
        console.log("Send button not found!");
    }

    regenerateButton.addEventListener("click", () => {
        console.log("Regenerate button clicked!");  // ✅ Debugging Step
        alert("Regenerate feature is not implemented yet.");
    });
    const emailForm = document.getElementById('emailForm');
    const result = document.getElementById('result');
    const emailContent = document.getElementById('emailContent');
    const copyButton = document.getElementById('copyButton');
    
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
});
// document.addEventListener('DOMContentLoaded', () => {
//     console.log("JavaScript Loaded!");
        
    // regenerateButton.addEventListener('click', async () => {
    //     // Resubmit the form to generate a new email
    //     emailForm.dispatchEvent(new Event('submit'));
    // });
    
    
    // sendButton.addEventListener("click", async () => {
    //     console.log("SendGrid button clicked!");  // ✅ Debugging step
    
    //     const recipientEmail = document.getElementById("recipientEmail").value;
    //     const senderEmail = document.getElementById("senderEmail").value;
        
    //     const fullContent = emailContent.innerText || emailContent.textContent;
    //     const emailText = fullContent.replace(/Generated Email:\s*/i, "").trim();
        
    //     const purpose = document.getElementById("purpose").value;
    //     const subject = `${purpose.charAt(0).toUpperCase() + purpose.slice(1)} Email`;
        
    //     const sendData = {
    //         email_content: emailText,
    //         recipient_email: recipientEmail,
    //         sender_email: senderEmail,
    //         subject: subject
    //     };
        
    //     console.log("Sending data:", sendData);  // ✅ Debugging step
        
    //     try {
    //         const API_URL = "http://127.0.0.1:8000";
    //         const response = await fetch(`${API_URL}/email/send-email`, {
    //             method: "POST",
    //             headers: { "Content-Type": "application/json" },
    //             body: JSON.stringify(sendData),
    //         });
    
    //         if (!response.ok) {
    //             const errorText = await response.text();
    //             throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
    //         }
    
    //         const responseData = await response.json();
    //         alert("Email sent successfully!");
    //     } catch (error) {
    //         console.error("Error:", error);
    //         alert(`Failed to send email. Reason: ${error.message}`);
    //     }
    // });    
    // Additional event handlers would go here
// });