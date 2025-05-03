import axios from 'axios';

// Get CSRF token from cookies
const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];

axios.defaults.headers.common['X-CSRFToken'] = csrftoken; // Set CSRF token globally

export default axios;
