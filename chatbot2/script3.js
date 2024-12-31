function sendMessage() {
    const input = document.getElementById("input").value.trim();
    if (input) {
        displayUserMessage(input); // Display user message in chat

        fetch("/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `message=${encodeURIComponent(input)}`,
        })
        .then(response => response.json())
        .then(data => {
            displayBotMessage(data.response);
            saveToHistory(); // Save chat after a bot response
        })
        .catch(error => {
            console.error("Error:", error);
            displayBotMessage("Error communicating with chatbot.");
        });

        document.getElementById("input").value = "";
    }
}

// Display user message on the chat
function displayUserMessage(message){ 
    let chat=document.getElementById("chat");
    let userMessage=document.createElement("div");
    userMessage.classList.add("message");
    userMessage.classList.add("user");
    let userAvatar=document.createElement("div");
    userAvatar.classList.add("avatar");
    let userText=document.createElement("div");
    userText.classList.add("text");
    userText.innerHTML = message;
    userMessage.appendChild(userAvatar);
    userMessage.appendChild(userText);
    chat.appendChild(userMessage);
    chat.scrollTop = chat.scrollHeight;
}

// Display bot message on the chat
function displayBotMessage(message){
    let chat=document.getElementById("chat");
    let botMessage=document.createElement("div");
    botMessage.classList.add("message");
    botMessage.classList.add("bot");
    let botText=document.createElement("div");
    botText.classList.add("text");
    botText.innerHTML = message;
    let botAvatar=document.createElement("div");
    botAvatar.classList.add("avatar");
    botMessage.appendChild(botAvatar);
    botMessage.appendChild(botText);
    chat.appendChild(botMessage);
    chat.scrollTop = chat.scrollHeight;
}

const historyList = document.getElementById('history-list');
let chatHistory = [];

// Save conversation to history and update history list
function saveToHistory() {
    const chatContent = document.getElementById("chat").innerHTML;
    if (chatContent.trim() !== '') {
        const conversationId = `conv_${new Date().getTime()}`; // Unique ID for each conversation

        // Save chat history to the Django API
        fetch("/save_history/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                chat_content: chatContent,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Chat history saved:", data.message);

            // Add conversation to the frontend history list
            const historyItem = document.createElement("li");
            historyItem.textContent = `Conversation ${conversationId}`;
            historyItem.addEventListener("click", () => loadChatHistory(conversationId));
            document.getElementById("history-list").appendChild(historyItem);
        })
        .catch(error => {
            console.error("Error saving chat history:", error);
        });
    }
}

// Function to retrieve and display chat history from the Django API
function loadChatHistory(conversationId) {
    fetch(`/get_history/${conversationId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.chat_content) {
                document.getElementById("chat").innerHTML = data.chat_content;
            } else {
                console.error("No chat history found for this conversation.");
            }
        })
        .catch(error => {
            console.error("Error retrieving chat history:", error);
        });
}

//scroll the chat
document.addEventListener("keydown", function (event) {
    const chat = document.getElementById("chat");
    if (event.key === "ArrowUp") {
        chat.scrollBy({ top: -30, behavior: "smooth" });
        event.preventDefault();
    } else if (event.key === "ArrowDown") {
        chat.scrollBy({ top: 30, behavior: "smooth" });
        event.preventDefault();
    }
});

//add a click event listener to the button
document.getElementById("button").addEventListener("click", sendMessage);

//add a keypress event listener to the input
document.getElementById("input").addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // Prevent adding a new line
        sendMessage();
    }
})
//define infputField
const inputField = document.getElementById("input");
//new line in input
inputField.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && event.shiftKey) {
        let cursorPos = inputField.selectionStart;
        inputField.value = inputField.value.substring(0, cursorPos) + "\n" + inputField.value.substring(cursorPos);
        event.preventDefault();
    }
});

 // Save conversation to history when window is closed
 window.addEventListener('beforeunload', saveToHistory);