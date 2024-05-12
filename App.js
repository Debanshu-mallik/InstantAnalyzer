import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

function App() {
    const [username, setUsername] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);
        setLoading(true);

        try {
            const response = await axios.post('http://localhost:5000/analyze', { username });
            setResult(response.data);
        } catch (error) {
            setError(`Failed to retrieve analysis. Error: ${error.message}`);
            console.error('Error:', error);
        }

        setLoading(false);
    };

    return (
        <div>
            <h1>Username Analyzer</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username"
                />
                <button type="submit">Submit</button>
            </form>
            {loading ? <p>Loading...</p> : null}
            {error ? <p>{error}</p> : null}
            {result ? (
                <div>
                    <img src={`data:image/png;base64,${result.image_base64}`} alt="Matplotlib Plot" />
                    <Plot
                        data={JSON.parse(result.fig_json).data}
                        layout={JSON.parse(result.fig_json).layout}
                        data_2= {JSON.parse(result.fig_json_2).data}
                        layout_2={JSON.parse(result.fig_json_2).layout}
                    />
                </div>
            ) : null}
        </div>
    );
}

export default App;
