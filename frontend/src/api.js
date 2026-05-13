import axios from 'axios';

const api = axios.create({
    // Apuntamos directamente a tu Django local (nada de Ngrok en desarrollo)
    baseURL: 'https://dexterous-reformed-overcast.ngrok-free.dev/api/',

  /*  auth: {
      username: 'admin',
      password: 'DasMasteR'
    },*/

    headers: {
        'ngrok-skip-browser-warning': 'true',
        'Content-Type': 'application/json'
    }
});

export default api;