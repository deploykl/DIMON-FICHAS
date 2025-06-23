import { generateText } from './gemini';
import { api } from './auth_axios';

// Función para obtener contexto de las APIs
// Función para obtener contexto de las APIs
export const getApiContext = async (endpoint) => {
  try {
    const response = await api.get(endpoint);
    return response.data;
  } catch (error) {
    console.error(`Error fetching data from ${endpoint}:`, error);
    return null;
  }
};

// Función principal que genera respuestas con contexto
export const generateResponseWithContext = async (prompt, options = {}) => {
  // Primero intentamos obtener contexto relevante de las APIs
  let context = '';
  
  // Identificar qué información necesita el usuario
  if (prompt.toLowerCase().includes('proceso') || prompt.toLowerCase().includes('ficha')) {
    const procesos = await getApiContext('ficha/proceso/');
    if (procesos) {
      context += `\nInformación de procesos disponibles:\n${JSON.stringify(procesos, null, 2)}`;
    }
  }
  
  if (prompt.toLowerCase().includes('subproceso')) {
    const subprocesos = await getApiContext('ficha/subproceso/');
    if (subprocesos) {
      context += `\nInformación de subprocesos:\n${JSON.stringify(subprocesos, null, 2)}`;
    }
  }
  
  if (prompt.toLowerCase().includes('verificador')) {
    const verificadores = await getApiContext('ficha/verificador/');
    if (verificadores) {
      context += `\nInformación de verificadores:\n${JSON.stringify(verificadores, null, 2)}`;
    }
  }
  
  if (prompt.toLowerCase().includes('evaluación') || prompt.toLowerCase().includes('evaluar')) {
    const evaluaciones = await getApiContext('ficha/evaluaciones/');
    if (evaluaciones) {
      context += `\nInformación de evaluaciones:\n${JSON.stringify(evaluaciones, null, 2)}`;
    }
  }
  
  if (prompt.toLowerCase().includes('matriz') || prompt.toLowerCase().includes('compromiso')) {
    const matrices = await getApiContext('ficha/matriz-compromiso/');
    if (matrices) {
      context += `\nInformación de matrices de compromiso:\n${JSON.stringify(matrices, null, 2)}`;
    }
  }
  
  if (prompt.toLowerCase().includes('categoría') || prompt.toLowerCase().includes('categoria')) {
    const categorias = await getApiContext('ficha/categoria/');
    if (categorias) {
      context += `\nInformación de categorías:\n${JSON.stringify(categorias, null, 2)}`;
    }
  }
  
  // Construir el prompt final con contexto
  const fullPrompt = `
    Eres un asistente especializado en procesos empresariales y gestión de calidad.
    El usuario ha preguntado: "${prompt}"
    
    Aquí tienes información relevante de nuestras APIs:
    ${context}
    
    Proporciona una respuesta clara, concisa y profesional basada en esta información.
    Si la pregunta requiere datos específicos que no están disponibles, indica qué información falta.
    Siempre sé preciso y evita inventar datos.
  `;
  
  // Generar la respuesta usando Gemini
  return await generateText(fullPrompt, options);
};