function viewPatientMessages() {
    fetch('/auth/view-messages')  // Endpoint to fetch patient messages
        .then(response => response.json())
        .then(messages => {
            const messageList = document.getElementById('message-list');
            messageList.innerHTML = ''; // Clear previous messages
            messages.forEach(msg => {
                let li = document.createElement('li');
                li.textContent = `${msg.username}: ${msg.message}`;
                messageList.appendChild(li);
            });
            document.getElementById('messages').style.display = 'block';
        })
        .catch(error => console.error('Failed to load messages:', error));
}

function writePatient() {
    fetch('/auth/get-patients')  // Endpoint to get patient usernames
        .then(response => response.json())
        .then(patients => {
            const select = document.getElementById('patient-select');
            select.innerHTML = ''; // Clear previous entries
            patients.forEach(patient => {
                let option = document.createElement('option');
                option.value = patient.id;
                option.textContent = patient.username;
                select.appendChild(option);
            });
            document.getElementById('write').style.display = 'block';
        })
        .catch(error => console.error('Error loading patients:', error));
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
