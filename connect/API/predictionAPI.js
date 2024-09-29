// Predction API 
document.getElementById('email-form').addEventListener('submit', async function (event) {
  event.preventDefault();

  // Get form values
  const city_name = document.getElementById('City-Choices').value;
  const model_name = document.getElementById('Model-Types').value;
  const days = document.getElementById('of-days').value;
  const datetime = '2023-03-26';  // Use current date

  // Validate inputs
  if (!city_name || !model_name || !days || !datetime) {
    alert("Please fill out all fields.");
    return;
  }

  // Prepare the data to send
  const data = { 
    city_name,
    model_name,
    days,
    datetime
  };

  try {
    // Send the data to the API
    const response = await fetch('http://127.0.0.1:8080/predict', {
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

      // Assuming `result` contains your prediction data
      addPrediction(result);  // Call your chart update function with the new prediction data

      alert('Prediction Successful: :).');
    } else {
      alert('Error: ' + result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Something went wrong!');
  }
});

// Fetch data API
document.getElementById('City-Choices').addEventListener('change', function () {
  const selectedCity = this.value; // Change this to the desired city name
  dailyLineChartData.datasets[1].label = selectedCity;

  fetch(`http://127.0.0.1:5000/api/data/${selectedCity}`)
      .then(response => {
          if (!response.ok) {
              throw new Error('City not found');
          }
          return response.json();
      })
      .then(data => {
          addValues(data);
          // Log the actual data to the console
          console.log('Data retrieved:', data);
      })
      .catch(error => console.error('Error fetching data:', error));



});

//Adding values function
function addValues(result) {
  const co2Values = result.map(entry => entry.CO2);
  const labels = result.map(entry => entry.date);

  //console.log(labels);
  //console.log(co2Value);

  
  graphChart.data.datasets[1].data = co2Values;  // Update the bar chart data
  graphChart.data.labels = labels;
  graphChart.data.datasets[0].data =  [, , , , ,co2Values[5]];

  graphChart.update();  // Refresh the chart with new data

}

//Function to Add Prediction Data on Button Click
function addPrediction(result) {
  const dataCo2 = result.predictions.map(predictions => predictions.CO2Emission);
  const labels = result.predictions.map(predictions => predictions.date);

  // Clear the current labels and dataset data before pushing new values
  graphChart.data.labels = ["2023-02-22","2023-02-24","2023-02-26","2023-03-01","2023-03-23","2023-03-24","2023-03-25"]; // Clear existing labels
  //graphChart.data.datasets[0].data =  [, , , , ,420.14317416759800]; // Clear existing prediction data

  console.log(labels)
  console.log(dataCo2)

  // Add the predicted data and labels
  graphChart.data.labels.push(...labels);
  graphChart.data.datasets[0].data.push(...dataCo2);  // Show prediction data
  graphChart.update();  // Update the chart to show the prediction
  
  console.log(graphChart.data.datasets[0].data)
  console.log(graphChart.data.datasets[1].data)
}