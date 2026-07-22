// Main Application Logic (Theme Toggle, Notifications, Referral Copy)

document.addEventListener('DOMContentLoaded', () => {
    // Theme Switcher Logic
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const currentTheme = localStorage.getItem('theme') || 'dark';
    
    if (currentTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        if (themeToggleBtn) themeToggleBtn.innerHTML = '🌙';
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (themeToggleBtn) themeToggleBtn.innerHTML = '☀️';
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let activeTheme = document.documentElement.getAttribute('data-theme');
            if (activeTheme === 'light') {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeToggleBtn.innerHTML = '☀️';
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                themeToggleBtn.innerHTML = '🌙';
            }
        });
    }

    // Referral Code Copy Button
    const copyRefBtn = document.getElementById('copyRefBtn');
    if (copyRefBtn) {
        copyRefBtn.addEventListener('click', () => {
            const refInput = document.getElementById('refLinkInput');
            if (refInput) {
                refInput.select();
                navigator.clipboard.writeText(refInput.value);
                copyRefBtn.innerText = 'Copied! 🎉';
                setTimeout(() => { copyRefBtn.innerText = 'Copy Link'; }, 2000);
            }
        });
    }
});

// Upvote post AJAX handler
function upvotePost(postId) {
    fetch(`/forum/${postId}/upvote/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        const countSpan = document.getElementById(`upvote-count-${postId}`);
        if (countSpan) {
            countSpan.innerText = data.count;
        }
    })
    .catch(err => console.error(err));
}

// CSRF Cookie Helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
