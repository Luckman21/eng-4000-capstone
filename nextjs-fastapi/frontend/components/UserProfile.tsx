"use client";
import React, { useState, useEffect } from "react";
import { Button, useDisclosure, Input, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Text } from "@heroui/react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import axios from "axios";

const UserProfile = ({ onSave }) => {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [editableUser, setEditableUser] = useState({
    username: "",
    email: "",
    password: "",
    id: "",
  });
  const [isPasswordModalOpen, setPasswordModalOpen] = useState(false); // State to control the password modal
  const [newPassword, setNewPassword] = useState(""); // State for new password
  const [confirmPassword, setConfirmPassword] = useState(""); // State for confirm password
  const [passwordError, setPasswordError] = useState(""); // State to track password match error

  useEffect(() => {
    fetch("http://127.0.0.1:8000/protected", {
      method: "GET",
      credentials: "include", // Ensures cookies are included in the request
    })
      .then((res) => res.json())
      .then((data) => setUser(data.user))
      .catch((err) => console.error(err));

  }, []);

  const handleChange = (field, value) => {
    setEditableUser((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      // Send update request to backend
      const response = await axios.put(`http://localhost:8000/update_user/${editableUser.id}`, {
        username: user.username,
        email: user.email,
      });

      if (response.status === 200) {
        console.log("User updated successfully");
        alert("Profile updated!");

        const { access_token } = response.data;
        if (access_token) {
          localStorage.setItem("access_token", access_token);
        }

        loadUserData();
        router.push("/inventory");
      }

      const updatedMaterial = { ...editableUser };
      onSave(updatedMaterial);

    } catch (error) {
      console.error("Failed to update user:", error);
    }
  };

  const handlePasswordModalClose = () => {
    setPasswordModalOpen(false); // Close password modal
    setPasswordError(""); // Reset the password error on close
  };

  const handlePasswordSave = async () => {
    // Check if new password and confirm password match
    if (newPassword !== confirmPassword) {
      setPasswordError("Passwords do not match");
      return;
    }

    try {
      const response = await axios.put(`http://localhost:8000/update_user/${editableUser.id}`, {
        password: newPassword, // Send only the password to the backend
      });

      if (response.status === 200) {
        console.log("Password updated successfully");
        // Optionally notify the user or refresh the state
        handlePasswordModalClose(); // Close the modal after saving
      }
    } catch (error) {
      console.error("Failed to update password:", error);
    }
  };
    console.log(user)
  return (
    <div className="flex items-center justify-center h-screen bg-black">
      <div className="w-full max-w-lg p-8 bg-neutral-900 text-white rounded-xl shadow-lg">
        <h1 className="text-2xl font-bold mb-4 text-center text-gray-100">User Profile</h1>
        <div className="space-y-4">
          <Input
            label="Username"
            placeholder="Enter username"
            variant="bordered"
            value={user?.username || ""}
            onChange={(e) => handleChange("username", e.target.value)}
          />
          <Input
            label="Email"
            placeholder="Enter user email"
            variant="bordered"
            value={user?.email || ""}
            onChange={(e) => handleChange("email", e.target.value)}
          />
          <div className="flex justify-between items-center gap-4 mt-6">
            <Button color="primary" onPress={() => setPasswordModalOpen(true)}>
              Update Password
            </Button>
            <Button color="primary" onPress={handleSave}>
              Save Changes
            </Button>
          </div>
        </div>
      </div>

      {/* Password Edit Modal */}
      <Modal isOpen={isPasswordModalOpen} onOpenChange={handlePasswordModalClose}>
        <ModalContent>
          <ModalHeader>Edit Password</ModalHeader>
          <ModalBody>
            <Input
              label="New Password"
              placeholder="Enter new password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <Input
              label="Confirm Password"
              placeholder="Confirm new password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            {passwordError && <div className="text-danger mt-2">{passwordError}</div>}
          </ModalBody>
          <ModalFooter>
            <Button color="danger" variant="flat" onPress={handlePasswordModalClose}>
              Close
            </Button>
            <Button color="primary" onPress={handlePasswordSave}>
              Save Changes
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </div>
  );
};

export default UserProfile;
