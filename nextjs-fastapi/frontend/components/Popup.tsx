"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@nextui-org/react";
import { Autocomplete, AutocompleteItem } from "@nextui-org/react";
import { MaterialTypeName } from '@/constants/data';

const Popup = ({ material, isOpen, onOpenChange, onSave }) => {
  const [materialTypes, setMaterialTypes] = useState([]);
  const [editableMaterial, setEditableMaterial] = useState(material);
  console.log(editableMaterial);

  // Update local state when material prop changes
  React.useEffect(() => {
    setEditableMaterial(material);
  }, [material]);

   // Fetch material types on component mount
  useEffect(() => {
    const fetchMaterialTypes = async () => {
      try {
        const res = await fetch("http://localhost:8000/material_types");
        const data = await res.json();

        // Transform fetched data to match AutocompleteItem structure
        const types = data.map((type) => ({
          label: type.type_name,
          key: type.id,
        }));

        setMaterialTypes(types);
      } catch (error) {
        console.error("Error fetching material types:", error);
      }
    };

    fetchMaterialTypes();
  }, []);

  const handleChange = (field, value) => {
    setEditableMaterial((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      // Send update request to backend
      const response = await fetch(`http://localhost:8000/update_material/${editableMaterial.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        mass: editableMaterial.mass,
        name: editableMaterial.name,
        colour: editableMaterial.colour

        }),
      });

      if (!response.ok) throw new Error("Failed to update material");

      const updatedMaterial = { ...editableMaterial };
      onSave(updatedMaterial); // Notify parent
      onOpenChange(); // Close the modal
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
            value={editableMaterial?.material_type_id ? MaterialTypeName(editableMaterial.material_type_id) ?? "" : ""}
            defaultItems={materialTypes}
            onSelectionChange={(key) => {
                handleChange("material_type_id", key);
              }
            }
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