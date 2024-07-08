import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Simulation from './components/Simulation';
import History from './components/History';
import Navbar from './components/Navbar';

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<Simulation />} />
                <Route path="/history" element={<History />} />
            </Routes>
        </Router>
    );
}

export default App;
