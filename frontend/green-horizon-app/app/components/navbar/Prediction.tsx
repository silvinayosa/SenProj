'use client'; 

import { useState } from "react";
import PredictionModal from "../modals/PredictionModal";

// interface PredictionProps {
//     onClick: () => </PredictionModal> ;
// }

const Prediction = () => {

    const [showModal, setShowModal] = useState(false);

    const handleOpenModal = () => {
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    return(
        <div className="border-[1px] w-full md:w-auto py-2 rounded-full shadow-sm hover:shadow-md transition
        cursor-pointer">
            <div className="flex flex-row items-center justify-between">
                <div className="text-sm font-semibold px-6" onClick={handleOpenModal}>
                        Prediction
                </div>
            </div>
            {showModal && (
                <PredictionModal show={showModal} handleClose={handleCloseModal} />
            )}
        </div>
    );
};

export default Prediction;