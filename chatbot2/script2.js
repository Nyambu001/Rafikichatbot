//simple chatbot
function chatbot(input) {
    let output = "Hello";
    return output;
}

// send user message and get bot response
function sendMessage() {
    let input = document.getElementById("input").value;
    if (input) {
        displayUserMessage(input); // Display user message in chat
        let output = chatbot(input);
        setTimeout(function() {
            displayBotMessage(output);
        }, 1000);
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
let chatHistory = {};

function saveToHistory() {
    const chatContent = document.getElementById("chat").innerHTML;
    if (chatContent.trim() !== '') {
        const conversationKey = `Conversation ${Object.keys(chatHistory).length + 1}`;
        chatHistory[conversationKey] = chatContent; // Store chat content in the object

        // Save the entire chat history to local storage
        localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
        
        const historyItem = document.createElement("li");
        historyItem.textContent = conversationKey;
        historyItem.addEventListener("click", () => {
            document.getElementById("chat").innerHTML = chatHistory[historyItem.textContent];
        });
        historyList.appendChild(historyItem);
    }
}

function loadHistoryFromLocalStorage() {
    const storedHistory = localStorage.getItem("chatHistory");
    if (storedHistory) {
        chatHistory = JSON.parse(storedHistory);

        // Populate the history list
        Object.keys(chatHistory).forEach(key => {
            const historyItem = document.createElement("li");
            historyItem.textContent = key;
            historyItem.addEventListener("click", () => {
                document.getElementById("chat").innerHTML = chatHistory[key];
            });
            historyList.appendChild(historyItem);
        });
    }
}

// Call this function when the page loads
loadHistoryFromLocalStorage();

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