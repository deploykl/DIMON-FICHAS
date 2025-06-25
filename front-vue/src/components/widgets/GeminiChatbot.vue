<template>
  <div class="chatbot-container" :class="{ 'chatbot-open': isOpen }">
    <button class="chatbot-toggle" @click="toggleChat">
      <span v-if="!isOpen">💬</span>
      <span v-else>✕</span>
    </button>

    <div class="chatbot-window" v-if="isOpen">
      <div class="chatbot-header">
        <h3>ChatBot</h3>
      </div>

      <div class="chatbot-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
          <div class="message-content">
            <div v-if="message.role === 'assistant'" class="message-avatar">🤖</div>
            <div v-html="formatMessage(message.content)"></div>
          </div>
        </div>

        <div v-if="loading" class="message assistant">
          <div class="message-content">
            <div class="message-avatar">🤖</div>
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chatbot-input">
        <textarea v-model="userInput" @keyup.enter.exact="sendMessage" placeholder="Escribe tu pregunta..." rows="1"
          ref="inputField"></textarea>
        <button @click="sendMessage" :disabled="loading">
          <span v-if="!loading">↩</span>
          <span v-else class="spinner"></span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import { generateResponseWithContext } from '@/components/services/gemini-context';

const isOpen = ref(false);
const userInput = ref('');
const messages = ref([]);
const loading = ref(false);
const chatHistory = ref([]);
const messagesContainer = ref(null);
const inputField = ref(null);

// Mover mounted a onMounted
onMounted(() => {
  addMessage('assistant', '¡Hola! Soy tu asistente especializado. ¿En qué puedo ayudarte hoy?');
});
// Add this inside your <script setup> section
const formatMessage = (content) => {
  // Simple formatting - you can enhance this as needed
  if (!content) return '';
  
  // Convert markdown-like formatting to HTML
  let formatted = content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // bold
    .replace(/\*(.*?)\*/g, '<em>$1</em>') // italic
    .replace(/`(.*?)`/g, '<code>$1</code>'); // code
  
  // Convert newlines to <br> tags
  formatted = formatted.replace(/\n/g, '<br>');
  
  return formatted;
};
const toggleChat = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    nextTick(() => {
      scrollToBottom();
      inputField.value?.focus();
    });
  }
};

const addMessage = (role, content) => {
  messages.value.push({ role, content });
  nextTick(scrollToBottom);
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// Resto de tus métodos sin cambios...
const sendMessage = async () => {
  const input = userInput.value.trim();
  if (!input || loading.value) return;

  addMessage('user', input);
  userInput.value = '';
  loading.value = true;
  
  try {
    const response = await generateResponseWithContext(input, {
      model: "gemini-1.5-flash",
      maxTokens: 2048,
      temperature: 0.7
    });
    
    addMessage('assistant', response);
    updateChatHistory(input, response);
  } catch (error) {
    console.error('Error:', error);
    addMessage('assistant', getErrorMessage(error));
  } finally {
    loading.value = false;
    nextTick(() => {
      scrollToBottom();
      inputField.value?.focus();
    });
  }
};

const getErrorMessage = (error) => {
  if (error.message.includes('API_KEY')) {
    return 'Error de autenticación. Verifica tu API Key.';
  } else if (error.message.includes('quota')) {
    return 'Se ha excedido la cuota de la API.';
  } else if (error.message.includes('fetch')) {
    return 'Error al conectar con nuestros sistemas internos. Por favor, inténtalo más tarde.';
  } else {
    return 'Lo siento, hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo.';
  }
};

const updateChatHistory = (userInput, assistantResponse) => {
  chatHistory.value.push(
    { role: 'user', content: userInput },
    { role: 'assistant', content: assistantResponse }
  );
  
  if (chatHistory.value.length > 10) {
    chatHistory.value = chatHistory.value.slice(-10);
  }
};

// Watcher para el textarea
watch(userInput, (val) => {
  nextTick(() => {
    const textarea = inputField.value;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
    }
  });
});
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  transition: all 0.3s ease;
}

.chatbot-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #0b4a7a;
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.chatbot-toggle:hover {
  background: #083758;
  transform: scale(1.1);
}

.chatbot-window {
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin-bottom: 15px;
}

.chatbot-header {
  padding: 15px;
  background: #0b4a7a;
  color: white;
  font-weight: bold;
  text-align: center;
}

.chatbot-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #f9f9f9;
}

.message {
  margin-bottom: 15px;
}

.message-content {
  display: flex;
  gap: 10px;
  max-width: 80%;
}

.message.user {
  justify-content: flex-end;
}

.message.user .message-content {
  background: #0b4a7a;
  color: white;
  padding: 10px 15px;
  border-radius: 18px 18px 0 18px;
}

.message.assistant .message-content {
  background: #e9e9e9;
  padding: 10px 15px;
  border-radius: 18px 18px 18px 0;
}

.message-avatar {
  font-size: 20px;
  margin-top: 2px;
}

.chatbot-input {
  display: flex;
  padding: 10px;
  background: white;
  border-top: 1px solid #eee;
}

.chatbot-input textarea {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 10px 15px;
  resize: none;
  max-height: 150px;
  outline: none;
  font-family: inherit;
}

.chatbot-input button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #0b4a7a;
  color: white;
  margin-left: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chatbot-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.typing-indicator {
  display: flex;
  align-items: center;
  height: 20px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background-color: #666;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0);
  }

  40% {
    transform: scale(1);
  }
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

pre {
  background: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
  margin: 5px 0;
}

code {
  font-family: monospace;
  white-space: pre;
}

strong {
  font-weight: bold;
}

em {
  font-style: italic;
}
</style>