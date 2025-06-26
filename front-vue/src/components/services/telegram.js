import axios from 'axios';

const sendTelegramAlert = async (seguimientoData) => {
  try {
    const message = `
NUEVO SEGUIMIENTO REGISTRADO
      
Fecha: ${seguimientoData.fecha_seguimiento}
IPRESS: ${seguimientoData.matriz.evaluacion.establecimiento}
Estado: ${seguimientoData.estado}

Análisis: ${seguimientoData.analisis_accion}
    `;
    
    await axios.post('https://api.telegram.org/bot7330411663:AAHYMEZibTRBrQl-SLd3fECZPlIOBPsXc68/sendMessage', {
      chat_id: '-4959493418',
      text: message
    });
  } catch (error) {
    console.error('Error enviando alerta a Telegram:', error);
  }
};

// Cuando envías el formulario:
async function submitSeguimiento() {
  const response = await api.post('/seguimientos/', formData);
  if (response.data.id) {
    await sendTelegramAlert(response.data);
  }
}