document.addEventListener('DOMContentLoaded', function() {
    const chatFormButton = document.getElementById('submit-btn'); 
    const chatInput = document.getElementById('topic-input');    
    const messagesContainer = document.getElementById('messages-container'); 
    const chatContainer = document.getElementById('chat-container');

    chatFormButton.addEventListener('click', async function(event) {
        event.preventDefault();
        const userMessage = chatInput.value.trim();

        if (userMessage === '') {
            return;
        }

        addMessage('Você', userMessage, 'user-message');
        chatInput.value = '';

        const thinkingMessage = addMessage('Nila', 'Pensando...', 'assistant-message', true);

        try {
            const runResponse = await fetch('/run_crew', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topic: userMessage }),
            });

            if (!runResponse.ok) {
                throw new Error(`HTTP error! status: ${runResponse.status}`);
            }

            const runData = await runResponse.json();
            const taskId = runData.task_id;

            if (!taskId) {
                throw new Error('Não foi possível obter o ID da tarefa.');
            }

            const result = await pollForResult(taskId);
            
            updateMessage(thinkingMessage, result.result);

        } catch (error) {
            console.error('Erro ao processar a solicitação:', error);
            updateMessage(thinkingMessage, 'Desculpe, ocorreu um erro ao tentar processar sua pergunta.');
        }
    });

    function pollForResult(taskId) {
        return new Promise((resolve, reject) => {
            const intervalId = setInterval(async () => {
                try {
                    const resultResponse = await fetch(`/get_result/${taskId}`);
                    if (!resultResponse.ok) {
                        clearInterval(intervalId);
                        reject(new Error(`Erro ao buscar resultado: ${resultResponse.statusText}`));
                        return;
                    }

                    const resultData = await resultResponse.json();

                    if (resultData.status === 'completed') {
                        clearInterval(intervalId);
                        resolve(resultData);
                    } else if (resultData.status === 'error') {
                        clearInterval(intervalId);
                        reject(new Error(resultData.message || 'A tarefa falhou no servidor.'));
                    }

                } catch (error) {
                    clearInterval(intervalId);
                    reject(error);
                }
            }, 3000);
        });
    }

    function addMessage(sender, text, messageClass, isThinking = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', messageClass);
        
        const senderElement = document.createElement('strong');
        senderElement.textContent = sender;
        
        const textElement = document.createElement('p');
        textElement.style.margin = '0';
        textElement.textContent = text;
        
        if (isThinking) {
            textElement.innerHTML += ' <span class="thinking-dots">.</span><span class="thinking-dots">.</span><span class="thinking-dots">.</span>';
        }

        messageElement.appendChild(senderElement);
        messageElement.appendChild(textElement);
        messagesContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight; 
        return messageElement;
    }

    function updateMessage(messageElement, newText) {
        const existingTextElement = messageElement.querySelector('p');
        existingTextElement.innerHTML = ''; 
        existingTextElement.textContent = newText;
    }
});