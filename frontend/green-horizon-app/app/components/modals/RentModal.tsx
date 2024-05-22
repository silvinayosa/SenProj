'use client';

import useRentModal from "@/app/hooks/useRentModal";
import Modal from "./Modal"

const RentModal = () => {
    const rentModal = useRentModal();
    return (
        <Modal
            isOpen={rentModal.isOpen}
            onClose={rentModal.onClose}
            //onSubmit={()=>()}
            actionLabel="Submit"
            title="My Green Venue"
        />
    )
}

export default RentModal;