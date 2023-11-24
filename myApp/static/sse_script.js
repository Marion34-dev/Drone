document.addEventListener('DOMContentLoaded', function() {
    const dataContainer = document.getElementById('data-container');

    // Create an EventSource to establish an SSE connection
    const eventSource = new EventSource("/ap/receive_data/");

    // Event listener for handling SSE messages
    eventSource.onmessage = function(event) {
        const data = event.data;
        updateUI(data);
    };

    // Event listener for handling SSE errors
    eventSource.onerror = function(error) {
        console.error('SSE Error:', error);
        eventSource.close();
    };

    function updateUI(data) {
        const formattedData = data.data.trim();
        dataContainer.textContent = `Received Data: ${formattedData}`;
    }
});
