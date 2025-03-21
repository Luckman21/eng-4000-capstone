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
import { fetchUserTypes } from "@/constants/data";
import { User } from "@/types";

interface NewUserOptions {
  isOpen: boolean;
  onOpenChange: () => void;
  onAddUser: (users: User) => void;
  users: User[];
}

interface NewUserTemplate {
  key: string | number;
  label: string;
}


export const NewUser: React.FC<NewUserOptions> = ({ isOpen, onOpenChange, onAddUser, users }) => {
  const [userTypes, setUserTypes] = useState<NewUserTemplate[]>([]);
  const [newUser, setNewUser] = useState({
    username: NaN,         
    password:NaN,    
    email: NaN,           
    user_type_id: NaN,
  });

  // Fetch user types on component mount
  useEffect(() => {
    const fetchTypes = async () => {
      const types = await fetchUserTypes();
      setUserTypes(types);
    };
    fetchTypes();
  }, []);

  
  const handleChange = (field: keyof User, value: string | number) => {
    setNewUser((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      const response = await fetch("http://localhost:8000/users/create_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
      });

      if (!response.ok) throw new Error("Failed to add user");
      let createdUser = await response.json();

     
      createdUser = {
        ...createdUser,
        id: createdUser.id || users.length +1, 
    };

      onAddUser(createdUser);
      onOpenChange(); // Close the modal

    } catch (error) {
      console.error("Error saving user:", error);
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
            onChange={(e) => handleChange("username", e.target.value)}
          />
          <Input
            label="Password"
            placeholder="Enter user password"
            variant="bordered"
            onChange={(e) => handleChange("password", e.target.value)}
          />
          <Input
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            onChange={(e) => handleChange("email", e.target.value)}
          />
          {/* Autocomplete for User Type */}
          <Autocomplete
            label="User Type"
            placeholder="Select user type"
            defaultItems={userTypes}
            onSelectionChange={(key) => {
              if (key != null) {
                handleChange("user_type_id", key);
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
            Add User
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};
export default NewUser;