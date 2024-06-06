import React from "react";
import 'chart.js/auto';
import { Line, Bar, Doughnut } from "react-chartjs-2";
import "./analysis.css";
import "../app/globals.css";


const Analytics: React.FC = () => {

    return (
        //analytics page
        <div className='App'> 
            <div className="descriptionBox">
                <div className="title">Analytics</div>
                <div className="description">
                    <h1>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
                        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
                    </h1>
                </div>
            </div>
            <div className="analysisBox">
                <div className='dataCard doughnutCard'>
                <Doughnut
                        datasetIdKey='id'
                        data={{
                            labels: ['Jun', 'Jul', 'Aug'],
                            datasets: [
                                {
                                label: 'Revenue',
                                data: [5, 6, 7],
                                backgroundColor: [
                                    "rgba(43, 63, 229, 0.8)",
                                    "rgba(250, 192, 19, 0.8)",
                                    "rgba(253, 135, 135, 0.8)",
                                ],
                                borderRadius: 10,
                
                            },
                            ],
                        }}
                    />
                </div>

                <div className='dataCard lineCard'>
                <Line
                    data={{
                        labels: ['Jun', 'Jul', 'Aug', 'Sep','Oct', 'Nov', 'Dec'],
                        datasets: [{
                                label: 'Revenue',
                                data: [5, 6, 7, 3, 9, 2, 7],
                            },
                            {
                                label: 'Sponsorship',
                                data: [3, 2, 11, 4, 3, 6, 7],   
                            }
                        ],
                    }}
                />
                </div>
            </div>
        </div>
    );
};

export default Analytics;
