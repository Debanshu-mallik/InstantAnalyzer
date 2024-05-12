const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const app = express();

app.use(cors({origin: 'hhtp://localhost:3000'}));
app.use(express.json());

// Assuming you have a route in your Node.js server to handle the GET request for user analysis data
app.get('/user-analysis', (req, res) => {
    const { username } = req.query; // Extract the username from the query parameters

    const sqlite3 = require('sqlite3').verbose();

    // Function to retrieve user analysis data from the SQLite database
    const retrieveUserAnalysisDataFromDatabase = (username) => {
        // Replace 'your_database_file.db' with the actual name of your SQLite database file
        const db = new sqlite3.Database('user_analysis.db', sqlite3.OPEN_READWRITE, (err) => {
            if (err) {
                console.error(err.message);
            } else {
                console.log('Connected to the SQLite database');
            }
        });
    
        // Assuming you have a table named 'user_analysis' in your database
        const sql = `SELECT * FROM UserAnalysis WHERE username = ?`;
        
        return new Promise((resolve, reject) => {
            db.get(sql, [username], (err, row) => {
                if (err) {
                    reject(err.message);
                } else {
                    resolve(row); // Assuming the data is stored in a single row for each username
                }
            });
        });
    };
    
    module.exports = retrieveUserAnalysisDataFromDatabase;
    const userAnalysisData = retrieveUserAnalysisDataFromDatabase(username);

    if (userAnalysisData) {
        res.send(userAnalysisData);
    } else {
        res.status(404).send({ error: 'User analysis data not found' });
    }
});


app.post('/analyze', (req, res) => {
    const { username } = req.body;

    const process = spawn('python', ['InstantAnalyzer.ipynb'], {
        stdio: ['pipe', 'pipe', process.stderr]
    });

    process.stdin.write(JSON.stringify({ username }));
    process.stdin.end();

    let output = '';
    process.stdout.on('data', (data) => {
        output += data.toString();
    });

    process.on('close', (code) => {
        try {
            const result = JSON.parse(output); // Assuming output is a JSON string
            res.send(result);
        } catch (error) {
            res.status(500).send({ error: 'Failed to parse Python script output' });
        }
    });
});
app.listen(5000, () => console.log('Server running on http://localhost:5000'));
