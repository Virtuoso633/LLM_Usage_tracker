document.addEventListener('DOMContentLoaded', function() {
    //const API_URL = window.location.origin;// for vercel 
    //const API_URL = 'http://localhost:5000';  // Local development API URL
    const statusDiv = document.getElementById('status');
    const debugDiv = document.getElementById('debug');
    const contentDiv = document.getElementById('content');

    // Show loading status
    statusDiv.innerHTML = '<p>Connecting to backend...</p>';


     // Test backend connection
    fetch(`/api/test`)
        .then(response => {
            debugDiv.innerHTML += `<br>Response status: ${response.status}`;
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                statusDiv.innerHTML = `<p style="color: green;">Backend connected! ${data.message}</p>`;
                contentDiv.style.display = 'block';
            } else {
                throw new Error(data.message || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Backend error:', error);
            statusDiv.innerHTML = `<p style="color: red;">Connection failed: ${error.message}</p>`;
        });

    // Populate timezone dropdown
    const timezoneSelect = document.getElementById('timezone');
    moment.tz.names().forEach(tz => {
        const option = document.createElement('option');
        option.value = tz;
        option.textContent = tz;
        timezoneSelect.appendChild(option);
    });

    // Try to set user's local timezone as default
    const userTimezone = moment.tz.guess();
    if (userTimezone) {
        timezoneSelect.value = userTimezone;
    }
    
    // Form submission
    document.getElementById('uploadForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        statusDiv.innerHTML = '<p>Processing file...</p>';
        
        const fileInput = document.getElementById('file');
        if (!fileInput.files.length) {
            alert('Please select a file');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('timezone', document.getElementById('timezone').value);
        
        try {
            statusDiv.innerHTML = '<p>Generating heatmap...</p>';
            
            const response = await fetch(`${API_URL}/api/generate-heatmap`, {
                method: 'POST',
                body: formData
            });

            // (!response.ok) {
            //     throw new Error('Network response was not ok')
            // }

            const data = await response.json();
            
            if (data.status === 'success') {
                const heatmapImg = document.getElementById('heatmap');
                heatmapImg.src = `data:image/png;base64,${data.image}`;
                heatmapImg.style.display = 'block';
                statusDiv.innerHTML = '<p style="color: green;">Heatmap generated successfully!</p>';
            } else {
                statusDiv.innerHTML = `<p style="color: red;">Error: ${data.message}</p>`;
            }
        } catch (error) {
            statusDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    });
});