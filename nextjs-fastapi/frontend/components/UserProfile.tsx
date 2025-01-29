"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";


const UserProfile = ({ user, isOpen, onOpenChange, onSave }) => {
  const [editableUser, setEditableUser] = useState(user);
  const [userTypes, setUserTypes] = useState([]);
  const mat = (user?.user_type_id)?.toString();
  console.log(mat)



  useEffect(() => {
    setEditableUser(user);
  }, [user]);


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
        const updatedUser = { ...editableUser };
        onSave(updatedUser); // Notify parent
        onOpenChange(); // Close the modal
      } catch (error) {
        console.error("Error updating user:", error);
      }
    }


  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop="opaque">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">Edit User</ModalHeader>
        <ModalBody>
          <Input
            label="Username"
            placeholder="Enter username"
            variant="bordered"
            value={editableUser?.username  || ""}
            onChange={(e) => handleChange("username", e.target.value)}
          />
          <Input
            label="Password"
            placeholder="Enter user password"
            variant="bordered"
            value={"*****"}
            onChange={(e) => handleChange("password", e.target.value)}
          />
          <Input
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            value={editableUser?.email  || ""}
            onChange={(e) => handleChange("email", e.target.value)}
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


export default UserProfile;
