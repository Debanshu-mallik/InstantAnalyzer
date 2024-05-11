  <script>
    document.getElementById('usernameForm').addEventListener('submit', function(event) {
      event.preventDefault();
      const username = document.getElementById('username').value;
  
      // Send the username to the server for data fetching
      fetch('/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username })
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        // Redirect to result.html after getting the analysis
        window.location.href = 'result.html';
      })
      .catch(error => {
        console.error('Error:', error);
        // Handle errors
      });
    });

    // Assuming backend.js contains the analysis code
    // Load backend.js dynamically
    const script = document.createElement('script');
    script.src = 'backend.js';
    document.body.appendChild(script);
</script>
