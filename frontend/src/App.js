import React, { useState } from 'react';
import './App.css';

function App() {
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleInputChange = (e) => {
    setContactForm({
      ...contactForm,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/contact/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(contactForm),
      });

      const result = await response.json();
      if (result.success) {
        alert('Message sent successfully!');
        setContactForm({ name: '', email: '', message: '' });
      } else {
        alert('Failed to send message. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Piyush Malviya</h1>
        <p>Full Stack Developer</p>
      </header>

      <main>
        <section id="about">
          <h2>About Me</h2>
          <p>
            Passionate full-stack developer with expertise in modern web technologies.
            I love creating efficient, scalable, and user-friendly applications.
          </p>
        </section>

        <section id="contact">
          <h2>Contact Me</h2>
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="name">Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={contactForm.name}
                onChange={handleInputChange}
                required
              />
            </div>
            <div>
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                name="email"
                value={contactForm.email}
                onChange={handleInputChange}
                required
              />
            </div>
            <div>
              <label htmlFor="message">Message:</label>
              <textarea
                id="message"
                name="message"
                value={contactForm.message}
                onChange={handleInputChange}
                required
              ></textarea>
            </div>
            <button type="submit">Send Message</button>
          </form>
        </section>
      </main>

      <footer>
        <p>&copy; 2024 Piyush Malviya. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;