// Function to show the user's health journal entries
function showHealthJournal() {
  fetch('/auth/get-journal-entries')  // Adjust endpoint as necessary
      .then(response => response.json())
      .then(data => {
          const entriesList = document.getElementById('journal-entries');
          entriesList.innerHTML = '';  // Clear previous entries
          data.forEach(entry => {
              let li = document.createElement('li');
              li.textContent = entry;
              entriesList.appendChild(li);
          });
          document.getElementById('journal').style.display = 'block';  // Make sure the journal is visible
          
          // Log the cookies to the console
          // console.log('Cookies:', document.cookie);
      })
      .catch(error => console.error('Failed to load journal entries:', error));
    }
  
  // Function to prompt user to write a message to a doctor and send it
  function writeDoctor() {
    var message = prompt("Please enter your message for the doctor:");
    if (message) {
        fetch('/auth/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert("Your message has been sent successfully.");
            } else {
                alert("Failed to send message.");
            }
        })
        .catch(error => console.error('Error sending message:', error));
    }
}
  
  // Function to handle user logout
  function logout() {
    fetch('/logout', {
      method: 'POST'
    })
    .then(() => {
      window.location.href = "/"; // Redirect to home screen
    })
    .catch(error => console.error('Logout failed:', error));
  }
  