'use client';

import styles from "@/app/CSS/PredictionModal.module.css"
import 'chart.js/auto';
import {Line, Bar, Doughnut} from "react-chartjs-2";
import "@/pages/analysis.css";

const PredictionModal = ({show, handleClose}) => {
    if (!show) {
        return null;
    }

    return (
        <div className={styles['modal-backdrop']}>
            <div className={styles.modal}>
                <button className={styles['close-button']} onClick={handleClose}>X</button>
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
                                    borderRadius: 1,
                                    },
                                            ],
                                }}
                                options={{
                                    responsive: true,
                                    maintainAspectRatio: false,
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
                    options={{
                        responsive: true,
                        maintainAspectRatio: false,
                    }}
                />
                </div>
            </div>
        </div> 
            </div>
        </div>
    );
}

export default PredictionModal;

