import React from 'react';
import axios from 'axios';

const Simulation = () => {
    const startSimulation = async () => {
        try {
            await axios.post('http://localhost:8000/simulate');
        } catch (error) {
            console.error("Error starting simulation:", error);
        }
    };

    return (
        <div>
            <h1>Simulation Page</h1>
            <button onClick={startSimulation}>Start Simulation</button>
        </div>
    );
};

export default Simulation;
