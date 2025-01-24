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
} from "@nextui-org/react";

const NotificationPanel = ({isOpen, onOpen, onOpenChange}) => {
  const [lowStockMaterials, setLowStockMaterials] = useState([]);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/low_stock");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLowStockMaterials(data);
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => socket.close(); // Cleanup on component unmount
  }, []);

  
    return (
      <>
        <Drawer isOpen={isOpen} onOpenChange={onOpenChange}>
          <DrawerContent>
            {(onClose) => (
              <>
                <DrawerHeader className="flex flex-col gap-1">Alerts</DrawerHeader>
                <DrawerBody>
                <div>
                  <h1>Low Stock Materials</h1>
                  {lowStockMaterials.length === 0 ? (
                    <p>All materials are sufficiently stocked!</p>
                  ) : (
                    <ul>
                      {lowStockMaterials.map((material) => (
                        <li key={material.id}>
                          {material.name} - {material.mass}g remaining
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam pulvinar risus non
                    risus hendrerit venenatis. Pellentesque sit amet hendrerit risus, sed porttitor
                    quam.
                  </p>
                  <p>
                    Magna exercitation reprehenderit magna aute tempor cupidatat consequat elit dolor
                    adipisicing. Mollit dolor eiusmod sunt ex incididunt cillum quis. Velit duis sit
                    officia eiusmod Lorem aliqua enim laboris do dolor eiusmod. Et mollit incididunt
                    nisi consectetur esse laborum eiusmod pariatur proident Lorem eiusmod et. Culpa
                    deserunt nostrud ad veniam.
                  </p>
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