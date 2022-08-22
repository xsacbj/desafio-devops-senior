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

async function getMaintenances() {

  const token = getToken();

  return await api.get('/maintenances', {
    headers: {
      'Authorization': token,
    }
  });

}

async function getMaintenanceById(id) {
  const token = getToken();

  return await api.get(`/maintenance/${id}`, {
    headers: {
      'Authorization': token,
    }
  });
}

async function putMaintenanceById(id, data) {
  const token = getToken();

  return await api.put(`/maintenance/${id}`, data, {
    headers: {
      'Authorization': token,
    }
  });
}

async function putServiceById(id, data) {
  const token = getToken();

  return await api.put(`/service/${id}`, data, {
    headers: {
      'Authorization': token,
    }
  });
}

async function deleteMaintenanceById(id) {
  const token = getToken();

  return await api.delete(`/maintenance/${id}`, {
    headers: {
      'Authorization': token,
    }
  });
}

async function deleteServiceById(id) {
  const token = getToken();

  return await api.delete(`/service/${id}`, {
    headers: {
      'Authorization': token,
    }
  });
}

async function postMaintenance(data) {
  const token = getToken();

  return await api.post('/maintenance', data, {
    headers: {
      'Authorization': token,
    }
  });
}

async function postService(data) {
  const token = getToken();

  return await api.post('/service', data, {
    headers: {
      'Authorization': token,
    }
  });
}

export {
  login, logout, getMaintenances, getMaintenanceById, 
  putMaintenanceById, putServiceById, deleteMaintenanceById, 
  deleteServiceById, postMaintenance, postService
};
