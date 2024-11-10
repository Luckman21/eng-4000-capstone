"use client";
import { useEffect, useState } from 'react';
import { Material,MaterialType } from '@/types';
import axios from 'axios';
import {useAsyncList} from "@react-stately/data";



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
  
  
  let list = useAsyncList({
    async load() {
     
      return {items: materials};
    },
    async sort({items, sortDescriptor}) {
      return {
        items: items.sort((a, b) => {
          let first = a[sortDescriptor.column];
          let second = b[sortDescriptor.column];
          let cmp = (parseInt(first) || first) < (parseInt(second) || second) ? -1 : 1;

          if (sortDescriptor.direction === "descending") {
            cmp *= -1;
          }

          return cmp;
        }),
      };
    },
  });


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
<Table 
  aria-label="Visualize information through table"
  isStriped 
  onSortChange={list.sort} 
  sortDescriptor={list.sortDescriptor}  
  >
    <TableHeader columns={columns}>
      <TableColumn allowsSorting key="id" >
          ID
      </TableColumn>
      <TableColumn allowsSorting key="colour" >
          COLOUR
      </TableColumn>
      <TableColumn allowsSorting key="name" >
          NAME
      </TableColumn>
      <TableColumn allowsSorting key="weight" >
          Weight (g)
      </TableColumn>
      <TableColumn  key="status" >
          STATUS
      </TableColumn>
      <TableColumn  key="actions" >
          ACTIONS
      </TableColumn>
    </TableHeader>
    <TableBody items={list.items}>
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