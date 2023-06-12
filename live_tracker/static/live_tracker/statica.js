



document.getElementById('playForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    var artistID = document.getElementById('artistID').value;
    var statusMessage = document.getElementById('statusMessage');

    statusMessage.textContent = 'In Progress...';
    statusMessage.className = 'inProgress';

    fetch('http://tracker.purpledorm.io:8000/api/upload-play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "playid": artistID,
        })
    })
    .then(response => {
        if (response.status === 200 || response.status === 201) {
            statusMessage.textContent = 'SUCCESS';
            statusMessage.className = 'success';
        } else {
            statusMessage.textContent = 'FAILED';
            statusMessage.className = 'failed';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        statusMessage.textContent = 'FAILED';
        statusMessage.className = 'failed';
    });
});






