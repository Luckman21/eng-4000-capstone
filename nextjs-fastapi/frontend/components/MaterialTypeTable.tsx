"use client";
import { Key, useEffect, useState } from "react";
import axios from "axios";
import { useAsyncList } from "@react-stately/data";
import { fetchMaterialTypes } from "@/constants/data";
import { MaterialType, User } from "@/types";
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

type UserInfo = {
  user_type_id: number;
  username: string;
  email: string;
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
  const [user, setUser] = useState<UserInfo | null>(null);
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
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/protected`, {
        method: "GET",
        credentials: "include", // Ensures cookies are included in the request
      })
        .then((res) => res.json())
        .then((data) => setUser(data.user as UserInfo))
        .catch((err) => console.error(err));
        
    }, []);

  const list = useAsyncList<MaterialType>({
    async load({ signal }) {
      let res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/material_types`, { signal });
      let json = await res.json();
      setMaterialTypes(json);
      setIsLoading(false);

      return {
        items: json,
      };
    },
  });

  const exportCSV = (data: any[], filename: string) => {
    if (data.length === 0) {
      alert("No data to export");
      return;
    }
    const headers = Object.keys(data[0]);
    const csvRows = [];
    csvRows.push(headers.join(","));
    for (const item of data) {
      const values = headers.map((header) => {
        let val = item[header as keyof typeof item];
        if (typeof val === "string") {
          // Escape quotes by doubling them
          val = val.replace(/"/g, '""');
          return `"${val}"`;
        }
        return val;
      });
      csvRows.push(values.join(","));
    }
    const csvString = csvRows.join("\n");
    const blob = new Blob([csvString], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleEditClick = React.useCallback((materialType: MaterialType) => {
    setEditMaterialType(materialType);
    openModalOne();
  }, [setEditMaterialType, openModalOne]);

  const handleDeleteClick = React.useCallback((materialType: MaterialType) => {
    setDeleteMaterialType(materialType);
    onDeleteOpen();
  }, [setDeleteMaterialType, onDeleteOpen]);

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
          { key: "actions", label: "ACTIONS" },
        ];
  })();
  
  


  const renderCell = React.useCallback(
    (materialType: MaterialType, columnKey: string) => {
      if (!columns.find(col => col.key === columnKey)) return null;
  
      if (columnKey === "actions") {
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
      } return materialType[columnKey as keyof MaterialType];
    },
    [[columns, handleEditClick, handleDeleteClick]]
  );
  

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <Button onPress={()=> handleModalTwoChange()} color="primary" >Add Material Type</Button>

        <Button color="primary" onPress={() => exportCSV(materialTypes, "materialTypes.csv")}>
          Export CSV
        </Button>
      </div>
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
          items={materialTypes}
          isLoading={isLoading}
          loadingContent={<Spinner label="Loading..." />}
        >
          {(item: MaterialType) => (
            <TableRow key={item.id}>
              {columns.map((column) => (
                <TableCell key={column.key}>{renderCell(item, column.key)}</TableCell> // ✅ Ensures only defined columns are rendered
              ))}
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
