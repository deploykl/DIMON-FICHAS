import { GoogleGenerativeAI } from "@google/generative-ai";

const API_KEY = "AIzaSyCNqOkq0X71h_rClx15f4PlWaOsN1z4pDY"; // Tu API Key aquí
const genAI = new GoogleGenerativeAI(API_KEY);

export const generateText = async (prompt) => {
  try {
    // Usar el modelo más reciente según Google Studio
    const model = genAI.getGenerativeModel({ 
      model: "gemini-1.5-flash", // o "gemini-1.5-pro" para más capacidad
      apiVersion: "v1beta" // Mantenemos v1beta como en el ejemplo
    });
    
    const result = await model.generateContent({
      contents: [{
        parts: [{
          text: prompt
        }]
      }]
    });
    
    const response = await result.response;
    return response.text();
  } catch (error) {
    console.error("Error con Gemini API:", error);
    throw error;
  }
};