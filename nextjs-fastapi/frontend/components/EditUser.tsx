"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Checkbox, Input, Link} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { fetchUserTypes, UserTypeName } from '@/constants/data';

type User = {
  id: number;
  username: string;
  email: string;
  user_type_id: number;
};

type UserWithRole = {
  id: number;
  username: string;
  email: string;
  role: string;
  password: string;
  user_type_id: number;
};

type UserType = { 
  key: string | number;
  label: string;
}

type EditUserTypes = {
  user: UserWithRole;
  isOpen: boolean;
  onOpenChange: () => void;
  onSave: (user: UserWithRole) => void;
};




const EditUser: React.FC<EditUserTypes> = ({ user, isOpen, onOpenChange, onSave }) => {
  const [editableUser, setEditableUser] = useState<UserWithRole>(user);
  const [userTypes, setUserTypes] = useState<UserType[]>([]);
  const mat = (user?.user_type_id)?.toString();
  console.log(mat)



  useEffect(() => {
    setEditableUser(user);
  }, [user]);

   // Fetch user types on component mount
  useEffect(() => {
    const fetchTypes = async () => {
      const types = await fetchUserTypes();
      setUserTypes(types);

    };
    fetchTypes();

  }, []);

  const handleChange = (field: keyof User, value: string) => {
    setEditableUser((prev) => ({ ...prev, [field]: value }));
  };



  const handleSave = async () => {

    try {

      // Send update request to backend
      const response = await fetch(`http://localhost:8000/users/update_user/${editableUser.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({

        username: editableUser.username,
        password: NaN,
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
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            value={editableUser?.email  || ""}
            onChange={(e) => handleChange("email", e.target.value)}
          />

          {/* Autocomplete for User Type */}
          <Autocomplete
            label="User Type"
            placeholder="Select user type"
            defaultSelectedKey={mat}
            defaultItems={userTypes}
            onSelectionChange={(key) => {
              if (key != null) {
                handleChange("user_type_id", key.toString());
              }
            }}
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

