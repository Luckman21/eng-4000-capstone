"use client"
import React, { use, useEffect, useState } from 'react'
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerBody,
  DrawerFooter,
  Button,
  useDisclosure,
} from "@heroui/react";
import {MaterialCard} from "@/components";
import { MaterialCardType } from "@/types"

interface ShelfDetailsType {
  temperature_cel: number;
  humidity_pct: number;
}
interface ShelfDetailsProps {
  shelf_id: number;              
  isOpen: boolean;              
  onOpen: () => void;            
  onOpenChange: () => void;      
}

const ShelfDetails: React.FC<ShelfDetailsProps> = ({shelf_id, isOpen, onOpen, onOpenChange}) => {
  const [shelfDetails, setShelfDetails] = useState<ShelfDetailsType | null>(null);
  const [shelfMaterials, setShelfMaterials] = useState<MaterialCardType[]>([]);

  useEffect(() => { 
    async function fetchShelfDetails() {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/shelf_details/${shelf_id}`);
        const data = await res.json();
        console.log(data);
        setShelfDetails(data.shelf);
        setShelfMaterials(data.materials);
      } catch (error) {
        console.error("Failed to fetch shelf details:", error);
      }
    }
    fetchShelfDetails();
  }
  , [isOpen, shelf_id]);

  return (
    <Drawer isOpen={isOpen} onOpenChange={onOpenChange}>
      <DrawerContent>
        <DrawerBody>        
          <div>
            <h1 className="text-lg font-semibold mb-4 pb-4">Shelf {shelf_id} Details:</h1>
            <div className="grid grid-cols-1 gap-4">
                <p className="text-sm">Shelf Temperature: {shelfDetails?.temperature_cel}</p>
                <p className="text-sm">Shelf Humidity: {shelfDetails?.humidity_pct}</p>
            </div>
          </div>
          <div>
            <h1 className="text-lg font-semibold mb-4 pb-4">Materials in Shelf {shelf_id}:</h1>
            <div className="grid grid-cols-1 gap-4"> 
                {shelfMaterials?.map((material) => (
                <MaterialCard key={material.id} material={material} />
                ))}
            </div>
          
          </div>
        </DrawerBody>
      </DrawerContent>
    </Drawer>
  )
}


export default ShelfDetails
