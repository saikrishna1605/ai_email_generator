document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript Loaded!");

    const sendButton = document.getElementById("sendButton");
    const regenerateButton = document.getElementById("regenerateButton");
    const emailForm = document.getElementById("emailForm");
    const result = document.getElementById("result");
    const emailContent = document.getElementById("emailContent");
    const copyButton = document.getElementById("copyButton");

    if (sendButton) {
        sendButton.addEventListener("click", async () => {
            console.log("SendGrid button clicked!");

            const recipientEmail = document.getElementById("recipientEmail").value;
            const senderEmail = document.getElementById("senderEmail").value;
            const fullContent = emailContent.innerText.trim();

            if (!recipientEmail || !fullContent) {
                alert("Recipient email or content is missing!");
                return;
            }

            const sendData = {
                from_email: senderEmail,
                to_email: recipientEmail,
                subject: "AI-Generated Email",
                content: fullContent
            };

            try {
                const API_URL = "http://127.0.0.1:8001";
                const response = await fetch(`${API_URL}/email/send-email`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(sendData),
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
                }

                console.log("Email sent successfully!");
                alert("Email sent successfully!");
            } catch (error) {
                console.error("Error:", error);
                alert(`Failed to send email: ${error.message}`);
            }
        });
    } else {
        console.log("Send button not found!");
    }

    if (regenerateButton) {
        regenerateButton.addEventListener("click", () => {
            emailForm.dispatchEvent(new Event("submit"));
        });
    } else {
        console.log("Regenerate button not found!");
    }

    emailForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("recipient_name", document.getElementById("recipientName").value);
        formData.append("recipient_email", document.getElementById("recipientEmail").value);
        formData.append("context", document.getElementById("context").value);
        formData.append("purpose", document.getElementById("purpose").value);
        formData.append("tone", document.getElementById("tone").value);

        const fileInput = document.getElementById("attachments");
        for (let i = 0; i < fileInput.files.length; i++) {
            formData.append("files", fileInput.files[i]);
        }

        try {
            const API_URL = "http://127.0.0.1:8001";
            const response = await fetch(`${API_URL}/generate-email`, {
                method: "POST",
                body: formData, // No need to set Content-Type manually
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
            }

            const responseData = await response.json();
            emailContent.innerHTML = `<p><strong>Generated Email:</strong></p>${responseData.email_content.replace(/\n/g, "<br>")}`;
            result.style.display = "block";
        } catch (error) {
            console.error("Error:", error);
            alert(`Failed to generate email. Reason: ${error.message}`);
        }
    });

    if (copyButton) {
        copyButton.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(emailContent.innerText.trim());
                alert("Email copied to clipboard!");
            } catch (error) {
                console.error("Clipboard Copy Failed:", error);
                alert("Failed to copy text. Try manually copying.");
            }
        });
    } else {
        console.log("Copy button not found!");
    }
});
