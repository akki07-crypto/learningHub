document.addEventListener('DOMContentLoaded', function () {
    const chatbotFab = document.getElementById('chatbotFab');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const closeChatbot = document.getElementById('closeChatbot');
    const chatInput = document.getElementById('chatInput');
    const sendChatBtn = document.getElementById('sendChatBtn');
    const chatMessages = document.getElementById('chatMessages');
    const chipBtns = document.querySelectorAll('.chip-btn');

    if (!chatbotFab || !chatbotWindow) return;

    // Toggle Chatbot Window
    chatbotFab.addEventListener('click', function () {
        chatbotWindow.classList.toggle('active');
        if (chatbotWindow.classList.contains('active')) {
            chatInput.focus();
        }
    });

    if (closeChatbot) {
        closeChatbot.addEventListener('click', function () {
            chatbotWindow.classList.remove('active');
        });
    }

    // Markdown Parser Helper
    function parseMarkdown(text) {
        if (!text) return '';
        let html = text;
        // Replace bold **text** with <strong>text</strong>
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Replace italic *text* with <em>text</em>
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        // Replace newlines with <br>
        html = html.replace(/\n/g, '<br>');
        return html;
    }

    // Send Message Logic
    function sendMessage(customMsg) {
        const message = (typeof customMsg === 'string' ? customMsg : chatInput.value).trim();
        if (!message) return;

        // Append User Message Bubble
        const userBubble = document.createElement('div');
        userBubble.className = 'chat-bubble user';
        userBubble.textContent = message;
        chatMessages.appendChild(userBubble);

        chatInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Append Loading Bot Bubble
        const botLoadingBubble = document.createElement('div');
        botLoadingBubble.className = 'chat-bubble bot';
        botLoadingBubble.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Gemini AI is thinking...';
        chatMessages.appendChild(botLoadingBubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Send API Request
        fetch('/api/ai-chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(res => res.json())
        .then(data => {
            const parsedReply = parseMarkdown(data.reply || 'Sorry, I did not catch that.');
            botLoadingBubble.innerHTML = parsedReply;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(err => {
            botLoadingBubble.innerHTML = '🤖 Connection error. Please try asking again!';
            console.error(err);
        });
    }

    // Quick Chips Click Event
    chipBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const question = this.getAttribute('data-question');
            if (question) {
                sendMessage(question);
            }
        });
    });

    if (sendChatBtn) {
        sendChatBtn.addEventListener('click', function() { sendMessage(); });
    }

    if (chatInput) {
        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});
