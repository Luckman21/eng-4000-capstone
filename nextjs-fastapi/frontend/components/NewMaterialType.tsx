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

interface NewMaterialTypeOption {
  isOpen: boolean;
  onOpenChange: () => void;
  onAddMaterialType: (materialtype: MaterialType) => void;
  materialtypes: MaterialType[];
}

interface MaterialTypeOption {
  label: string;
  key: number;
}

export const NewMaterialType: React.FC<NewMaterialTypeOption> = ({ isOpen, onOpenChange, onAddMaterialType, materialtypes}) => {
    const [MaterialTypes, setMaterialTypes] = useState<MaterialTypeOption[]>([]);
    const [newMaterialType, setNewMaterialType] = useState({
        name: NaN
    });

    useEffect(() => {
        const fetchTypes = async () => {
            const types = await fetchMaterialTypes();
            setMaterialTypes(types);
        }
        fetchTypes();
    }, []);

    const handleChange = (field: keyof MaterialType, value: string) => {
        setNewMaterialType((prev) => ({ ...prev, [field]: value }));
    };


    const handleSave = async () => {
        try {
          const response = await fetch("http://localhost:8000/create_mattype", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newMaterialType),
          });
    
          if (!response.ok) throw new Error("Failed to add user");
          let createdMaterialType = await response.json();
    
         
          createdMaterialType = {
            ...createdMaterialType,
            id: createdMaterialType.id || materialtypes.length +1, 
        };
    
          onAddMaterialType(createdMaterialType);
          onOpenChange(); // Close the modal
    
        } catch (error) {
          console.error("Error saving material type:", error);
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
            <ModalHeader className="flex flex-col gap-1">Add New Material Type</ModalHeader>
            <ModalBody>
              {/* Autocomplete for Material Type */}
              <Input
                label="Material Type Name"
                placeholder="Enter the material type's name"
                variant="bordered"
                onChange={(e) =>  handleChange("type_name", e.target.value)}
              />
            </ModalBody>
            <ModalFooter>
              <Button color="danger" variant="flat" onPress={onOpenChange}>
                Close
              </Button>
              <Button color="primary" onPress={handleSave}>
                Add Material Type
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
    );
};
export default NewMaterialType;