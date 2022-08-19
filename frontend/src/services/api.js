import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.REACT_APP_URL_API
});

async function login(nickname, password) {
  return await api.post('/auth', { nickname, password });
}



export {login};
