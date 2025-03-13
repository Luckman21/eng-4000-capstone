"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { fetchMaterialTypes, MaterialTypeName } from '@/constants/data';
import { MaterialType } from '@/types';

interface NewMaterials {
  isOpen: boolean;
  onOpenChange: () => void;
  onSave: (material: MaterialType) => void;
  material: MaterialType;
}

interface MaterialOption {
  key: string | number;
  label: string;
}

const Popup: React.FC<NewMaterials> = ({ material, isOpen, onOpenChange, onSave }) => {
  const [editableMaterial, setEditableMaterial] = useState(material);
  const [materialTypes, setMaterialTypes] = useState<MaterialOption[]>([]);
  const mat = (material?.material_type_id)?.toString();



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

  const handleChange = (field: keyof MaterialType, value: string | number) => {
    setEditableMaterial((prev) => ({ ...prev, [field]: value }));
  };



  const handleSave = async () => {

    try {

      // Send update request to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/update_material/${editableMaterial.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({

        mass: editableMaterial.mass,
        supplier_link: editableMaterial.supplier_link,
        material_type_id: editableMaterial.material_type_id,
        colour: editableMaterial.colour,
        shelf_id: editableMaterial.shelf_id
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
        <ModalHeader className="flex flex-col gap-1">Edit Material</ModalHeader>
        <ModalBody>
          <Input
            label="Supplier Link"
            placeholder="Enter material supplier link"
            variant="bordered"
            value={editableMaterial?.supplier_link || ""}
            onChange={(e) => handleChange("supplier_link", e.target.value)}
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
            value={editableMaterial?.mass?.toString() ?? ""}
            onChange={(e) => handleChange("mass", parseFloat(e.target.value))}
          />
            <Input
            label="Shelf"
            placeholder="Enter shelf number"
            type="number"
            variant="bordered"
            value={editableMaterial?.shelf_id?.toString() ?? ""}
            onChange={(e) => handleChange("shelf_id", parseFloat(e.target.value))}
          />

          {/* Autocomplete for Material Type */}
          <Autocomplete
            label="Material Type"
            placeholder="Search material type"
            defaultSelectedKey={mat !== undefined ? String(mat) : undefined}
            defaultItems={materialTypes}
            onSelectionChange={(key) => {
              if (key === null) return;
              handleChange("material_type_id", parseInt(key as string, 10))}
            }
          >
             {materialTypes.map((item) => (
            <AutocompleteItem key={item.key} value={item.key}>
                {item.label}
            </AutocompleteItem>
           ))}
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

