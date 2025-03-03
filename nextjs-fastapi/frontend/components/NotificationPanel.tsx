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
import MaterialCard from './MaterialCard';

const NotificationPanel = ({ lowstock, isOpen, onOpen, onOpenChange}) => {
  const [lowStockMaterials, setLowStockMaterials] = useState();
  useEffect(() => {
    setLowStockMaterials(lowstock);
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
            <h1 className="text-lg font-semibold mb-4 pb-4">Low Stock Materials</h1> {/* Added margin-bottom */}
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