import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './Login.css';
import MyFeed from './MyFeed';
import Footer from './Footer';
function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const handleSubmit = (event) => {
    event.preventDefault();
    fetch('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // Handle successful login
        if(data["code"] = "12345"){
          ReactDOM.render(<Footer />, document.getElementById('root'));
        }
      })
      .catch(error => {
        // Handle failed login
        console.error('There was an error logging in:', error);
      });
  };

  return (
    <div className="overlay">
        <form onSubmit={handleSubmit}>   
            <div class="con">  
                <h2>Login to vent</h2>
                <div class="field-set">
                    <label>
                        <input type="text" className="form-input" value={username} placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
                    </label>
                    <label>
                        <input type="password" className="form-input" value={password} placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
                    </label>
                    <button className="btn submits sign-up" type="submit">Log in</button>
                </div> 
            </div>
        </form>
    </div>
  );
}

export default Login;