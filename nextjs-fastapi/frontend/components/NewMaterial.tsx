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
} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { fetchMaterialTypes } from "@/constants/data";
import { MaterialType } from "@/types";


interface NewMaterialTypes {
  isOpen: boolean;
  onOpenChange: () => void;
  onAddMaterial: (material: MaterialType) => void;
  materials: MaterialType[];
}

interface MaterialTypeOption {
  key: string | number;
  label: string;
}

export const NewMaterial: React.FC<NewMaterialTypes> = ({ isOpen, onOpenChange, onAddMaterial, materials }) => {
  const [materialTypes, setMaterialTypes] = useState<MaterialTypeOption[]>([]);
  const [newMaterial, setNewMaterial] = useState({
    colour: NaN,         
    supplier_link:NaN,
    mass: NaN,           
    material_type_id: NaN,
    shelf_id: NaN
  });

  // Fetch material types on component mount
  useEffect(() => {
    const fetchTypes = async () => {
      const types = await fetchMaterialTypes();
      setMaterialTypes(types);
    };
    fetchTypes();
  }, []);

  // Update editableMaterial state on input change
  const handleChange = (field: string | number | null, value: string | number) => {
    if (field === null) return;
    setNewMaterial((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      const response = await fetch(`/materials/create_material`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newMaterial),
      });

      if (!response.ok) throw new Error("Failed to add material");
      let createdMaterial = await response.json();

     
      createdMaterial = {
        ...createdMaterial,
        id: createdMaterial.id || materials.length +1, 
    };

      onAddMaterial(createdMaterial);
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
            label="Colour"
            placeholder="Enter material colour"
            type="text"
            onChange={(e) => handleChange("colour", e.target.value)}
          />
          <Input
            isRequired
            label="Supplier Link"
            placeholder="Enter material supplier link"
            type="text"
            onChange={(e) => handleChange("supplier_link", e.target.value)}
          />
          <Input
            isRequired
            label="Weight (g)"
            placeholder="Enter material weight"
            type="number"
            onChange={(e) => handleChange("mass", parseFloat(e.target.value))}
          />
           <Input

            label="Shelf"
            placeholder="Enter shelf number"
            type="number"
            onChange={(e) => handleChange("shelf_id", parseFloat(e.target.value))}
          />
          {/* Autocomplete for Material Type */}
          <Autocomplete
            isRequired
            label="Material Type"
            placeholder="Search material type"
            defaultItems={materialTypes}
            onSelectionChange={(key) => {
              if (key != null) {
                handleChange("material_type_id", key);
              }
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
