"use client";
import React from 'react'
import { useEffect, useState } from "react";
import { Button, useDisclosure, Input, Link} from "@heroui/react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { fetchUserTypes, UserTypeName } from '@/constants/data';
import { jwtDecode } from "jwt-decode";
import axios from "axios";

const UserProfile = (onSave) => {
  const [user, setUser] = useState(null);
  const [editableUser, setEditableUser] = useState({
    username: "",
    email: "",
    password: "",
    id: "",
  });




  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decoded = jwtDecode(token); // Decode JWT
        setUser(decoded); // Store user data
        setEditableUser({
          username: decoded.username,
          email: decoded.email, // Default to empty if not in token
          id: decoded.id,
          password: "", // Leave password blank for security
        });
      } catch (err) {
        console.error("Failed to decode token:", err);
      }
    }
  }, []);

  const handleChange = (field, value) => {
    setEditableUser((prev) => ({ ...prev, [field]: value }));
  };



  const handleSave = async () => {

    try {

      // Send update request to backend
      const response = await axios.put(`http://localhost:8000/update_user/${editableUser.id}`, {
        username: editableUser.username,
        email: editableUser.email,
        password: editableUser.password // Send only if not empty
      });

      if (response.status === 200) {
        console.log("User updated successfully");
        alert("Profile updated!");
      }
      const updatedMaterial = { ...editableUser };
      onSave(updatedMaterial);

    } catch (error) {
      console.error("Failed to update user:", error);
    }
  };


  return (
    <div className="flex items-center justify-center h-screen bg-black">
      <div className="w-full max-w-lg p-8 bg-neutral-900 text-white rounded-xl shadow-lg">
      <h1 className="text-2xl font-bold mb-4 text-center text-gray-100">User Profile</h1>
        <div className="space-y-4">
          <Input
            label="Username"
            placeholder="Enter username"
            variant="bordered"
            value={editableUser?.username || ""}
            onChange={(e) => handleChange("username", e.target.value)}
          />
          <Input
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            value={editableUser?.email || ""}
            onChange={(e) => handleChange("email", e.target.value)}
          />
      <div className="flex justify-between items-center gap-4 mt-6">
            <Button color="primary">
              Update Password
            </Button>
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
