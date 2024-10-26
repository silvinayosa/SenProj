

/*
//////////////////////////////////////////////////// 
//////////////////// LISTENERS ///////////////////// 
//////////////////////////////////////////////////// 
*/

// Cost fetch data
document.getElementById('City-Choices').addEventListener('change', function () {
    const selectedCitys = this.value;

    fetch(`http://127.0.0.1:5000/api/datacost/${selectedCitys}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('City not found');
            }
            return response.json();
        })
        .then(data => {
            addValuesCost(data);
            console.log('Data retrieved:', data);
        })
        .catch(error => console.error('Error fetching data:', error));
});

// Co2 fetch data
document.getElementById('City-Choices').addEventListener('change', function () {
    const selectedCity = this.value; // Change this to the desired city name
    dailyLineChartData.datasets[1].label = selectedCity;
  
    fetch(`http://127.0.0.1:5000/api/dataco2/${selectedCity}`)
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
  
/*
//////////////////////////////////////////////////// 
//////////////////// FUNCTIONS ///////////////////// 
//////////////////////////////////////////////////// 
*/  

// Add Cost data
function addValuesCost(result) 
{
    // Extract the 'price' field from each entry
    const priceRange = result.map(entry => entry.price); 
    console.log(priceRange);

    PieChartDataCost.labels = priceRange;

    // Assuming you want to use the percentages too, here's how you can extract them:
    const percentage = result.map(entry => entry.percentage);
    PieChartDataCost.datasets[0].data = percentage;

    costgraphChart.update();
}

// Add co2 data
function addValues(result)
{
    const co2Values = result.map(entry => entry.CO2);
    const labels = result.map(entry => entry.date);
  
    //console.log(labels);
    //console.log(co2Value);
  
    
    graphChart.data.datasets[1].data = co2Values;  // Update the bar chart data
    graphChart.data.labels = labels;
    graphChart.data.datasets[0].data =  [, , , , ,co2Values[5]];
  
    graphChart.update();  // Refresh the chart with new data
  
  }