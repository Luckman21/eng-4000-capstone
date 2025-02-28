"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, Input, Tabs, Tab } from "@heroui/react";

import { fetchMaterialTypes } from '@/constants/data';

const Order = ({ material, isOpen, onOpenChange, onSave }) => {
  const [editableMaterial, setEditableMaterial] = useState(material);
  const [materialTypes, setMaterialTypes] = useState([]);
  const [orderType, setOrderType] = useState("add");
  const mat = (materialTypes[material?.material_type_id]?.label);



  useEffect(() => {
    setEditableMaterial(material);
  }, [material]);

   // Fetch material types on component mount
  useEffect(() => {
    const fetchTypes = async () => {
      const types = await fetchMaterialTypes();
      setMaterialTypes(types);

    };
    fetchTypes();

  }, []);

  const handleChange = (field, value) => {
    setEditableMaterial((prev) => ({ ...prev, [field]: value }));
  };



  const handleSave = async (actionType) => {

    try {
        const endpoint = actionType === "add" ? 
        `http://localhost:8000/replenish_mass/${editableMaterial.id}`
        : `http://localhost:8000/consume_mass/${editableMaterial.id}`;
      // Send update request to backend
      const response = await fetch(endpoint, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            mass_change: parseFloat(editableMaterial.mass) // Make sure mass_change is passed correctly
        }),
      });
        if (!response.ok) {
        console.log(response.body)
         const errorData = await response.json();
         console.error("Error updating material:", errorData); // Log the error response from the backend
         throw new Error("Failed to update material");
      }
        const updatedMaterial = { ...editableMaterial };
        onSave(updatedMaterial); // Notify parent
        onOpenChange(); // Close the modal
      } catch (error) {
        console.error("Error updating material:", error);
      }
    }
    


  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop="opaque">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">Add/Remove Material</ModalHeader>
        <ModalBody>
            {/* Material Type Tabs */}
          <Tabs
            fullWidth
            selectedKey={orderType}
            onSelectionChange={(key) => setOrderType(key.toString())}
            color='primary'
          >
            <Tab key="add" title= "Add Mass" ></Tab>
            <Tab key="remove" title="Remove Mass"></Tab>
          </Tabs>
          
          <Input
            isDisabled
            label="Colour"
            placeholder="Material colour"
            variant="bordered"
            value={editableMaterial?.colour || ""}
          />
            <Input
              isDisabled
              label="Material Type"
              placeholder="Material type"
              variant="bordered"
              value={mat}
            
            />
          <Input
            label="Weight (g)"
            placeholder="Enter material weight"
            type="number"
            variant="bordered"
           
            onChange={(e) => handleChange("mass", parseFloat(e.target.value))}
          />
            

        </ModalBody>
        <ModalFooter>
          <Button color="danger" variant="flat" onPress={onOpenChange}>
            Close
          </Button>
          <Button color="primary" onPress={() => handleSave(orderType)}>
            Update Material
          </Button>

        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};


export default Order;

