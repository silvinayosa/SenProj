document.getElementById('create-event-form').addEventListener('submit', async function (event) {
    event.preventDefault();
  
    // Get form values
    const event_name = document.getElementById('event-name').value;
    const event_type = document.getElementById('event-type').value;
    const guests = document.getElementById('guests').value;
    const start_date = document.getElementById('start-date').value;
    const end_date = document.getElementById('end-date').value;
    const province = document.getElementById('province').value;
    const budget = document.getElementById('budget').value;
  
    // Validate inputs
    if (!event_name || !event_type || !guests || !start_date || !end_date || !province || !budget) {
      alert("Please fill out all fields.");
      return;
    }
  
    // Prepare the data to send
    const data = {
      event_name,
      event_type,
      guests,
      start_date,
      end_date,
      province,
      budget
    };
    console.log(data);

    try {
      // Send the data to the Flask API
      const response = await fetch('http://127.0.0.1:5000/spea-2', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
  
      // Parse the response
      const result = await response.json();
  
      if (response.ok) {
        console.log(result);
  
        // Redirect to the results page with query parameters
        const query = new URLSearchParams(result).toString();
        window.location.href = `/main-web-page/recomendation-page1?${query}`;
      } else {
        alert('Error: ' + result.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong!');
    }
  });
  