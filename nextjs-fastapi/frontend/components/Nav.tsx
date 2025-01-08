"use client"
import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button, useDisclosure} from "@nextui-org/react";
import { Badge } from "@nextui-org/react";
import { NotificationIcon } from "@/constants/NotificationIcon";
import React from "react";
import {NotificationPanel} from "@/components";
const Nav= ()=> {
  const [isInvisible, setIsInvisible] = React.useState(false);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
    
  
  return (
    <>
      {/* Navbar */}
      <Navbar>
        <NavbarBrand>
          <p className="font-bold text-inherit">Pantheon 3D Print</p>
        </NavbarBrand>
        <NavbarContent className="hidden sm:flex gap-4" justify="center">
          <NavbarItem>
            <Link color="foreground" href="#">
              Log
            </Link>
          </NavbarItem>
          <NavbarItem isActive>
            <Link href="#" aria-current="page">
              Inventory
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Link color="foreground" href="#">
              Edit Materials
            </Link>
          </NavbarItem>
        </NavbarContent>
        <NavbarContent justify="end">
          <NavbarItem className="hidden lg:flex">
            <Link href="#">Login</Link>
          </NavbarItem>
          <NavbarItem>
            <Button as={Link} color="primary" href="#" variant="flat">
              Sign Up
            </Button>
          </NavbarItem>
          <NavbarItem onClick={onOpen} style={{ cursor: "pointer" }}>
            {/* Badge with Notification Icon */}
            <Badge
              color="danger"
              content={5}
              isInvisible={isInvisible}
              shape="circle"
            >
              <NotificationIcon className="fill-current" size={30} height={30} width={30} />
            </Badge>
          </NavbarItem>
        </NavbarContent>
      </Navbar>

      {/* Notification Panel */}
      <NotificationPanel isOpen={isOpen} onOpen={onOpen} onOpenChange={onOpenChange} />
    </>
  );
};

export default Nav;