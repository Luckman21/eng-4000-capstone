"use client";
import { useEffect, useState } from "react";
import { MaterialType } from "@/types";
import axios from "axios";
import { useAsyncList } from "@react-stately/data";
import { fetchMaterialTypes } from "@/constants/data";

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



const MaterialTypeTable = () => {
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

  //useEffect(() => {
    //const fetchTypes = async () => {
      //const types = await fetchMaterialTypes();
      //setMaterialTypes(types);
    //};
    //fetchTypes();
  //}, []);

  

  const list = useAsyncList({
    async load({ signal }) {
      let res = await fetch("http://localhost:8000/material_types", { signal });
      let json = await res.json();
      setIsLoading(false);

      return {
        items: json,
      };
    },
  });

  const handleEditClick = (materialType: MaterialType) => {
    setEditMaterialType(materialType);
    openModalOne();
  };

  const handleDeleteClick = (materialType: MaterialType) => {
    setDeleteMaterialType(materialType);
    onDeleteOpen();
  };

  // Callback for updating a material
  const handleSaveMaterialType = (updatedMaterialType: MaterialType) => {
    setMaterialTypes((prevMaterialType) =>
        prevMaterialType.map((mat) =>
        mat.id === updatedMaterialType.id ? updatedMaterialType : mat
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
    (materialType, columnKey) => {
      const cellValue = materialType[columnKey];
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
    []
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
            Name
          </TableColumn>
          <TableColumn key="actions">ACTIONS</TableColumn>
        </TableHeader>
        <TableBody
          items={list.items}
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
      <EditMaterialType
        materialType={editMaterialType}
        isOpen={isModalOneOpen}
        onOpenChange={handleModalOneChange}
        onSave={handleSaveMaterialType} // Pass callback to Popup
      />
      <NewMaterialType isOpen={isModalTwoOpen} onOpenChange={handleModalTwoChange} onAddMaterialType={addMaterialType} materialtypes={materialTypes} />
       <DeletePopup
        item={deleteMaterialType}
        isOpen={isDeleteOpen}
        onOpenChange={onDeleteOpenChange}
        itemType={APIHEADER}
        onDelete={handleDeleteMaterialType} // Pass callback to DeletePopup
      />
    </div>
  );
};

export default MaterialTypeTable;
