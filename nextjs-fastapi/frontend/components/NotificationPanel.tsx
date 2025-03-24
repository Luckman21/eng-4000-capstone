"use client"
import React, { useEffect, useState } from 'react'
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerBody,
  DrawerFooter,
  Button,
  useDisclosure,
} from "@heroui/react";
import {MaterialCard,ShelfCard} from "@/components";
import { MaterialCardType, ShelftCardType } from "@/types";
interface NotificationPanelProps {
    lowstock: MaterialCardType[];
    shelfStat: ShelftCardType[];
    isOpen: boolean;              
    onOpen: () => void;            
    onOpenChange: () => void;      
  }

const NotificationPanel: React.FC<NotificationPanelProps> = ({ lowstock ,shelfStat, isOpen, onOpen, onOpenChange }) => {
  const [lowStockMaterials, setLowStockMaterials] = useState<MaterialCardType[]>([]);
  const [shelfStatus, setShelfStatus] = useState<ShelftCardType[]>([]);
  useEffect(() => {
    setLowStockMaterials(lowstock);
    setShelfStatus(shelfStat);
  }, [lowstock]);
  useEffect(() => {
    const sortedShelves = [...shelfStat].sort((a, b) => a.id - b.id);
    setShelfStatus(sortedShelves);
  }, [lowstock, shelfStat]);

  const [scaleActive, setScaleActive] = useState<boolean | null>(null);
  const [dhtActive, setDhtActive] = useState<boolean | null>(null);

    // Fetch service status
  useEffect(() => {
    async function fetchServiceStatus() {
      try {
        const res = await fetch("http://localhost:8000/mqtt-status");  // Update to match your API route
        const data = await res.json();
        setScaleActive(data.dht_connection);
        setDhtActive(data.scale_connection);
      } catch (error) {
        console.error("Failed to fetch service status:", error);
        setScaleActive(false);
        setDhtActive(false);
      }
    }
    fetchServiceStatus();
  }, []);

    return (
      <>
        <Drawer isOpen={isOpen} onOpenChange={onOpenChange}>
            <DrawerContent>
                {(onClose) => (
                <>
                    <DrawerHeader className="flex flex-col gap-1">Alerts</DrawerHeader>

                    {/* Service Status Alerts */}
                    <div className="px-4 pb-4">
                        {scaleActive === false && (
                            <div className="bg-red-500 text-white p-2 rounded-md mb-2">
                                ⚠️ Scale service is down!
                            </div>
                            )}
                        {dhtActive === false && (
                        <div className="bg-red-500 text-white p-2 rounded-md mb-2">
                            ⚠️ DHT-11 service is down!
                        </div>
                        )}
                    </div>

                    <DrawerBody>
                    <div>
                        <h1 className="text-lg font-semibold mb-4 pb-4">Low Stock Materials</h1>
                        {lowStockMaterials.length === 0 ? (
                        <p>All materials are sufficiently stocked!</p>
                        ) : (
                        <div className="grid grid-cols-1 gap-4"> 
                            {lowStockMaterials.map((material) => (
                            <MaterialCard key={material.id} material={material} />
                            ))}
                        </div>
                        )}
                    </div>
                    <div>
                        <h1 className="text-lg font-semibold mb-4 pb-4">Shelf Status</h1> 
                        {shelfStatus.length === 0 ? (
                        <p>All Shelves operating at optimal conidtions!</p>
                        ) : (
                        <div className="grid grid-cols-1 gap-4"> 
                            {shelfStatus.map((shelf) => (
                            <ShelfCard key={shelf.id} shelf={shelf} />
                            ))}
                        </div>
                        )}
                    </div>
                    </DrawerBody>
                    <DrawerFooter>
                    <Button color="danger" variant="light" onPress={onClose}>
                        Close
                    </Button>
                    </DrawerFooter>
                </>
                )}
            </DrawerContent>
        </Drawer>

      </>
    );
  }
  

export default NotificationPanel