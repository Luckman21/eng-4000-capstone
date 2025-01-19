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

export const NewUser = ({ isOpen, onOpenChange, onAddUser, users }) => {
  const [userTypes, setUserTypes] = useState([]);
  const [newUser, setNewUser] = useState({
    username: NaN,         
    password:NaN,    
    email: NaN,           
    user_type_id: NaN,
  });

  // Fetch material types on component mount
  useEffect(() => {
    const fetchTypes = async () => {
      const types = await fetchMaterialTypes();
      setUserTypes(types);
    };
    fetchTypes();
  }, []);

  // Update editableMaterial state on input change
  const handleChange = (field, value) => {
    setNewUser((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      const response = await fetch("http://localhost:8000/create_material", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
      });

      if (!response.ok) throw new Error("Failed to add material");
      let createdMaterial = await response.json();

     
      createdMaterial = {
        ...createdMaterial,
        id: createdMaterial.id || users.length +1, 
    };

      onAddUser(createdMaterial);
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
        <ModalHeader className="flex flex-col gap-1">Add New User</ModalHeader>
        <ModalBody>
          
        <Input
            label="Username"
            placeholder="Enter username"
            variant="bordered"
            onChange={(e) => handleChange("name", e.target.value)}
          />
          <Input
            label="Password"
            placeholder="Enter user password"
            variant="bordered"
            onChange={(e) => handleChange("colour", e.target.value)}
          />
          <Input
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            onChange={(e) => handleChange("mass", parseFloat(e.target.value))}
          />
          {/* Autocomplete for Material Type */}
          <Autocomplete
            label="User Type"
            placeholder="Select user type"
            defaultItems={userTypes}
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
            Add Material
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};
export default NewUser;