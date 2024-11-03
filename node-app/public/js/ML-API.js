//Mock data after prediction button is clicked for each city
var mockData = {
  "Quebec": {
    "LSTM": {
      "14": {
        "co2": [419.6575297941606, 409.7299041666667, 419.824341, 419.7805289008265, 422.181091, 420.14317416759775],
        "cost": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
      }
    },
    "RNN": {
      "14": {
        "co2": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
        "cost": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
      }
    }
  }
};

/*
//////////////////////////////////////////////////// 
//////////////////// LISTENERS ///////////////////// 
//////////////////////////////////////////////////// 
*/

// document.getElementById('email-form').addEventListener('submit', async function (event) {
//   event.preventDefault();

//   // Get form values
//   const city_name = document.getElementById('City-Choices').value;
//   const model_name = document.getElementById('Model-Types').value;
//   const days = document.getElementById('of-days').value;
//   const datetime = '2023-03-26';  // Use current date

//   // Validate inputs
//   if (!city_name || !model_name || !days || !datetime) {
//     alert("Please fill out all fields.");
//     return;
//   }

//   // Prepare the data to send
//   const data = { 
//     city_name,
//     model_name,
//     days,
//     datetime
//   };

//   try {
//     // Send the data to the API
//     const response = await fetch('http://127.0.0.1:5000/predict', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify(data)
//     });

//     // Parse the response
//     const result = await response.json();

//     if (response.ok) {
//       console.log(result);

//       // Assuming `result` contains your prediction data
//       addPrediction(result);  // Call your chart update function with the new prediction data

//       alert('Prediction Successful: :).');
//     } else {
//       alert('Error: ' + result.error);
//     }
//   } catch (error) {
//     console.error('Error:', error);
//     alert('Something went wrong!');
//   }
// });

/*
//////////////////////////////////////////////////// 
//////////////////// FUNCTIONS ///////////////////// 
//////////////////////////////////////////////////// 
*/

// Real prediction data
// function addPrediction(result) {
//   const dataCo2 = result.predictions.map(predictions => predictions.CO2Emission);
//   const labels = result.predictions.map(predictions => predictions.date);

//   // Clear the current labels and dataset data before pushing new values
//   graphChart.data.labels = ["2023-02-22","2023-02-24","2023-02-26","2023-03-01","2023-03-23","2023-03-24","2023-03-25"]; // Clear existing labels
//   //graphChart.data.datasets[0].data =  [, , , , ,420.14317416759800]; // Clear existing prediction data

//   console.log(labels)
//   console.log(dataCo2)

//   // Add the predicted data and labels
//   graphChart.data.labels.push(...labels);
//   graphChart.data.datasets[0].data.push(...dataCo2);  // Show prediction data
//   graphChart.update();  // Update the chart to show the prediction

//   console.log(graphChart.data.datasets[0].data)
//   console.log(graphChart.data.datasets[1].data)
// }


// New event listener for the prediction button linked with mock data function
document.getElementById('email-form').addEventListener('click', function () {
  const city_name = document.getElementById('City-Choices').value;
  const model_name = document.getElementById('Model-Types').value;
  const days = document.getElementById('of-days').value;

  addMockPrediction(city_name, model_name, days);
});

//Mock prediction data function
function addMockPrediction(city_name, model_name, days) {
  console.log(city_name, model_name, days);
}
