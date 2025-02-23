"use client";
import { useCallback, useEffect, useState } from "react";
import { User } from "@/types";
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
  Button,
  user
} from "@heroui/react";

import { EditIcon } from "@/constants/EditIcon";
import { DeleteIcon } from "@/constants/DeleteIcon";
import { NewUser, EditUser,DeletePopup } from "@/components";



const UserTable = () => {
  const APIHEADER = "delete_user";  
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editUser, setEditUser] = useState<User | null>(null); 
  const {
    isOpen: isModalOneOpen,
    onOpen: openModalOne,
    onOpenChange: handleModalOneChange,
  } = useDisclosure();
  const [deleteUser, setDeleteUser] = useState<User | null>(null);
  const {isOpen: isDeleteOpen, onOpen: onDeleteOpen, onOpenChange: onDeleteOpenChange} = useDisclosure();

  
  const {
    isOpen: isModalTwoOpen,
    onOpen: openModalTwo,
    onOpenChange: handleModalTwoChange,
  } = useDisclosure();

  

  const list = useAsyncList({
    async load({ signal }) {
      let res = await fetch("http://localhost:8000/users", { signal });
      let json = await res.json();

      const UpdatedUsers = json.map((user) => ({
        ...user, 
        role: user.user_type_id === 1 ? "Admin" : user.user_type_id === 2 ? "Super Admin" : "Not Assigned",
      }));
      setUsers(UpdatedUsers);
      setIsLoading(false);

      return {
        items: UpdatedUsers,
      };
    },
  });

  const handleEditClick = useCallback((user: User) => {
    setEditUser(user);
    openModalOne();
  }, [openModalOne]);

  const handleDeleteClick = useCallback((user: User) => {
    setDeleteUser(user);
    onDeleteOpen();
  }, [onDeleteOpen]);

  // Callback for updating a material
  const handleSaveMaterial = (updatedMaterial: User) => {
    setUsers((prevMaterials) =>
      prevMaterials.map((mat) =>
        mat.id === updatedMaterial.id ? updatedMaterial : mat
      )
    );
    list.reload();
  };
  const addUser = (newUser: User) => {
    setUsers((prevUsers) => [...prevUsers, newUser]);
    
      list.reload();
    };

 const handleDeleteUser = (deletedId: number) => {
    setUsers((prevMaterials) => prevMaterials.filter((mat) => mat.id !== deletedId));
  };


  const renderCell = React.useCallback(
    (user: User, columnKey:string) => {
      const cellValue = user[columnKey as keyof User];
      switch (columnKey) {
        
        case "actions":
          return (
            <div className="relative flex items-center gap-2">
              <Tooltip content="Edit User">
                <span
                  onClick={() => handleEditClick(user)}
                  className="text-lg text-default-400 cursor-pointer active:opacity-50"
                >
                  <EditIcon />
                </span>
              </Tooltip>
              <Tooltip color="danger" content="Delete User">
                  <span
                  onClick={() => handleDeleteClick(user)}
                  className="text-lg text-danger cursor-pointer active:opacity-50"
                >
                  <DeleteIcon />
                </span>
              </Tooltip>
            </div>
          );
          case "user_type_id":
          return user.role || "Not Assigned";
        default:
          return cellValue;
      }
    },
    [handleEditClick, handleDeleteClick]
  );

  return (
    <div>
      <Button onPress={()=> handleModalTwoChange()} color="primary" className="self-start" >Add User</Button>
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
          <TableColumn allowsSorting key="username">
            USERNAME
          </TableColumn>
          <TableColumn allowsSorting key="email">
            EMAIL
          </TableColumn>
          <TableColumn allowsSorting key="user_type_id">
            USER TYPE
          </TableColumn>
          <TableColumn key="actions">ACTIONS</TableColumn>
        </TableHeader>
        <TableBody
          items={users}
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
      <EditUser
        user={editUser}
        isOpen={isModalOneOpen}
        onOpenChange={handleModalOneChange}
        onSave={handleSaveMaterial} // Pass callback to Popup
      />
      <NewUser isOpen={isModalTwoOpen} onOpenChange={handleModalTwoChange} onAddUser={addUser} users={users} />
       <DeletePopup
        item={deleteUser}
        isOpen={isDeleteOpen}
        onOpenChange={onDeleteOpenChange}
        itemType={APIHEADER}
        onDelete={handleDeleteUser} // Pass callback to DeletePopup
      />
    </div>
  );
};

export default UserTable;
