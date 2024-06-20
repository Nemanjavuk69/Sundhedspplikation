function viewPatientMessages() {
    fetch('/doctor/get-patient-messages')  // Fetch patient messages from the server
        .then(response => response.json())  // Parse the response as JSON
        .then(data => {  // Handle the JSON data
            const messageList = document.getElementById('message-list');  // Get the element to display messages
            messageList.innerHTML = '';  // Clear the list first
            data.forEach(msg => {  // Iterate over each message
                const item = document.createElement('li');  // Create a list item element
                item.textContent = `${msg.username}: ${msg.message}`;  // Set the text content of the list item
                messageList.appendChild(item);  // Append the list item to the message list
            });
            document.getElementById('messages').style.display = 'block';  // Make sure the list is visible
        })
        .catch(error => {  // Handle errors
            console.error('Error loading messages:', error);  // Log the error
        });
}

function writePatient() {
    fetchPatients();  // Fetch and populate the dropdown with patients
    document.getElementById('write').style.display = 'block';  // Show the form
}

function sendPatientMessage() {
    const selectedId = document.getElementById('patient-select').value;  // Get the selected patient ID
    const message = document.getElementById('patient-message').value;  // Get the message text
    fetch('/auth/send-to-patient', {  // Send the message to the server
        method: 'POST',  // Use POST method
        headers: {
            'Content-Type': 'application/json',  // Set the content type to JSON
        },
        body: JSON.stringify({ patientId: selectedId, message: message })  // Send the patient ID and message in the request body
    })
    .then(response => response.json())  // Parse the response as JSON
    .then(data => {  // Handle the JSON data
        alert(data.success ? "Message sent successfully!" : "Failed to send message.");  // Alert the user based on success or failure
    })
    .catch(error => console.error('Error sending message:', error));  // Handle errors
}

function logout() {
    // Logout function similar to what's already in userSettings.js
}

function fetchPatients() {
    fetch('/doctor/get-patients')  // Fetch the list of patients from the server
        .then(response => response.json())  // Parse the response as JSON
        .then(data => {  // Handle the JSON data
            const select = document.getElementById('patient-select');  // Get the dropdown element
            select.innerHTML = '';  // Clear previous entries
            data.forEach(patient => {  // Iterate over each patient
                const option = document.createElement('option');  // Create an option element
                option.value = patient.id;  // Set the value of the option
                option.textContent = patient.username;  // Set the text content of the option
                select.appendChild(option);  // Append the option to the dropdown
            });
        })
        .catch(error => console.error('Error loading patients:', error));  // Handle errors
}

function sendPatientMessage() {
    const patientId = document.getElementById('patient-select').value;  // Get the selected patient ID
    const message = document.getElementById('patient-message').value;  // Get the message text

    fetch('/doctor/add-patient-note', {  // Send the message to the server
        method: 'POST',  // Use POST method
        headers: {
            'Content-Type': 'application/json',  // Set the content type to JSON
        },
        body: JSON.stringify({ userId: patientId, entry: message })  // Send the patient ID and message in the request body
    })
    .then(response => response.json())  // Parse the response as JSON
    .then(data => {  // Handle the JSON data
        alert('Message saved successfully');  // Alert the user of success
        document.getElementById('patient-message').value = '';  // Clear the text field
    })
    .catch(error => console.error('Error sending message:', error));  // Handle errors
}
