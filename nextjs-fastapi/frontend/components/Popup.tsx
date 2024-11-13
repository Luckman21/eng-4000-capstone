"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@nextui-org/react";


export const Popup = ({ material, isOpen, onOpenChange }) => {
    const [editableMaterial, setEditableMaterial] = useState(material);

    // Update local state when material prop changes
    React.useEffect(() => {
      setEditableMaterial(material);
    }, [material]);
  
    const handleChange = (field, value) => {
      setEditableMaterial((prev) => ({ ...prev, [field]: value }));
    };
  
    const handleSave = () => {
      if (onSave) {
        
      }
       // Close the modal after saving
    };
  
    return (
      <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop='opaque'>
        <ModalContent>
          <ModalHeader className="flex flex-col gap-1">Edit Material</ModalHeader>
          <ModalBody>
            <Input
              label="Name"
              placeholder="Enter material name"
              variant="bordered"
              value={editableMaterial?.name || ""}
              onChange={(e) => handleChange("name", e.target.value)}
            />
            <Input
              label="Colour"
              placeholder="Enter material colour"
              variant="bordered"
              value={editableMaterial?.colour || ""}
              onChange={(e) => handleChange("colour", e.target.value)}
            />
            <Input
              label="Weight (g)"
              placeholder="Enter material weight"
              type="number"
              variant="bordered"
              value={editableMaterial?.mass || ""}
              onChange={(e) => handleChange("mass", parseFloat(e.target.value))}
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
export default Popup;

