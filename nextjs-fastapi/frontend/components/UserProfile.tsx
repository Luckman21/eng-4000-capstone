"use client";
import React, { useState, useEffect } from "react";
import { Button, useDisclosure, Input, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Alert } from "@heroui/react";
import { useRouter } from "next/navigation";
import { jwtDecode, JwtPayload } from "jwt-decode";
import axios from "axios";

interface UserProfileProps {
  onSave: (updatedUser: { username: string; email: string; id: string }) => void;
}


interface UserInfo {
  username: string;
  email: string;
  id: string;
}


const UserProfile: React.FC<UserProfileProps> = ({ onSave }) => {
  const router = useRouter();
  const [user, setUser] = useState<UserInfo | null>(null);
  const [editableUser, setEditableUser] = useState<UserInfo>({
    username: "",
    email: "",
    id: "",
  });
  const [isPasswordModalOpen, setPasswordModalOpen] = useState(false); // State to control the password modal
  const [newPassword, setNewPassword] = useState(""); // State for new password
  const [confirmPassword, setConfirmPassword] = useState(""); // State for confirm password
  const [passwordError, setPasswordError] = useState(""); // State to track password match error
  const [alertFlag, setAlertFlag] = useState(false);

  useEffect(() => {
    fetch(`/access_management/protected`, {
      method: "GET",
      credentials: "include", // Ensures cookies are included in the request
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.user) {
          setUser(data.user);
          setEditableUser({
            username: data.user.username,
            email: data.user.email,
            id: data.user.id,
          });
        }
      })
      .catch((err) => console.error(err));
      
  }, []);

  const handleChange = (field: keyof UserInfo, value: string) => {
    setEditableUser((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      // Send update request to backend
      const response = await axios.put(`/users/update_user/${editableUser.id}`, {
        username: editableUser.username,
        email: editableUser.email,
      });

      if (response.status === 200) {
        console.log("User updated successfully");
        setAlertFlag(true);
        setTimeout(() => {
          setAlertFlag(false);
          router.push("/inventory");
        }
        , 1500);

        
        //router.push("/inventory");
      }

      const updatedUser = { ...editableUser };
      onSave(updatedUser);

    } catch (error) {
      console.error("Failed to update user:", error);
    }
  };

  const handlePasswordModalClose = () => {
    setPasswordModalOpen(false);
    setPasswordError("");
  };

  const handlePasswordSave = async () => {
    if (newPassword !== confirmPassword) {
      setPasswordError("Passwords do not match");
      return;
    }

    try {
      if (!user) return;
      const response = await axios.put(`/users/update_user/${user.id}`, {
        password: newPassword,
      });

      if (response.status === 200) {
        console.log("Password updated successfully");
        handlePasswordModalClose();
      }
    } catch (error) {
      console.error("Failed to update password:", error);
    }
  };

  return (

  
    <div className="flex items-center justify-center h-screen bg-black">
      
      <div className="w-full max-w-lg p-8  text-white rounded-xl shadow-lg">
      {alertFlag && (
        <Alert color="success" onClose={() => setAlertFlag(false)}>
          User updated successfully
        </Alert>
      )}
        <h1 className="text-2xl font-bold mb-4 text-center text-gray-100">User Profile</h1>
        <div className="space-y-4">
          <Input
            label="Username"
            placeholder="Enter username"
            variant="bordered"
            className="py-2"
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
          <div className="flex justify-between items-center gap-4 mt-6 py-2">
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
              
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <Input
              label="Confirm Password"
              placeholder="Confirm new password"
              type="password"
              
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
