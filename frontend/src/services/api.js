import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = {
  generateVideo: async (data) => {
    const response = await axios.post(`${API_BASE_URL}/generate-video`, data);
    return response.data;
  },
  
  listVideos: async () => {
    const response = await axios.get(`${API_BASE_URL}/list-videos`, { withCredentials: false });
    return response.data;
  }
};

export default api;