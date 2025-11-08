import axiosClient from './axiosClient';

const authApi = {
  // Login: access + refresh
  login: async (username, password) => {
    const response = await axiosClient.post('/auth/token/', {
      username,
      password,
    });
    return response.data;
  },

  // Current user credentials
  getProfile: async () => {
    const response = await axiosClient.get('/auth/me/');
    return response.data;
  },

  // Token update
  refreshToken: async (refreshToken) => {
    const response = await axiosClient.post('/auth/token/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  },
};

export default authApi;

