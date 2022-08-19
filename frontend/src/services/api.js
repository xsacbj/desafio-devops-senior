import axios from 'axios';

import {getToken, logout as authLogout} from './auth';

export const api = axios.create({
  baseURL: "http://localhost:5000",
});

async function login(nickname, password) {
  return await api.post('/auth', { nickname, password });
}

function logout() {
  authLogout()
}

async function getMaintenance() {
  return await api.get('/maintenances', null, {
    headers: {
      Authorization: `${getToken()}`,
    },
  });
}


export {login, logout};
