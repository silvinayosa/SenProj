import { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export default function Home() {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axios.get('http://localhost:5001/process-data');
                const data = response.data;
                setChartData({
                    labels: data.dates,
                    datasets: [
                        {
                            label: 'Actual CO2 Emissions',
                            data: data.actual_co2,
                            borderColor: 'blue',
                            fill: false,
                        },
                        {
                            label: 'RNN Predictions',
                            data: data.rnn_predictions,
                            borderColor: 'orange',
                            fill: false,
                        },
                        {
                            label: 'LSTM Predictions',
                            data: data.lstm_predictions,
                            borderColor: 'green',
                            fill: false,
                        }
                    ]
                });
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        fetchData();
    }, []);

    return (
        <div>
            <h1>CO2 Emissions Predictions</h1>
            {chartData ? <Line data={chartData} /> : <p>Loading data...</p>}
        </div>
    );
}