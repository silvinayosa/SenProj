
// Line Chart Data: Random CO2 Emissions for Daily Line Chart (for each city)
const dailyLineChartData = {
   

    labels: ["2022-11", "2022-12", "2023-01", "2023-02", "2023-03"],
    datasets: [{
        label: "Prediction",
        data: [  , , , , 420.4365605758441], // Align
        borderColor: 'rgb(255,0,0,1)',
        borderDash: [20, 30],
        pointBackgroundColor: "transparent"
    }, {
        label: "Ontario",
        data: [419.0000013805282, 420.3353944138966, 420.85891214403034, 420.8034878132765, 420.4365605758441, ,], //Default dataset
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        pointBackgroundColor: "transparent"
        
    }, {
        label: "British Columbia",
        data: [422.09394952602815, 421.55606281865664, 418.9886790425056, 414.38425851103233, 412.53910037532785, , ], //Default dataset
        backgroundColor: 'rgba(255, 165, 0, 0.2)', // Change the background color to orange
        borderColor: 'rgba(255, 165, 0, 1)', // Change the border color to orange
        pointBackgroundColor: "transparent"
    },{
        label: "Prediction2",
        data: [ , , , , 412.53910037532785], // Align
        borderColor: 'rgb(255,0,0,1)',
        borderDash: [20, 30],
        pointBackgroundColor: "transparent"
    }, 
    ],
    

};


const config1 ={
    type: 'line',
    data: dailyLineChartData,
    options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
            x: {
                type: 'category',  // Use 'category' instead of 'time' for string labels
                title: {
                    display: true,
                    text: 'Date'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'CO2 Emission (ppm)'
                },
                ticks:{
                    stepSize: 0.00025,
                }

            }
        },
        plugins:{
            title:{
                display: true,
                text: 'Co2 Analysis and Prediction'
            }
        }
    },
};


const graphChart = new Chart(
    document.getElementById('co2Predisction'),
    config1
);
