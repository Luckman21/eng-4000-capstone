"use client";
import { useEffect, useState } from 'react';
import { Material,MaterialType } from '@/types';
import axios from 'axios';



import React from "react";
import {Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, Chip, Tooltip, getKeyValue} from "@nextui-org/react";

import { EditIcon } from '@/constants/EditIcon';
import { DeleteIcon } from '@/constants/DeleteIcon';
import { columns, hardcodedMaterials } from '@/constants/data';

const statusColorMap = {
  "In Stock": "success",
  "Out of Stock": "danger",
  "Low Stock": "warning",
};



const TableComponent = () => {
  const [materials, setMaterials] = useState<Material[]>(hardcodedMaterials);
  useEffect(() => {
    const fetchMaterials = async () => {
      try {
        const response = await axios.get<Material[]>("http://localhost:8000/materials");
        setMaterials(response.data); // Set API materials if fetch is successful
      } catch (error) {
        console.error("Failed to fetch materials. Using hardcoded data.", error);
        
      }
    };

    fetchMaterials();
  }, []);

const renderCell = React.useCallback((material, columnKey) => {
  const cellValue = material[columnKey];

  switch (columnKey) {
    case "status":
      return (
        <Chip className="capitalize" color={statusColorMap[material.status]} size="sm" variant="flat">
          {cellValue}
        </Chip>
      );
    case "actions":
      return (
        <div className="relative flex items-center gap-2">
          <Tooltip content="Edit material">
            <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
              <EditIcon />
            </span>
          </Tooltip>
          <Tooltip color="danger" content="Delete material">
            <span className="text-lg text-danger cursor-pointer active:opacity-50">
              <DeleteIcon />
            </span>
          </Tooltip>
        </div>
      );
    default:
      return cellValue;
  }
}, []);

return (
<Table isStriped>
    <TableHeader columns={columns}>
      {(column) => (
        <TableColumn key={column.uid} >
          {column.name}
        </TableColumn>
      )}
    </TableHeader>
    <TableBody items={materials}>
      {(item) => (
        <TableRow key={item.id}>
          {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
        </TableRow>
      )}
    </TableBody>
  </Table>
);
}

export default TableComponent