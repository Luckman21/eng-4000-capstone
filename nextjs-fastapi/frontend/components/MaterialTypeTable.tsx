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
  const [user, setUser] = useState(null);
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

  useEffect(() => {
      fetch("http://127.0.0.1:8000/protected", {
        method: "GET",
        credentials: "include", // Ensures cookies are included in the request
      })
        .then((res) => res.json())
        .then((data) => setUser(data.user))
        .catch((err) => console.error(err));
        
    }, []);

  

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
  const columns = (() => {
    return user?.user_type_id === 2
      ? [
          { key: "id", label: "ID" },
          { key: "type_name", label: "NAME" },
          { key: "actions", label: "ACTIONS" }, 
        ]
      : [
          { key: "id", label: "ID" },
          { key: "type_name", label: "NAME" }, 
        ];
  })();
  
  


  const renderCell = React.useCallback(
    (materialType, columnKey) => {
     
  
      // if (columnKey === "actions") {
      //   return (
      //     <div className="relative flex items-center gap-2">
      //       <Tooltip content="Edit Material Type">
      //         <span
      //           onClick={() => handleEditClick(materialType)}
      //           className="text-lg text-default-400 cursor-pointer active:opacity-50"
      //         >
      //           <EditIcon />
      //         </span>
      //       </Tooltip>
      //       <Tooltip color="danger" content="Delete Material Type">
      //         <span
      //           onClick={() => handleDeleteClick(materialType)}
      //           className="text-lg text-danger cursor-pointer active:opacity-50"
      //         >
      //           <DeleteIcon />
      //         </span>
      //       </Tooltip>
      //     </div>
      //   );
      // }
  
      return materialType[columnKey];
    },
    [user]
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
          {columns.map((column) => (
            <TableColumn key={column.key} >
              {column.label}
            </TableColumn>
          ))}
        </TableHeader>
        <TableBody
          items={list.items}
          isLoading={isLoading}
          loadingContent={<Spinner label="Loading..." />}
        >
          {(item) => (
            <TableRow key={item.id}>
              {columns.map((column) => (
                <TableCell key={column.key}>{renderCell(item, column.key)}</TableCell> // ✅ Ensures only defined columns are rendered
              ))}
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
