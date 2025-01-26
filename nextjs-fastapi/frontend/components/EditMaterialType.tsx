"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { fetchMaterialTypes, MaterialTypeName} from '@/constants/data';

const EditMaterialType = ({ materialType, isOpen, onOpenChange, onSave}) => {
    const [editableMaterialType, setEditableMaterialType] = useState(materialType);
    const [MaterialTypes, setMaterialTypes] = useState([]);
    const mat = (materialType?.type_name)?.toString();
    console.log(mat)


    useEffect(() => {
        setEditableMaterialType(materialType);
    }, [materialType]);

    useEffect(() => {
        const fetchTypes = async () => {
            const types = await fetchMaterialTypes();
            setMaterialTypes(types);
        }
        fetchTypes();
    }, []);

    const handleChange = (field, value) => {
        setEditableMaterialType((prev) => ({ ...prev, [field]: value }));
    };

    const handleSave = async () => {

        try {

        // Send update request to backend
      const response = await fetch(`http://localhost:8000/update_mattype/${editableMaterialType.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({

        type_name: editableMaterialType.type_name
        }),
      });
        if (!response.ok) {
        console.log(response.body)
         const errorData = await response.json();
         console.error("Error updating material type:", errorData); // Log the error response from the backend
         throw new Error("Failed to update material type");
      }
        const updatedMaterialType = { ...editableMaterialType,
          type_name: editableMaterialType.type_name
         };
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
            label="Material Type Name"
            placeholder="Enter the Material Type's Name"
            variant="bordered"
            value={editableMaterialType?.type_name || ""}
            onChange={(e) => handleChange("type_name", e.target.value)}
          />
            </ModalBody>
            <ModalFooter>
              <Button color="danger" variant="flat" onPress={onOpenChange}>
                Cancel
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