"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@heroui/react";


const EditMaterialType = ({ materialType, isOpen, onOpenChange, onSave }) => {
  const [editableMaterialType, setEditableMaterialType] = useState(materialType);

  useEffect(() => {
    setEditableMaterialType(materialType);
  }, [materialType]);


  const handleChange = (field, value) => {
    setEditableMaterialType((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {

    try {

      // Send update request to backend
      const response = await fetch(`http://localhost:8000/update_material/${editableMaterialType.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        name: editableMaterialType.name,
        
        }),
      });
        if (!response.ok) {
        console.log(response.body)
         const errorData = await response.json();
         console.error("Error updating material type:", errorData); // Log the error response from the backend
         throw new Error("Failed to update material type");
      }
        const updatedMaterialType = { ...editableMaterialType };
        onSave(updatedMaterialType); // Notify parent
        onOpenChange(); // Close the modal
      } catch (error) {
        console.error("Error updating material type:", error);
      }
    }


  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop="opaque">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">Edit Material Type</ModalHeader>
        <ModalBody>
          <Input
            label="Name"
            placeholder="Enter material type name"
            variant="bordered"
            value={editableMaterialType?.name || ""}
            onChange={(e) => handleChange("name", e.target.value)}
          />
        </ModalBody>
        <ModalFooter>
          <Button color="danger" variant="flat" onPress={onOpenChange}>
            Close
          </Button>
          <Button color="primary" onPress={handleSave}>
            Save Changes
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};


export default EditMaterialType;

