import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.detail || 'Signup failed');
        return;
      }
      navigate('/login');
    } catch (err) {
      setError('Network error');
    }
  };

  return (
    <div style={styles.container}>
      <form onSubmit={handleSignup} style={styles.form}>
        <h2>Sign Up</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          style={styles.input} 
          required 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          style={styles.input} 
          required 
        />
        <button type="submit" style={styles.button}>Sign Up</button>
        <p style={styles.linkText}>
           Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}

const styles = {
  container: { display: 'flex', height: '100vh', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f8fafc' },
  form: { padding: '40px', backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 4px 10px rgba(0,0,0,0.1)', display: 'flex', flexDirection: 'column', width: '300px' },
  input: { marginBottom: '15px', padding: '10px', borderRadius: '4px', border: '1px solid #ccc' },
  button: { padding: '10px', backgroundColor: '#6366f1', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' },
  linkText: { marginTop: '15px', textAlign: 'center', fontSize: '14px' }
};

export default Signup;
