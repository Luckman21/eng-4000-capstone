"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { fetchMaterialTypes, MaterialTypeName } from '@/constants/data';

const EditUser = ({ user, isOpen, onOpenChange, onSave }) => {
  const [editableUser, setEditableUser] = useState(user);
  const [userTypes, setUserTypes] = useState([]);
  const mat = (user?.user_type_id)?.toString();
  console.log(mat)



  useEffect(() => {
    setEditableUser(user);
  }, [user]);

   // Fetch user types on component mount
  useEffect(() => {
    const fetchTypes = async () => {
      const types = await fetchMaterialTypes();
      setUserTypes(types);

    };
    fetchTypes();

  }, []);

  const handleChange = (field, value) => {
    setEditableUser((prev) => ({ ...prev, [field]: value }));
  };



  const handleSave = async () => {

    try {

      // Send update request to backend
      const response = await fetch(`http://localhost:8000/update_user/${editableUser.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({

        username: editableUser.username,
        password: editableUser.password,
        email: editableUser.email,
        user_type_id: editableUser.user_type_id,
        }),
      });
        if (!response.ok) {
        console.log(response.body)
         const errorData = await response.json();
         console.error("Error updating user:", errorData); // Log the error response from the backend
         throw new Error("Failed to update user");
      }
        const updatedMaterial = { ...editableUser };
        onSave(updatedMaterial); // Notify parent
        onOpenChange(); // Close the modal
      } catch (error) {
        console.error("Error updating user:", error);
      }
    }


  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop="opaque">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">Edit Material</ModalHeader>
        <ModalBody>
          <Input
            label="Username"
            placeholder="Enter username"
            variant="bordered"
            value={editableUser?.name || ""}
            onChange={(e) => handleChange("name", e.target.value)}
          />
          <Input
            label="Password"
            placeholder="Enter user password"
            variant="bordered"
            value={editableUser?.colour || ""}
            onChange={(e) => handleChange("colour", e.target.value)}
          />
          <Input
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            value={editableUser?.mass || ""}
            onChange={(e) => handleChange("mass", parseFloat(e.target.value))}
          />

          {/* Autocomplete for Material Type */}
          <Autocomplete
            label="User Type"
            placeholder="Select user type"
            defaultSelectedKey={mat}
            defaultItems={userTypes}
            onSelectionChange={(key) => handleChange("user_type_id", parseInt(key, 2))}
          >
             {userTypes.map((item) => (
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


export default EditUser;

