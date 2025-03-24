"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, Input, Tabs, Tab } from "@heroui/react";

import { fetchMaterialTypes } from '@/constants/data';


interface Material {
  id: number;
  material_type_id: number;
  mass: number;
  colour: string;
  totalDistance: number;
  shelf_id: number;
  name: string;
  weight: number;
  status: string;
  key: number;
  label: string;
  supplier_link: string | null;
  type_name: string;
}

interface OrderProps {
  material: Material | null;
  isOpen: boolean;
  onOpenChange: () => void;
  onSave: (updatedMaterial: Material) => void;
}



const Order: React.FC<OrderProps> = ({ material, isOpen, onOpenChange, onSave }) => {
  const [editableMaterial, setEditableMaterial] = useState<Material | null>(material);
  const [materialTypes, setMaterialTypes] = useState<{label: string}[]>([]);
  const [orderType, setOrderType] = useState("add");
  const mat = material?.material_type_id !== undefined ? materialTypes[material.material_type_id]?.label : "";



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

  const handleChange = (field: keyof Material, value: any) => {
    setEditableMaterial((prev) => (prev ? { ...prev, [field]: value } : null));
  };



  const handleSave = async (actionType: string) => {
    if (!editableMaterial) return;
    try {
        const endpoint = actionType === "add" ? 
        `http://localhost:8000/materials/replenish_mass/${editableMaterial.id}`
        : `http://localhost:8000/materials/consume_mass/${editableMaterial.id}`;
      // Send update request to backend
      const response = await fetch(endpoint, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            mass_change: parseFloat(editableMaterial.mass.toString()) // Make sure mass_change is passed correctly
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

