document.getElementById('apiForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    var artistID = document.getElementById('artistID').value;
    var artistName = document.getElementById('artistName').value;

    fetch('http://127.0.0.1:8000/api/upload-audio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "aid": artistID,
            "artistName": artistName
        })
    })
    .then(response => {
        if (response.status === 200 || response.status === 201) {
            document.getElementById('statusMessage').textContent = 'SUCCESS';
        } else {
            document.getElementById('statusMessage').textContent = 'FAILED';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('statusMessage').textContent = 'FAILED';
    });
});
