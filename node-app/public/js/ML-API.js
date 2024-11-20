/*
//////////////////////////////////////////////////// 
//////////////////// LISTENERS ///////////////////// 
//////////////////////////////////////////////////// 
*/

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
    const response = await fetch('http://127.0.0.1:5000/predict', {
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

      // alert('Prediction Successful: :).');
    } else {
      alert('Error: ' + result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Something went wrong!');
  }
});

document.getElementById('email-form').addEventListener('submit', async function (event) {
  event.preventDefault();

  // Get form values
  const city_name = document.getElementById('City-Choices2').value;
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
  console.log("Data sent",data)

  try {
    // Send the data to the API
    const response = await fetch('http://127.0.0.1:5000/predict-csv', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    // Parse the response
    const result = await response.json();

    if (response.ok) {
      console.log("Result for predict csv: ",result);

      // Assuming `result` contains your prediction data
      addPrediction2(result);  // Call your chart update function with the new prediction data

      // alert('Prediction Successful: :).');
    } else {
      alert('Error: ' + result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Something went wrong!');
  }
});
/*
//////////////////////////////////////////////////// 
//////////////////// FUNCTIONS ///////////////////// 
//////////////////////////////////////////////////// 
*/

// Real prediction data
function addPrediction(result) {
  const dataCo2 = result.predictions.map(predictions => predictions.CO2Emission);
  const labels = result.predictions.map(predictions => predictions.date);

  // Clear the current labels and dataset data before pushing new values
  graphChart.data.labels = ["2022-11", "2022-12", "2023-01", "2023-02", "2023-03"]; // Clear existing labels
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

function addPrediction2(result) {
  const dataCo2 = result.predictions.map(predictions => predictions.CO2);
  const labels = result.predictions.map(predictions => predictions.Date);

  // Clear the current labels and dataset data before pushing new values
  graphChart.data.labels = ["2022-11", "2022-12", "2023-01", "2023-02", "2023-03"]; // Clear existing labels
  //graphChart.data.datasets[0].data =  [, , , , ,420.14317416759800]; // Clear existing prediction data

  console.log(labels)
  console.log(dataCo2)

  // Add the predicted data and labels
  graphChart.data.labels.push(...labels);
  graphChart.data.datasets[3].data.push(...dataCo2);  // Show prediction data
  graphChart.update();  // Update the chart to show the prediction

  console.log(graphChart.data.datasets[0].data)
  console.log(graphChart.data.datasets[3].data)
}
