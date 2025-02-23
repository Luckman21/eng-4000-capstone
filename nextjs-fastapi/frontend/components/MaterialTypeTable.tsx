"use client";
import { Key, useEffect, useState } from "react";
import axios from "axios";
import { useAsyncList } from "@react-stately/data";
import { fetchMaterialTypes } from "@/constants/data";
import { MaterialType } from "@/types";
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
} from "@heroui/react";

import { EditIcon } from "@/constants/EditIcon";
import { DeleteIcon } from "@/constants/DeleteIcon";
import { NewMaterialType, EditMaterialType, DeletePopup } from "@/components";

type MaterialTypes = {
  materialTypes: MaterialType[];
};

const defaultMaterialType: MaterialType = {
  id: 0,
  type_name: "",
  shelf_id: null,
  colour: "",
  supplier_link: null,
  mass: 0,
  material_type_id: 0,
  key: 0,
  label: "",
  status: "",
  totalDistance: 0,
  name: "",
  weight: 0
};

const MaterialTypeTable: React.FC<MaterialTypes> = () => {
  const APIHEADER = "delete_mattype";  
  const [materialTypes, setMaterialTypes] = useState<MaterialType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editMaterialType, setEditMaterialType] = useState<MaterialType | null>(null); 
  const {
    isOpen: isModalOneOpen,
    onOpen: openModalOne,
    onOpenChange: handleModalOneChange,
  } = useDisclosure();
  const [deleteMaterialType, setDeleteMaterialType] = useState<MaterialType | null>(null);
  const {isOpen: isDeleteOpen, onOpen: onDeleteOpen, onOpenChange: onDeleteOpenChange} = useDisclosure();

  
  const {
    isOpen: isModalTwoOpen,
    onOpen: openModalTwo,
    onOpenChange: handleModalTwoChange,
  } = useDisclosure();


  const list = useAsyncList<MaterialType>({
    async load({ signal }) {
      let res = await fetch("http://localhost:8000/material_types", { signal });
      let json = await res.json();
      setIsLoading(false);

      return {
        items: json,
      };
    },
  });

  const handleEditClick = React.useCallback((materialType: MaterialType) => {
    setEditMaterialType(materialType);
    openModalOne();
  }, [openModalOne]);

  const handleDeleteClick = React.useCallback((materialType: MaterialType) => {
    setDeleteMaterialType(materialType);
    onDeleteOpen();
  }, [onDeleteOpen]);

  // Callback for updating a material
  const handleSaveMaterialType = (updatedMaterialType: MaterialType) => {
    setMaterialTypes((prevMaterialType) =>
        prevMaterialType.map((mat) =>
        mat.id === updatedMaterialType.id ? {...mat, ...updatedMaterialType}  : mat
      )
    );
    list.reload();
  };
  const addMaterialType = (newMaterialType: MaterialType) => {
    setMaterialTypes((prevMaterialType) => [...prevMaterialType, newMaterialType]);
    
      list.reload();
    };

 const handleDeleteMaterialType = (deletedId: number) => {
    setMaterialTypes((prevMaterialType) => prevMaterialType.filter((mat) => mat.id !== deletedId));
    list.reload();
  };


  const renderCell = React.useCallback(
    (materialType: MaterialType, columnKey: Key) => {
      if (typeof columnKey !== "string") return null;
      const cellValue = materialType[columnKey as keyof MaterialType];
      switch (columnKey) {
        
        case "actions":
          return (
            <div className="relative flex items-center gap-2">
              <Tooltip content="Edit Material Type">
                <span
                  onClick={() => handleEditClick(materialType)}
                  className="text-lg text-default-400 cursor-pointer active:opacity-50"
                >
                  <EditIcon />
                </span>
              </Tooltip>
              <Tooltip color="danger" content="Delete Material Type">
                  <span
                  onClick={() => handleDeleteClick(materialType)}
                  className="text-lg text-danger cursor-pointer active:opacity-50"
                >
                  <DeleteIcon />
                </span>
              </Tooltip>
            </div>
          );
        default:
          return cellValue;
      }
    },
    [handleEditClick, handleDeleteClick]
  );

  return (
    <div>
      <Button onPress={()=> handleModalTwoChange()} color="primary" >Add Material Type</Button>
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
          <TableColumn allowsSorting key="type_name">
            NAME
          </TableColumn>
          <TableColumn key="actions">ACTIONS</TableColumn>
        </TableHeader>
        <TableBody
          items={list.items}
          isLoading={isLoading}
          loadingContent={<Spinner label="Loading..." />}
        >
          {(item: MaterialType) => (
            <TableRow key={item.id}>
              {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
            </TableRow>
          )}
        </TableBody>
      </Table>
      <EditMaterialType
        materialType={editMaterialType ?? defaultMaterialType }
        isOpen={isModalOneOpen}
        onOpenChange={handleModalOneChange}
        onSave={handleSaveMaterialType} // Pass callback to Popup
      />
      <NewMaterialType isOpen={isModalTwoOpen} onOpenChange={handleModalTwoChange} onAddMaterialType={addMaterialType} materialtypes={materialTypes} />
       <DeletePopup
        item={deleteMaterialType ?? {id: 0}}
        isOpen={isDeleteOpen}
        onOpenChange={onDeleteOpenChange}
        itemType={APIHEADER}
        onDelete={handleDeleteMaterialType} // Pass callback to DeletePopup
      />
    </div>
  );
};

export default MaterialTypeTable;
