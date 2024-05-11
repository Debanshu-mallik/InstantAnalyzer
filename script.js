document.getElementById("usernameForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form submission

  // Get the value entered in the input field
  var username = document.getElementById("username").value;

  // Send the username value to the Python script using fetch API
  fetch("/path/to/InstantAnalyzer.py", {
    method: "POST",
    body: JSON.stringify({ username: username }),
    headers: {
      "Content-Type": "application/json"
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.text();
  })
  .then(data => {
    // Redirect to results.html with the username as query parameter
    window.location.href = `/results.html?username=${encodeURIComponent(username)}`;
  })
  .catch(error => {
    console.error("There was a problem with the fetch operation:", error);
  });
});
