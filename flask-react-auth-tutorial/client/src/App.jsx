import React, { useState, useEffect } from 'react';
import { loginUser, getProtectedData, registerUser } from './api';

function App() {
    // State management
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [protectedData, setProtectedData] = useState(null);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);

    // Effect to store/remove the token from localStorage
    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
        } else {
            localStorage.removeItem('token');
        }
    }, [token]);

    // --- Event Handlers ---

    const handleAuthAction = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        try {
            if (isRegistering) {
                // Handle Registration
                const data = await registerUser({ email, password });
                setMessage(data.message);
                setIsRegistering(false); // Switch to login view after successful registration
            } else {
                // Handle Login
                const data = await loginUser({ email, password });
                setToken(data.token);
            }
        } catch (err) {
            setError(err.message);
        }
    };

    const handleLogout = () => {
        setToken(null);
        setProtectedData(null);
        setError('');
        setMessage('');
    };

    const handleFetchProtectedData = async () => {
        setError('');
        setProtectedData(null);
        try {
            const data = await getProtectedData(token);
            setProtectedData(data.message);
        } catch (err) {
            setError(err.message);
            // If the token is expired or invalid, log the user out
            if (err.message.includes('expired') || err.message.includes('Invalid')) {
                handleLogout();
            }
        }
    };

    // --- Render Logic ---

    if (!token) {
        return (
            <div>
                <h1>{isRegistering ? 'Register' : 'Login'}</h1>
                <form onSubmit={handleAuthAction}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <br />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <br />
                    <button type="submit">{isRegistering ? 'Register' : 'Login'}</button>
                </form>
                <button onClick={() => { setIsRegistering(!isRegistering); setError(''); setMessage(''); }}>
                    {isRegistering ? 'Switch to Login' : 'Switch to Register'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {message && <p style={{ color: 'green' }}>{message}</p>}
            </div>
        );
    }

    return (
        <div>
            <h1>Welcome!</h1>
            <p>You are logged in.</p>
            <button onClick={handleLogout}>Logout</button>
            <hr />
            <button onClick={handleFetchProtectedData}>Fetch Protected Data</button>
            {protectedData && <p style={{ color: 'blue' }}>{protectedData}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default App;
