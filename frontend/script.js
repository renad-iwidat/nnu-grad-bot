const API_URL = 'https://nnu-grad-bot.onrender.com';
let currentTheme = 'light';
let sessionId = null;

const elements = {
    chatForm: document.getElementById('chatForm'),
    userInput: document.getElementById('userInput'),
    sendBtn: document.getElementById('sendBtn'),
    messages: document.getElementById('messages'),
    loading: document.getElementById('loading'),
    welcomeMessage: document.getElementById('welcomeMessage'),
    themeToggle: document.getElementById('themeToggle')
};

function initializeApp() {
    elements.chatForm.addEventListener('submit', handleSubmit);
    elements.themeToggle.addEventListener('click', toggleTheme);
    
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.getAttribute('data-question');
            elements.userInput.value = question;
            handleSubmit(new Event('submit'));
        });
    });
    
    elements.userInput.addEventListener('input', autoResize);
    elements.userInput.addEventListener('keydown', handleKeyDown);
    
    sessionId = generateSessionId();
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit(new Event('submit'));
    }
}

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substring(2, 11);
}

function autoResize() {
    elements.userInput.style.height = 'auto';
    elements.userInput.style.height = elements.userInput.scrollHeight + 'px';
}

async function handleSubmit(e) {
    e.preventDefault();
    
    const question = elements.userInput.value.trim();
    if (!question) return;
    
    elements.welcomeMessage.style.display = 'none';
    
    addMessage(question, 'user');
    elements.userInput.value = '';
    elements.userInput.style.height = 'auto';
    elements.sendBtn.disabled = true;
    elements.loading.style.display = 'block';
    
    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                session_id: sessionId,
                include_context: false
            })
        });
        
        if (!response.ok) {
            if (response.status === 500) {
                throw new Error('حدث خطأ في الخادم. يرجى المحاولة مرة أخرى.');
            } else if (response.status === 404) {
                throw new Error('الخدمة غير متوفرة حالياً.');
            } else {
                throw new Error('حدث خطأ في الاتصال.');
            }
        }
        
        const data = await response.json();
        addMessage(data.answer, 'assistant', data.sources);
        
    } catch (error) {
        console.error('Error:', error);
        
        let errorMessage = 'عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.';
        
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMessage = 'تعذر الاتصال بالخادم. يرجى التأكد من أن الخادم يعمل والمحاولة مرة أخرى.';
        } else if (error.message) {
            errorMessage = error.message;
        }
        
        addMessage(errorMessage, 'assistant');
    } finally {
        elements.loading.style.display = 'none';
        elements.sendBtn.disabled = false;
        elements.userInput.focus();
    }
}

function formatAnswer(text) {
    let formatted = text;
    
    // Clean up unwanted markers
    formatted = formatted.replace(/\[Source \d+\]/g, '');
    formatted = formatted.replace(/\[.*?\]/g, '');
    formatted = formatted.replace(/\s+\./g, '.');
    formatted = formatted.replace(/\s+,/g, ',');
    formatted = formatted.replace(/\.\s*\./g, '.');
    
    // Convert markdown headings to HTML
    formatted = formatted.replace(/###\s*(.+?)(\n|$)/g, '<h4 class="answer-subheading">$1</h4>\n');
    formatted = formatted.replace(/##\s*(.+?)(\n|$)/g, '<h3 class="answer-heading">$1</h3>\n');
    
    // Convert bold text
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    const lines = formatted.split('\n');
    let result = '';
    let inNumberedList = false;
    let inBulletList = false;
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        
        // Skip empty lines but add spacing
        if (!line) {
            if (inNumberedList) {
                result += '</div>';
                inNumberedList = false;
            }
            if (inBulletList) {
                result += '</div>';
                inBulletList = false;
            }
            if (result && !result.endsWith('</h3>') && !result.endsWith('</h4>')) {
                result += '<div class="paragraph-break"></div>';
            }
            continue;
        }
        
        // Handle HTML headings (already converted)
        if (line.startsWith('<h3') || line.startsWith('<h4')) {
            if (inNumberedList) {
                result += '</div>';
                inNumberedList = false;
            }
            if (inBulletList) {
                result += '</div>';
                inBulletList = false;
            }
            result += line;
            continue;
        }
        
        // Handle numbered lists (1. 2. 3.)
        const numberedMatch = line.match(/^(\d+)\.\s+(.+)/);
        if (numberedMatch) {
            if (inBulletList) {
                result += '</div>';
                inBulletList = false;
            }
            if (!inNumberedList) {
                result += '<div class="list-container">';
                inNumberedList = true;
            }
            result += `<div class="numbered-item"><span class="number">${numberedMatch[1]}.</span><span class="item-text">${numberedMatch[2]}</span></div>`;
            continue;
        }
        
        // Handle bullet lists (- or •)
        const bulletMatch = line.match(/^[\-•]\s+(.+)/);
        if (bulletMatch) {
            if (inNumberedList) {
                result += '</div>';
                inNumberedList = false;
            }
            if (!inBulletList) {
                result += '<div class="list-container">';
                inBulletList = true;
            }
            result += `<div class="bullet-item"><span class="bullet">•</span><span class="item-text">${bulletMatch[1]}</span></div>`;
            continue;
        }
        
        // Close any open lists before regular paragraphs
        if (inNumberedList) {
            result += '</div>';
            inNumberedList = false;
        }
        if (inBulletList) {
            result += '</div>';
            inBulletList = false;
        }
        
        // Regular paragraph
        result += `<p>${line}</p>`;
    }
    
    // Close any remaining open lists
    if (inNumberedList) {
        result += '</div>';
    }
    if (inBulletList) {
        result += '</div>';
    }
    
    return result;
}

function addMessage(content, type, sources = []) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'user' ? '👤' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (type === 'assistant') {
        let cleanContent = content;
        cleanContent = cleanContent.replace(/\[Source \d+\]/g, '');
        cleanContent = cleanContent.replace(/المصدر:.*$/gm, '');
        cleanContent = cleanContent.replace(/المصادر:.*$/gm, '');
        cleanContent = cleanContent.replace(/\(المصدر.*?\)/g, '');
        cleanContent = cleanContent.trim();
        contentDiv.innerHTML = formatAnswer(cleanContent);
    } else {
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    elements.messages.appendChild(messageDiv);
    
    if (sources && sources.length > 0 && type === 'assistant') {
        const uniqueSources = [];
        const seenTitles = new Set();
        
        for (const source of sources) {
            if (!seenTitles.has(source.title)) {
                seenTitles.add(source.title);
                uniqueSources.push(source);
            }
        }
        
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources-container';
        
        const sourcesTitle = document.createElement('div');
        sourcesTitle.className = 'sources-title';
        sourcesTitle.innerHTML = '<span class="sources-icon">📚</span>المصادر';
        sourcesDiv.appendChild(sourcesTitle);
        
        const sourcesList = document.createElement('div');
        sourcesList.className = 'sources-list';
        
        uniqueSources.forEach((source, index) => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            
            const sourceNumber = document.createElement('span');
            sourceNumber.className = 'source-number';
            sourceNumber.textContent = index + 1;
            
            const sourceContent = document.createElement('div');
            sourceContent.className = 'source-content';
            
            if (source.url) {
                const link = document.createElement('a');
                link.href = source.url;
                link.target = '_blank';
                link.className = 'source-link';
                link.textContent = source.title;
                sourceContent.appendChild(link);
            } else {
                sourceContent.textContent = source.title;
            }
            
            sourceItem.appendChild(sourceNumber);
            sourceItem.appendChild(sourceContent);
            sourcesList.appendChild(sourceItem);
        });
        
        sourcesDiv.appendChild(sourcesList);
        elements.messages.appendChild(sourcesDiv);
    }
    
    setTimeout(() => {
        const lastMessage = elements.messages.lastElementChild;
        if (lastMessage) {
            lastMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }, 150);
}

function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.body.className = `${currentTheme}-mode`;
    
    const icon = elements.themeToggle.querySelector('.theme-icon');
    icon.textContent = currentTheme === 'light' ? '🌙' : '☀️';
}

initializeApp();
