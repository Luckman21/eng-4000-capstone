"use client";
import { useEffect, useState } from "react";
import { Material, MaterialType } from "@/types";
import axios from "axios";
import { useAsyncList } from "@react-stately/data";

import React from "react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  Tooltip,
  Spinner,
  useDisclosure,
  Button
} from "@nextui-org/react";

import { EditIcon } from "@/constants/EditIcon";
import { DeleteIcon } from "@/constants/DeleteIcon";

import { Popup } from "@/components";
import { NewMaterial } from "@/components";
import { DeletePopup } from "@/components/DeletePopup";

const statusColorMap = {
  "In Stock": "success",
  "Low Stock": "warning",
}

const TableComponent = () => {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editMaterial, setEditMaterial] = useState<Material | null>(null); 
  const {
    isOpen: isModalOneOpen,
    onOpen: openModalOne,
    onOpenChange: handleModalOneChange,
  } = useDisclosure();
  const [deleteMaterial, setDeleteMaterial] = useState<Material | null>(null);
  const {isOpen: isDeleteOpen, onOpen: onDeleteOpen, onOpenChange: onDeleteOpenChange} = useDisclosure();

  
  const {
    isOpen: isModalTwoOpen,
    onOpen: openModalTwo,
    onOpenChange: handleModalTwoChange,
  } = useDisclosure();

  

  const list = useAsyncList({
    async load({ signal }) {
      let res = await fetch("http://localhost:8000/materials", { signal });
      let json = await res.json();

      const updatedMaterials = json.map((material) => ({
        ...material,
        status: material.mass <= 50 ? "Low Stock" : "In Stock",
      }));
      setMaterials(updatedMaterials);
      setIsLoading(false);

      return {
        items: updatedMaterials,
      };
    },
  });

  const handleEditClick = (material: Material) => {
    setEditMaterial(material);
    openModalOne();
  };

  const handleDeleteClick = (material: Material) => {
    setDeleteMaterial(material);
    onDeleteOpen();
  };

  // Callback for updating a material
  const handleSaveMaterial = (updatedMaterial: Material) => {
    setMaterials((prevMaterials) =>
      prevMaterials.map((mat) =>
        mat.id === updatedMaterial.id ? updatedMaterial : mat
      )
    );
    list.reload();
  };
  const addMaterial = (newMaterial) => {
    setMaterials((prevMaterials) => [...prevMaterials, newMaterial]);
    
      list.reload();
    };

 const handleDeleteMaterial = (deletedId: number) => {
    setMaterials((prevMaterials) => prevMaterials.filter((mat) => mat.id !== deletedId));
  };


  const renderCell = React.useCallback(
    (material, columnKey) => {
      const cellValue = material[columnKey];
      switch (columnKey) {
        case "status":
          return (
            <Chip
              className="capitalize"
              color={statusColorMap[material.status]}
              size="sm"
              variant="flat"
            >
              {cellValue}
            </Chip>
          );
        case "actions":
          return (
            <div className="relative flex items-center gap-2">
              <Tooltip content="Edit material">
                <span
                  onClick={() => handleEditClick(material)}
                  className="text-lg text-default-400 cursor-pointer active:opacity-50"
                >
                  <EditIcon />
                </span>
              </Tooltip>
              <Tooltip color="danger" content="Delete material">
                  <span
                  onClick={() => handleDeleteClick(material)}
                  className="text-lg text-danger cursor-pointer active:opacity-50"
                >
                  <DeleteIcon />
                </span>
              </Tooltip>
            </div>
          );
          case "shelf_id":
          return cellValue || "Not Assigned";
        default:
          return cellValue;
      }
    },
    []
  );

  return (
    <div>
      <Button onPress={()=> handleModalTwoChange()} color="primary" >Add Material</Button>
      <Table
        aria-label="Visualize information through table"
        isStriped
        onSortChange={list.sort}
        sortDescriptor={list.sortDescriptor}
      >
        <TableHeader>
          <TableColumn allowsSorting key="id">
            ID
          </TableColumn>
          <TableColumn allowsSorting key="colour">
            COLOUR
          </TableColumn>
          <TableColumn allowsSorting key="name">
            NAME
          </TableColumn>
          <TableColumn allowsSorting key="mass">
            Weight (g)
          </TableColumn>
          <TableColumn allowsSorting key="material_type_id">
            Material Type
          </TableColumn>
          <TableColumn allowsSorting key="shelf_id">
            Shelf
          </TableColumn>
          <TableColumn key="status">STATUS</TableColumn>
          <TableColumn key="actions">ACTIONS</TableColumn>
        </TableHeader>
        <TableBody
          items={materials}
          isLoading={isLoading}
          loadingContent={<Spinner label="Loading..." />}
        >
          {(item) => (
            <TableRow key={item.id}>
              {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
            </TableRow>
          )}
        </TableBody>
      </Table>
      <Popup
        material={editMaterial}
        isOpen={isModalOneOpen}
        onOpenChange={handleModalOneChange}
        onSave={handleSaveMaterial} // Pass callback to Popup
      />
      <NewMaterial isOpen={isModalTwoOpen} onOpenChange={handleModalTwoChange} onAddMaterial={addMaterial} materials={materials} />
       <DeletePopup
        material={deleteMaterial}
        isOpen={isDeleteOpen}
        onOpenChange={onDeleteOpenChange}
        onDelete={handleDeleteMaterial} // Pass callback to DeletePopup
      />
    </div>
  );
};

export default TableComponent;
