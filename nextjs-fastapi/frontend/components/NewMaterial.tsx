"use client";
import React, { useEffect, useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Input,
} from "@nextui-org/react";
import { Autocomplete, AutocompleteItem } from "@nextui-org/react";

export const NewMaterial = ({ isOpen, onOpenChange }) => {
  const [materialTypes, setMaterialTypes] = useState([]);
  const [newMaterial, setNewMaterial] = useState({
    colour: NaN,         
    name:NaN,    
    mass: NaN,           
    type_id: NaN, 
  });

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

  // Update editableMaterial state on input change
  const handleChange = (field, value) => {
    setNewMaterial((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      const response = await fetch("http://localhost:8000/create_material", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newMaterial),
      });

      if (!response.ok) throw new Error("Failed to add material");

      onOpenChange(); // Close the modal
    } catch (error) {
      console.error("Error saving material:", error);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onOpenChange={onOpenChange}
      placement="top-center"
      backdrop="opaque"
    >
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">Add New Material</ModalHeader>
        <ModalBody>
          <Input
            isRequired
            label="Name"
            placeholder="Enter material name"
            type="text"
            onChange={(e) => handleChange("name", e.target.value)}
          />
          <Input
            isRequired
            label="Colour"
            placeholder="Enter material colour"
            type="text"
            onChange={(e) => handleChange("colour", e.target.value)}
          />
          <Input
            isRequired
            label="Weight (g)"
            placeholder="Enter material weight"
            type="number"
            onChange={(e) => handleChange("mass", parseFloat(e.target.value))}
          />
          {/* Autocomplete for Material Type */}
          <Autocomplete
            isRequired
            label="Material Type"
            placeholder="Search material type"
            defaultItems={materialTypes}
            onSelectionChange={(key) => {
                handleChange("type_id", key);
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
            Add Material
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};
export default NewMaterial;