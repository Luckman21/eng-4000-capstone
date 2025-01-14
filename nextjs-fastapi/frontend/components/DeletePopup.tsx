"use client";
import React from 'react'
import { useEffect, useState } from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure } from "@nextui-org/react";

export const DeletePopup = ({ material, isOpen, onOpenChange, onDelete}) => {
  const [deleteMaterial, setDeleteMaterial] = useState(material);

  React.useEffect(() => {
    setDeleteMaterial(material);
  }, [material]);

  const handleDelete = async () => {
    try {
      // send delete request to backend
      const response = await fetch(`http://localhost:8000/delete_material/${material.id}` , {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) throw new Error("Failed to delete material");

      onDelete(material.id);
      onOpenChange();
    } catch (error) {
      console.error("Error deleting material:", error);
    }
  };

  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center" backdrop="opaque">
      <ModalContent>
        <ModalHeader className="flex flex-col gap-1">
          Delete Material
        </ModalHeader>
        <ModalBody>
          Are you sure you want to delete this material? This action cannot be undone.
        </ModalBody>
        <ModalFooter>
          <Button color="danger" variant="flat" onPress={onOpenChange}>
            Close
          </Button>
          <Button color="primary" onPress={handleDelete}>
            Delete
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};