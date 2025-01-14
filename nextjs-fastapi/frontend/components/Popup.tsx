"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@nextui-org/react";
import { Autocomplete, AutocompleteItem } from "@nextui-org/react";
import { fetchMaterialTypes, MaterialTypeName } from '@/constants/data';

const Popup = ({ material, isOpen, onOpenChange, onSave }) => {
  const [editableMaterial, setEditableMaterial] = useState(material);
  const [materialTypes, setMaterialTypes] = useState([]);
  const mat = (material?.material_type_id)?.toString();
  console.log(mat)
 
  

  useEffect(() => {
    setEditableMaterial(material);
  }, [material]);

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
  
  
  
  const handleSave = async () => {
    const updatedMaterial = {
      mass: editableMaterial.mass,
      name: editableMaterial.name,
      colour: editableMaterial.colour,
      material_type_id: editableMaterial.material_type_id,
    };
  
    console.log("Request payload:", JSON.stringify(updatedMaterial, null, 2));
  
    try {
      const response = await fetch(`http://localhost:8000/update_material/${editableMaterial.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedMaterial),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Failed to update material: ${errorData.detail}`);
      }
  
      onSave(updatedMaterial); // Notify parent
      onOpenChange(); // Close modal
    } catch (error) {
      console.error("Error updating material:", error);
    }
  };
  
    

  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop="opaque">
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
          
          <Autocomplete
            label="Material Type"
            placeholder="Search material type"
            defaultSelectedKey={mat}
            defaultItems={materialTypes}
            onSelectionChange={(key) => handleChange("material_type_id", parseInt(key, 10))}
          >
            {(item) => (

            <AutocompleteItem key={item.key} >
            {item.label}
          </AutocompleteItem>
            )}
          </Autocomplete>
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