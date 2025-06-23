<template>
  <div class="chatbot-container" :class="{ 'chatbot-hidden': !isOpen }">
    <div class="chatbot-header" @click="toggleChat">
      <h3>Asistente Virtual</h3>
      <span class="toggle-icon">{{ isOpen ? '−' : '+' }}</span>
    </div>
    
    <div class="chatbot-body" v-show="isOpen">
      <div class="chat-messages">
        <div v-for="(message, index) in messages" :key="index" 
             :class="['message', message.type]">
          <div class="message-content">{{ message.text }}</div>
        </div>
      </div>
      
      <div class="chat-input">
        <input v-model="userMessage" 
               @keyup.enter="sendMessage" 
               placeholder="Escribe tu mensaje..." />
        <button @click="sendMessage">Enviar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FloatingChat',
  data() {
    return {
      isOpen: false,
      userMessage: '',
      messages: [
        { text: '¡Hola! ¿En qué puedo ayudarte hoy?', type: 'bot' }
      ]
    }
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen
    },
 async sendMessage() {
  if (!this.userMessage.trim()) return
  
  this.messages.push({
    text: this.userMessage,
    type: 'user'
  })
  
  const userText = this.userMessage
  this.userMessage = ''
  
  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer TU_API_KEY`
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [{role: "user", content: userText}],
        temperature: 0.7
      })
    });
    
    const data = await response.json();
    const botReply = data.choices[0].message.content;
    
    this.messages.push({
      text: botReply,
      type: 'bot'
    })
  } catch (error) {
    this.messages.push({
      text: 'Lo siento, hubo un error al conectar con el servidor.',
      type: 'bot'
    })
  }
},
    getBotResponse(userText) {
      // Respuestas simples (en un caso real, conectarías con ChatGPT API)
      const responses = [
        "Entiendo lo que dices sobre: " + userText,
        "Interesante pregunta sobre " + userText + ". ¿Necesitas más ayuda?",
        "Puedo ayudarte con eso. ¿Qué más necesitas saber?",
        "Gracias por tu mensaje. Estoy procesando tu solicitud."
      ]
      return responses[Math.floor(Math.random() * responses.length)]
    }
  }
}
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
}

.chatbot-hidden {
  height: 50px !important;
}

.chatbot-header {
  background: #4a6fa5;
  color: white;
  padding: 15px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-icon {
  font-size: 20px;
  font-weight: bold;
}

.chatbot-body {
  display: flex;
  flex-direction: column;
  height: 400px;
}

.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #f9f9f9;
}

.message {
  margin-bottom: 15px;
  max-width: 80%;
}

.message.user {
  margin-left: auto;
}

.message.bot {
  margin-right: auto;
}

.message-content {
  padding: 10px 15px;
  border-radius: 18px;
}

.user .message-content {
  background: #4a6fa5;
  color: white;
  border-bottom-right-radius: 5px;
}

.bot .message-content {
  background: #e5e5ea;
  color: black;
  border-bottom-left-radius: 5px;
}

.chat-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  background: white;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-input button {
  margin-left: 10px;
  padding: 10px 15px;
  background: #4a6fa5;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.chat-input button:hover {
  background: #3a5a80;
}
</style>