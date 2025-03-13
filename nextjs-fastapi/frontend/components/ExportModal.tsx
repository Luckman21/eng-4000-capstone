"use client";
import React, {useState} from "react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, RadioGroup, Radio} from "@heroui/react";


interface ExportModalProps {
    isOpen: boolean;
    onClose: () => void;
    onExport: (choice: "materials" | "materialTypes") => void;
}

const ExportModal: React.FC<ExportModalProps> = ({ isOpen, onClose, onExport}) => {
    const [choice, setChoice] = useState<"materials" | "materialTypes">("materials");

    return (
        <Modal isOpen={isOpen} onOpenChange={onClose} placement="center" backdrop="opaque">
            <ModalContent>
                <ModalHeader className="flex flex-col gap-1">
                    Export Data
                </ModalHeader>
                <ModalBody>
                    <p className="mb-4">
                        Select the data you want to export:
                    </p>
                    <RadioGroup
                        value={choice}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setChoice(e.target.value as "materials" | "materialTypes")
                          }
                    >
                        <Radio value="materials">Materials</Radio>
                        <Radio value="materialTypes">Material Types</Radio>
                    </RadioGroup>
                </ModalBody>
                <ModalFooter>
                    <Button
                        color="primary"
                        onPress={() => {
                            onExport(choice);
                            onClose();
                        }}
                    >
                        Export
                    </Button>
                    <Button color="danger" variant="flat" onPress={onClose}>
                        Cancel
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
};

export default ExportModal;