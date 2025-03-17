"use client";
import React from 'react'
import { useEffect, useState } from "react";

import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button
} from "@heroui/react";

type DeletePopupTypes = {
  item: { id: number} | null;
  isOpen: boolean;
  onOpenChange: () => void;
  onDelete: (id: number) => void;
  itemType: string;
};

const DeletePopup: React.FC<DeletePopupTypes> = ({ item, isOpen, onOpenChange, onDelete, itemType}) => {
  const [errorMessage, setErrorMessage] = useState("");

  

  const handleDelete = async () => {
    if (!item) return;
    try {
      // send delete request to backend
      const response = await fetch(`http://localhost:8000/${itemType}/${item.id}` , {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) throw new Error("Failed to delete material");

      onDelete(item.id);
      onOpenChange();
    } catch (error) {

      // Extract "detail" if it exists
      const errorMessage = "Login failed. Please try again.";
      setErrorMessage(errorMessage);
      console.error("Error deleting material:", error);
    }
  };

  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop="opaque">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">
          Delete Item
        </ModalHeader>
        <ModalBody>
          Are you sure you want to delete this item? This action cannot be undone.
        </ModalBody>
        <ModalFooter>
          <Button color="danger" variant="flat" onPress={onOpenChange}>
            Close
          </Button>
          <Button color="primary" onPress={handleDelete}>
            Delete
          </Button>
                  {errorMessage && (
            <p className="text-red-500 bg-red-100 border border-red-400 text-sm mt-2 p-2 rounded">
        {errorMessage}
            </p>
        )}
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};
export default DeletePopup;