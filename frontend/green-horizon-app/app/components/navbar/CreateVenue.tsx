'use client';

const CreateVenue = () => {
    return (
        <div className="border-[1px] w-full md:w-auto py-2 rounded-full shadow-sm hover:shadow-md transition
                        cursor-pointer"> 
        
            <div className="flex flex-row items-center justify-between">
                <div className="text-sm font-semibold px-6">
                    Create Venue
                </div>
                {/* <div className="hidden sm:block text-sm font-semibold px-6 border-x-[1px] flex-1 text-center">
                    Prediction
                </div> */}

            </div>

        </div>
    );
}

export default CreateVenue;