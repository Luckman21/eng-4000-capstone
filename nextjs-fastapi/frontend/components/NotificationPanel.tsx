"use client";
import React, { useEffect, useState } from "react";
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerBody,
  DrawerFooter,
  Button,
} from "@heroui/react";
import { MaterialCard ,ShelfCard} from "@/components";
import { MaterialCardType, ShelftCardType } from "@/types";

interface NotificationPanelProps {
    lowstock: MaterialCardType[];
    shelfStat: ShelftCardType[];
    isOpen: boolean;              
    onOpen: () => void;            
    onOpenChange: () => void;      
  }
  lowstock: MaterialCardType[];
  shelfStat: ShelftCardType[];
  isOpen: boolean;
  onOpen: () => void;
  onOpenChange: () => void;
}

const NotificationPanel: React.FC<NotificationPanelProps> = ({ lowstock ,shelfStat, isOpen, onOpen, onOpenChange }) => {
const NotificationPanel: React.FC<NotificationPanelProps> = ({
  lowstock,
  shelfStat,
  isOpen,
  onOpen,
  onOpenChange,
}) => {
  const [lowStockMaterials, setLowStockMaterials] = useState<MaterialCardType[]>([]);

  const [shelfStatus, setShelfStatus] = useState<ShelftCardType[]>([]);
  useEffect(() => {
    setLowStockMaterials(lowstock);
    setShelfStatus(shelfStat);
  }, [lowstock]);


  
  
    return (
      <>
        <Drawer isOpen={isOpen} onOpenChange={onOpenChange}>
            <DrawerContent>
                {(onClose) => (
                <>
                    <DrawerHeader className="flex flex-col gap-1">Alerts</DrawerHeader>
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
  );
};

export default NotificationPanel;
