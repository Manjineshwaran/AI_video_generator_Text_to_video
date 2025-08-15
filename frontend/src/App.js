import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Videos from './pages/Videos';
import './App.css';

function App() {
  return (
    <div className="App">
      <Header />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          {/* <Route path="/videos" element={<Videos />} /> */}
        </Routes>
      </main>
    </div>
  );
}

export default App;