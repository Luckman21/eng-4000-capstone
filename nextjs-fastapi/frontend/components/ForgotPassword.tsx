"use client";
import React, { useEffect, useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Input,
  Button,
} from "@heroui/react";
import axios from "axios";

interface ForgotPasswordProps {
  user?: {username: string; email: string};
  isOpen: boolean;
  onOpenChange: () => void;
}

const ForgotPassword: React.FC<ForgotPasswordProps> = ({ user, isOpen, onOpenChange }) => {
  const [forgotEmail, setForgotEmail] = useState("");
  const [editableUser, setEditableUser] = useState(user);

  useEffect(() => {
      setEditableUser(user);
    }, [user]);

  const handleForgotPassword = async () => {
    try {
      // Send the email to the backend for the forgot password process
      const response = await axios.post(`/access_management/forgot_password`, {
        email: forgotEmail,
      });

      alert(response.data.message); // Show success message
      setForgotEmail(""); // Clear the email field
      onOpenChange(); // Close the modal
    } catch (error) {
      console.error("Failed to send forgot password email:", error);
      alert("Something went wrong. Please try again later.");
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
        <ModalHeader className="flex flex-col gap-1">Forgot Password</ModalHeader>
        <ModalBody>
          <div>
            <p className="mb-4">Enter your email to receive a temporary password:</p>
            <Input
              label="Email"
              placeholder="Enter your email"
              type="email"
              value={forgotEmail}
              onChange={(e) => setForgotEmail(e.target.value)}
              isRequired
            />
          </div>
        </ModalBody>
        <ModalFooter>
          <Button color="danger" variant="flat" onPress={onOpenChange}>
            Cancel
          </Button>
          <Button color="primary" onPress={handleForgotPassword}>
            Submit
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default ForgotPassword;
