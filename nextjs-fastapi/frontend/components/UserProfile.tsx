"use client";
import React from 'react'
import { useEffect, useState } from "react";
import { Button, useDisclosure, Input, Link} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { fetchUserTypes, UserTypeName } from '@/constants/data';

const UserProfile = ({ user }) => {
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
      const types = await fetchUserTypes();
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
        const updatedUser = { ...editableUser };
      } catch (error) {
        console.error("Error updating user:", error);
      }
    }


  return (
    <div className="flex items-center justify-center h-screen bg-black">
      <div className="w-full max-w-lg p-8 bg-neutral-900 text-white rounded-xl shadow-lg">
      <h1 className="text-2xl font-bold mb-4 text-center text-gray-100">User Profile</h1>
        
        {/* Add spacing between input fields */}
        <div className="space-y-4">
          <Input
            label="Username"
            placeholder="Enter username"
            variant="bordered"
            value={editableUser?.username || ""}
            onChange={(e) => handleChange("username", e.target.value)}
          />
          <Input
            label="Password"
            placeholder="Enter user password"
            variant="bordered"
            value={editableUser?.password || ""}
            onChange={(e) => handleChange("password", e.target.value)}
          />
          <Input
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            value={editableUser?.email || ""}
            onChange={(e) => handleChange("email", e.target.value)}
          />
      <div className="flex justify-end gap-4 mt-6">
        <Button color="primary" onPress={handleSave}>
          Save Changes
        </Button>
      </div>
    </div>
    </div>
    </div>
  );
};


export default UserProfile;
