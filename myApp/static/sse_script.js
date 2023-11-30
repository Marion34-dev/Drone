/* document.addEventListener('DOMContentLoaded', function() {
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
 */





/* 
const latitudeSpan = document.getElementById('latitude');
const longitudeSpan = document.getElementById('longitude');

const eventSource = new EventSource('/ap/receive_data/');  // Replace with your Django endpoint

eventSource.onmessage = function (event) {
    const latestData = event.data;

    // Update the spans with the latest latitude and longitude
    updateCoordinates(latestData);
};

function updateCoordinates(data) {
    latitudeSpan.innerText = `Latitude: ${data.latitude.toFixed(6)}`;
    longitudeSpan.innerText = `Longitude: ${data.longitude.toFixed(6)}`;
}
  */

