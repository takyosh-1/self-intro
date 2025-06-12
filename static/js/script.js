document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('nameInput');
    const generateBtn = document.getElementById('generateBtn');
    const outputArea = document.getElementById('outputArea');
    const loading = document.getElementById('loading');
    
    let isGenerating = false;
    
    generateBtn.addEventListener('click', generateIntroduction);
    nameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !isGenerating) {
            generateIntroduction();
        }
    });
    
    function generateIntroduction() {
        const name = nameInput.value.trim();
        
        if (!name) {
            alert('名前を入力してください');
            nameInput.focus();
            return;
        }
        
        if (isGenerating) {
            return;
        }
        
        isGenerating = true;
        generateBtn.disabled = true;
        generateBtn.textContent = '生成中...';
        loading.style.display = 'flex';
        
        outputArea.innerHTML = '';
        outputArea.classList.remove('placeholder');
        
        const cursor = document.createElement('span');
        cursor.className = 'typing-cursor';
        outputArea.appendChild(cursor);
        
        fetch('/generate_intro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            function readStream() {
                return reader.read().then(({ done, value }) => {
                    if (done) {
                        const cursor = outputArea.querySelector('.typing-cursor');
                        if (cursor) {
                            cursor.remove();
                        }
                        resetUI();
                        return;
                    }
                    
                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');
                    
                    lines.forEach(line => {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                if (data.content) {
                                    const cursor = outputArea.querySelector('.typing-cursor');
                                    const textNode = document.createTextNode(data.content);
                                    outputArea.insertBefore(textNode, cursor);
                                    
                                    outputArea.scrollTop = outputArea.scrollHeight;
                                } else if (data.error) {
                                    throw new Error(data.error);
                                }
                            } catch (e) {
                                console.error('Error parsing stream data:', e);
                            }
                        }
                    });
                    
                    return readStream();
                });
            }
            
            return readStream();
        })
        .catch(error => {
            console.error('Error:', error);
            outputArea.innerHTML = `<div style="color: #e53e3e; text-align: center; margin-top: 150px;">
                エラーが発生しました: ${error.message}<br>
                <small>Azure OpenAIの設定を確認してください</small>
            </div>`;
            resetUI();
        });
    }
    
    function resetUI() {
        isGenerating = false;
        generateBtn.disabled = false;
        generateBtn.textContent = '自己紹介を生成';
        loading.style.display = 'none';
    }
    
    function autoResize(element) {
        element.style.height = 'auto';
        element.style.height = element.scrollHeight + 'px';
    }
});
