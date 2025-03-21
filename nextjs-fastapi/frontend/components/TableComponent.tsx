"use client";
import { useCallback, useEffect, useState } from "react";
import { Material, MaterialType } from "@/types";
import axios from "axios";
import { useAsyncList } from "@react-stately/data";
import { fetchMaterialTypes } from "@/constants/data";
import Levenshtein from 'fast-levenshtein';

import React from "react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  Input,
  Tooltip,
  Spinner,
  useDisclosure,
  Button,
} from "@heroui/react";

import { EditIcon } from "@/constants/EditIcon";
import { DeleteIcon } from "@/constants/DeleteIcon";

import { Order, Popup } from "@/components";
import { NewMaterial } from "@/components";
import { DeletePopup } from "@/components";
import { PlusIcon } from "@/constants/PlusIcon";

const statusColorMap: Record<"In Stock" | "Low Stock", "success" | "warning"> = {
  "In Stock": "success",
  "Low Stock": "warning",
}

type MaterialTypeSimple = {
  key: number;
  label: string;
};


const TableComponent = () => {
  const APIHEADER = "delete_material"; 
  const statusOptions = ["available", "unavailable", "in use"];
  const [user, setUser] = useState(null);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editMaterial, setEditMaterial] = useState<Material | null>(null); 
  const [order, setOrder] = useState<Material | null>(null);
  const [materialTypes, setMaterialTypes] = useState<MaterialType[]>([]);
  const [statusFilter, setStatusFilter] = React.useState("all");
  const [filterValue, setFilterValue] = React.useState("");
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
  useEffect(() => {
    const fetchTypes = async () => {
      const types = await fetchMaterialTypes();
      const materialTypes: MaterialTypeSimple[] = types.map(type => ({
        key: type.key,
        label: type.label,
      }));
      setMaterialTypes(materialTypes as unknown as MaterialType[]);
    };
    fetchTypes();
  }, []);
  const {
    isOpen: isModalThreeOpen,
    onOpen: openModalThree,
    onOpenChange: handleModalThreeChange,
  } = useDisclosure();
  
  const list = useAsyncList({
    async load({ signal }) {
      let res = await fetch("http://127.0.0.1:8000/materials", { signal });
      let json = await res.json();

      const updatedMaterials = json.map((material: { mass: number; }) => ({
        ...material,
        status: material.mass < 50 ? "Low Stock" : "In Stock",
      }));
      const types = await fetchMaterialTypes();
      setMaterialTypes(types as MaterialType[]);
       
      setMaterials(updatedMaterials);
      setIsLoading(false);

      return {
        items: updatedMaterials,
      };
    },
  });

  const handleEditClick = useCallback((material: Material) => {
    setEditMaterial(material);
    openModalOne();
  }, [setEditMaterial, openModalOne]);
  const handleOrderClick = (material: Material) => {
    setOrder(material);
    openModalThree();
  };

  const handleDeleteClick = useCallback((material: Material) => {
    setDeleteMaterial(material);
    onDeleteOpen();
  }, [onDeleteOpen]);

  // Callback for updating a material
  const handleSaveMaterial = (updatedMaterial: Material) => {
    setMaterials((prevMaterials) =>
      prevMaterials.map((mat) =>
        mat.id === updatedMaterial.id ? updatedMaterial : mat
      )
    );
    list.reload();
  };
  const addMaterial = (newMaterial: Material) => {
    setMaterials((prevMaterials) => [...prevMaterials, newMaterial]);
    
      list.reload();
    };

 const handleDeleteMaterial = (deletedId: number) => {
    setMaterials((prevMaterials) => prevMaterials.filter((mat) => mat.id !== deletedId));
  };
  useEffect(() => {
    fetch("http://127.0.0.1:8000/protected", {
      method: "GET",
      credentials: "include", // Ensures cookies are included in the request
    })
      .then((res) => res.json())
      .then((data) => setUser(data.user))
      .catch((err) => console.error(err));
      
  }, []);


// Searching Logic
  const hasSearchFilter = Boolean(filterValue);


const filteredItems = React.useMemo(() => {
  let filteredMaterials = [...materials];

  if (hasSearchFilter) {
    filteredMaterials = filteredMaterials
      .map((material) => {

      const mass = material.mass || 0; // Assuming material.mass is a float

        // Differentiate thresholds given common sizes of each category's words
        const levenshteinThresholdColour = 2;
        const levenshteinThresholdStatus = 1;
        const levenshteinThresholdType = 1;

        const materialTypeName = materialTypes.find((type) => type.key === material.material_type_id)?.label || "";

        // Calculate Levenshtein distances for each field
        const colourDistance = Levenshtein.get(filterValue.toLowerCase(), material.colour.toLowerCase());
        const shelfIdDistance = Levenshtein.get(filterValue.toLowerCase(), material.shelf_id.toString().toLowerCase());
        const statusDistance = Levenshtein.get(filterValue.toLowerCase(), material.status.toLowerCase());
        const materialTypeDistance = Levenshtein.get(filterValue.toLowerCase(), materialTypeName.toLowerCase());
        // Sum of all Levenshtein distances
        const totalDistance =
          colourDistance + shelfIdDistance + statusDistance + materialTypeDistance;

        console.log(filterValue);



        // Add distance data to material for sorting
        return {
          ...material,
          totalDistance, // Store the Levenshtein total distance for sorting
          colourMatch: colourDistance <= levenshteinThresholdColour,
          shelfIdMatch: filterValue.toLowerCase() === material.shelf_id.toString().toLowerCase(),
          statusMatch: statusDistance <= levenshteinThresholdStatus,
          materialTypeMatch: materialTypeDistance <= levenshteinThresholdType
        };
      })
      .filter((material) => {
        // Filter based on Levenshtein distance thresholds
        return (
          material.colourMatch ||
          material.shelfIdMatch ||
          material.statusMatch ||
          material.materialTypeMatch
        );
      });
  }

  if (statusFilter !== "all" && Array.from(statusFilter).length !== statusOptions.length) {
    filteredMaterials = filteredMaterials.filter((material) =>
      Array.from(statusFilter).includes(material.status)
    );
  }

  // Sort by the smallest total Levenshtein distance (ascending order)
  filteredMaterials.sort((a, b) => a.totalDistance - b.totalDistance);

  return filteredMaterials;
}, [materials, filterValue, statusFilter, materialTypes, hasSearchFilter]); // Add materialTypes as a dependency

  const renderCell = React.useCallback(
    (material: Material, columnKey: keyof Material | "actions" | "supplier_link") => {
      const cellValue = material[columnKey as keyof Material];
      switch (columnKey) {
        case "status":
          return (
            <Chip
              className="capitalize"
              color={statusColorMap[material.status as "In Stock" | "Low Stock"] || "gray"}
              size="sm"
              variant="flat"
            >
              {cellValue}
            </Chip>
          );
        case "material_type_id":
          const materialType = materialTypes.find(
             (type) => Number(type.key) === Number(material.material_type_id)
           );

          return materialType ? materialType.label : "Unknown Type";
        case "actions":
          return  (
            <div className="relative flex items-center gap-2">
              <Tooltip content="Edit material mass">
                <span
                  onClick={() => handleOrderClick(material)}
                  className="text-lg text-default-400 cursor-pointer active:opacity-50"
                >
                  <PlusIcon />
                </span>
              </Tooltip>
              <Tooltip content="Edit material">
                <span
                  onClick={() => handleEditClick({...material,
                    totalDistance: material.totalDistance ?? 0,
                    name: material.name ?? "Unknown",
                    weight: material.weight ?? 0,})}
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
          ) as any;
        case "supplier_link":
        // Check if there is a link and it's valid
        if (cellValue) {
          return (
          <Chip
              color="warning"
              variant="flat"
              size="sm"
              endContent={<ExternalLinkIcon size={18} stroke="currentColor" />}
              onClick={() => window.open(cellValue, "_blank")}
              className="cursor-pointer"
            >
              Visit Supplier
            </Chip>
          );
        } else {
          return <Chip size="sm">No Link</Chip>; // or some default text
        }
          case "shelf_id":
          return cellValue || "Not Assigned";
        default:
          return cellValue;
      }
    },
    [materialTypes, handleEditClick, handleDeleteClick]
  );

  const onSearchChange = React.useCallback((value: string) => {
  if (value) {
    setFilterValue(value);
  } else {
    setFilterValue("");
  }
}, []);

  function onClear(): void {
    throw new Error("Function not implemented.");
  }

  return (
 <div className="px-4 pt-4"> {/* Padding for spacing from the edges and top */}
    {/* Flex container for the search bar and button */}
    <div className="flex items-center gap-4" style={{ marginBottom: "16px" }}> {/* Gap between button and search bar, margin-bottom for space to the table */}
      {/* Add Material button */}
      <Button
        onPress={() => handleModalTwoChange()}
        color="primary"
        className="self-start"  // Keeps the button at its default size, aligned at the start of the container
      >
        Add Material
      </Button>

      {/* Search Bar */}
      <Input
        isClearable
        className="w-full sm:max-w-[70%]"  // Search bar takes 70% of the width on larger screens
        placeholder="Search by colour, status, shelf, or type..."
        startContent={<SearchIcon />}
        value={filterValue}
        onClear={() => onClear()}
        onValueChange={onSearchChange}
      />
    </div>
      <Table
        aria-label="Visualize information through table"
        isStriped
        onSortChange={list.sort}
        sortDescriptor={list.sortDescriptor}
      >
        <TableHeader>
          <TableColumn   key="id">
            ID
          </TableColumn>
          <TableColumn   key="material_type_id">
            MATERIAL TYPE
          </TableColumn>
          <TableColumn   key="colour">
            COLOUR
          </TableColumn>
          <TableColumn   key="mass">
            MASS (g)
          </TableColumn>
          <TableColumn   key="shelf_id">
            SHELF
          </TableColumn>
          <TableColumn key="status">STATUS</TableColumn>
          <TableColumn   key="supplier_link">
            SUPPLIER LINK
          </TableColumn>
          <TableColumn key="actions">
             ACTIONS
          </TableColumn>
        </TableHeader>
        <TableBody
          items={filteredItems}
          isLoading={isLoading}
          loadingContent={<Spinner label="Loading..." />}
        >
          {filteredItems.map((item) => (
            <TableRow key={item.id}>
              {(columnKey) => <TableCell>{renderCell(item, columnKey as "supplier_link" | "actions" | keyof Material)}</TableCell>}
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Popup
        material={editMaterial ?? {} as Material}
        isOpen={isModalOneOpen}
        onOpenChange={handleModalOneChange}
        onSave={handleSaveMaterial} // Pass callback to Popup
      />
      <NewMaterial isOpen={isModalTwoOpen} onOpenChange={handleModalTwoChange} onAddMaterial={addMaterial} materials={materials} />
       <DeletePopup
        item={deleteMaterial}
        isOpen={isDeleteOpen}
        onOpenChange={onDeleteOpenChange}
        onDelete={handleDeleteMaterial} // Pass callback to DeletePopup
        itemType={APIHEADER}
      />
      <Order
        material={order}
        isOpen={isModalThreeOpen}
        onOpenChange={handleModalThreeChange}
        onSave={handleSaveMaterial} // Pass callback to
        />
    </div>
  );
};

export default TableComponent;


export const ExternalLinkIcon = ({ size = 18, stroke = "currentColor", ...props }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={1.5}
      stroke={stroke}
      width={size}
      height={size}
      {...props}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25"
      />
    </svg>
  );
};

export const SearchIcon = (props: React.JSX.IntrinsicAttributes & React.SVGProps<SVGSVGElement>) => {
  return (
    <svg
      aria-hidden="true"
      fill="none"
      focusable="false"
      height="1em"
      role="presentation"
      viewBox="0 0 24 24"
      width="1em"
      {...props}
    >
      <path
        d="M11.5 21C16.7467 21 21 16.7467 21 11.5C21 6.25329 16.7467 2 11.5 2C6.25329 2 2 6.25329 2 11.5C2 16.7467 6.25329 21 11.5 21Z"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
      />
      <path
        d="M22 22L20 20"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
      />
    </svg>
  );
};