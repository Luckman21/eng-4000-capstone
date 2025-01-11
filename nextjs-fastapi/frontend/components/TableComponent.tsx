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
  useDisclosure
} from "@nextui-org/react";

import { EditIcon } from "@/constants/EditIcon";
import { DeleteIcon } from "@/constants/DeleteIcon";
import { columns } from "@/constants/data";
import { Popup } from "@/components/Popup";

const statusColorMap = {
  "In Stock": "success",
  "Low Stock": "warning",
};

const TableComponent = () => {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editMaterial, setEditMaterial] = useState<Material | null>(null); // Single Material
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

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
    onOpen();
  };

  // Callback for updating a material
  const handleSaveMaterial = (updatedMaterial: Material) => {
    setMaterials((prevMaterials) =>
      prevMaterials.map((mat) =>
        mat.id === updatedMaterial.id ? updatedMaterial : mat
      )
    );
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
                <span className="text-lg text-danger cursor-pointer active:opacity-50">
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
      <Table
        aria-label="Visualize information through table"
        isStriped
        onSortChange={list.sort}
        sortDescriptor={list.sortDescriptor}
      >
        <TableHeader columns={columns}>
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
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        onSave={handleSaveMaterial} // Pass callback to Popup
      />
    </div>
  );
};

export default TableComponent;
