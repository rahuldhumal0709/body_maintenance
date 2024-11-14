// // src/SignIn.js

// import React, { useState } from 'react';
// import './SignIn.css';

// const SignIn = () => {
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [message, setMessage] = useState('');

//     const handleSubmit = async (event) => {
//         event.preventDefault();
//         const response = await fetch('http://localhost:8000/api/token/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ email, password }),
//         });
//         const data = await response.json();
//         setMessage(data.message);
//     };

//     return (
//         <div className="sign-in-container">
//             <form className="sign-in-form" onSubmit={handleSubmit}>
//                 <h2>Sign In</h2>
//                 <div className="form-group">
//                     <label htmlFor="email">Email:</label>
//                     <input
//                         type="email"
//                         id="email"
//                         value={email}
//                         onChange={(e) => setEmail(e.target.value)}
//                         required
//                     />
//                 </div>
//                 <div className="form-group">
//                     <label htmlFor="password">Password:</label>
//                     <input
//                         type="password"
//                         id="password"
//                         value={password}
//                         onChange={(e) => setPassword(e.target.value)}
//                         required
//                     />
//                 </div>
//                 <button type="submit" className="sign-in-button">Sign In</button>
//                 {message && <p>{message}</p>}
//             </form>
//         </div>
//     );
// };

// export default SignIn;
