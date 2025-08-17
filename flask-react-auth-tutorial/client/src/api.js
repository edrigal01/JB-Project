const API_BASE_URL = 'http://localhost:5001';

/**
 * A helper function to handle fetch responses.
 */
const handleResponse = async (response) => {
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `Error: ${response.status}`);
    }
    return response.json();
};

/**
 * Logs in a user.
 * @param {object} credentials - The user's credentials.
 * @param {string} credentials.email - The user's email.
 * @param {string} credentials.password - The user's password.
 * @returns {Promise<object>} The server response, including the token.
 */
export const loginUser = (credentials) => {
    return fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
    }).then(handleResponse);
};

/**
 * Fetches protected data from the server.
 * @param {string} token - The JWT for authentication.
 * @returns {Promise<object>} The protected data.
 */
export const getProtectedData = (token) => {
    return fetch(`${API_BASE_URL}/api/protected`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    }).then(handleResponse);
};

/**
 * Registers a new user.
 * @param {object} userData - The user's data.
 * @param {string} userData.email - The user's email.
 * @param {string} userData.password - The user's password.
 * @returns {Promise<object>} The server response.
 */
export const registerUser = (userData) => {
    return fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    }).then(handleResponse);
};
