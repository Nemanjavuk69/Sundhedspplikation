function viewPatientMessages() {
    fetch('/doctor/get-patient-messages')
        .then(response => response.json())
        .then(data => {
            const messageList = document.getElementById('message-list');
            messageList.innerHTML = '';  // Clear the list first
            data.forEach(msg => {
                const item = document.createElement('li');
                item.textContent = `${msg.username}: ${msg.message}`;
                messageList.appendChild(item);
            });
            document.getElementById('messages').style.display = 'block';  // Make sure the list is visible
        })
        .catch(error => {
            console.error('Error loading messages:', error);
        });
}


function writePatient() {
    fetchPatients();  // Fetch and populate the dropdown
    document.getElementById('write').style.display = 'block';  // Show the form
}


function sendPatientMessage() {
    const selectedId = document.getElementById('patient-select').value;
    const message = document.getElementById('patient-message').value;
    fetch('/auth/send-to-patient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ patientId: selectedId, message: message })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.success ? "Message sent successfully!" : "Failed to send message.");
    })
    .catch(error => console.error('Error sending message:', error));
}

function logout() {
    // Logout function similar to what's already in userSettings.js
}


function fetchPatients() {
    fetch('/doctor/get-patients')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('patient-select');
            select.innerHTML = '';  // Clear previous entries
            data.forEach(patient => {
                const option = document.createElement('option');
                option.value = patient.id;
                option.textContent = patient.username;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading patients:', error));
}

function sendPatientMessage() {
    const patientId = document.getElementById('patient-select').value;
    const message = document.getElementById('patient-message').value;

    fetch('/doctor/add-patient-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId: patientId, entry: message })
    })
    .then(response => response.json())
    .then(data => {
        alert('Message saved successfully');
        document.getElementById('patient-message').value = '';  // Clear the text field
    })
    .catch(error => console.error('Error sending message:', error));
}
