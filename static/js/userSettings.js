// Function to show the user's health journal entries
function showHealthJournal() {
  fetch('/auth/get-journal-entries')  // Adjust endpoint as necessary
      .then(response => response.json())  // Parse the response as JSON
      .then(data => {  // Handle the JSON data
          const entriesList = document.getElementById('journal-entries');  // Get the element to display entries
          entriesList.innerHTML = '';  // Clear previous entries
          data.forEach(entry => {  // Iterate over each journal entry
              let li = document.createElement('li');  // Create a list item element
              li.textContent = entry;  // Set the text content of the list item
              entriesList.appendChild(li);  // Append the list item to the entries list
          });
          document.getElementById('journal').style.display = 'block';  // Make sure the journal is visible
          
          // Log the cookies to the console
          // console.log('Cookies:', document.cookie);
      })
      .catch(error => console.error('Failed to load journal entries:', error));  // Handle errors
}

// Function to prompt user to write a message to a doctor and send it
function writeDoctor() {
  var message = prompt("Please enter your message for the doctor:");  // Prompt the user for a message
  if (message) {  // If the user entered a message
      fetch('/auth/send-message', {
          method: 'POST',  // Use POST method to send the message
          headers: {
              'Content-Type': 'application/json',  // Set the content type to JSON
          },
          body: JSON.stringify({ message: message })  // Send the message in the request body as JSON
      })
      .then(response => response.json())  // Parse the response as JSON
      .then(data => {  // Handle the JSON data
          if(data.success) {  // If the message was sent successfully
              alert("Your message has been sent successfully.");  // Alert the user
          } else {  // If the message failed to send
              alert("Failed to send message.");  // Alert the user
          }
      })
      .catch(error => console.error('Error sending message:', error));  // Handle errors
  }
}

// Function to handle user logout
function logout() {
  fetch('/logout', {
      method: 'POST'  // Use POST method to log out
  })
  .then(() => {
      window.location.href = "/"; // Redirect to home screen
  })
  .catch(error => console.error('Logout failed:', error));  // Handle errors
}
