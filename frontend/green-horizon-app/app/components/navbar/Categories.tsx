'use client';

import Container from "../Container";
import CategoryBox from "../CategoryBox";
import { usePathname, useSearchParams } from "next/navigation";
import { PiDiscoBall, PiMicrophoneStageLight } from "react-icons/pi";
import {  GiDualityMask } from "react-icons/gi";
import { LuCalendarHeart } from "react-icons/lu";
import { IoFastFoodOutline, IoGameControllerOutline } from "react-icons/io5";
import { MdOutlineHealthAndSafety, MdOutlineWorkOutline } from "react-icons/md";

export const categories = [

    {
        label: 'Music',
        icon: PiMicrophoneStageLight,
        description: 'Music venues'
    },
    {
        label: 'Nightlife',
        icon: PiDiscoBall,
        description: 'Nightlife venues'
    },
    {
        label: 'Performing & Visual Arts',
        icon: GiDualityMask,
        description: 'Theatric venues'
    },
    {
        label: 'Holidays',
        icon: LuCalendarHeart,
        description: 'Holiday venues'
    },
    {
        label: 'Health',
        icon: MdOutlineHealthAndSafety,
        description: 'Health venues'
    },
    {
        label: 'Hobbies',
        icon: IoGameControllerOutline,
        description: 'Hobby venues'
    },
    {
        label: 'Business',
        icon: MdOutlineWorkOutline,
        description: 'Business venues'
    },
    {
        label: 'Food & Drinks',
        icon: IoFastFoodOutline,
        description: 'Food & drink venues'
    },
]

const Categories = () => {
    const params = useSearchParams();
    const category = params?.get('category');
    const pathname = usePathname();
    
    const isMainPage = pathname =='/';

    if (!isMainPage) {
        return null;
    }
    return (
        <Container>
            <div className="
            pt-4
            flex
            flex-row
            items-center
            justify-between
            overflow-x-auto">
                {categories.map((item) => (
                    <CategoryBox
                    key={item.label}
                    label={item.label}
                    selected={category==item.label}
                    icon={item.icon}
                    />
                ))}
            </div>
        </Container>
    );
}

export default Categories;