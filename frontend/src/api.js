import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const diagnoseImage = async (file, language) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('language', language);
  const response = await api.post('/diagnose', formData);
  return response.data;
};

export const getDiagnoses = async () => {
  const response = await api.get('/diagnoses');
  return response.data;
};

export const getCrops = async () => {
  const response = await api.get('/crops');
  return response.data;
};

export const deleteDiagnosis = async (id) => {
  const response = await api.delete(`/diagnoses/${id}`);
  return response.data;
};

export const generateTTS = async (text, language) => {
  const response = await api.post('/tts', { text, language });
  return response.data.audio;
};

export default api;
