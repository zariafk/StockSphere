import axios from 'axios';

// Get CSRF token from cookies
const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/);

window.onload = function () {
    if (csrftoken) {
        axios.defaults.headers.common['X-CSRFToken'] = csrftoken[1]; // Set CSRF token globally
    } else {
        console.error('CSRF token not found in cookies');
    }
}

// Ensure cookies are sent with requests (for cross-origin requests)
axios.defaults.withCredentials = true;

export default axios;
