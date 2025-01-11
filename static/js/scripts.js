document.getElementById("send-btn").addEventListener("click", function() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    // Display user message
    appendMessage(userInput, "user");

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send message to backend
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        appendMessage(data.reply, "bot");
    })
    .catch(err => console.error("Error:", err));
});

function appendMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

    // Remove any URLs from the message (just like before)
    message = message.replace(/http[^ ]+/g, '');  // This removes any URLs from the text

    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
