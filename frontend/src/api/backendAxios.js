import axios from 'axios';

const backendApi = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8080',
});

// No JWT — no Authorization header needed. All endpoints are open.
export default backendApi;
