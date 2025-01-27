"use client";
import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Avatar,Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from "@heroui/react";
import Link from "next/link";
import { jwtDecode } from "jwt-decode";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";


const Nav= ()=> {
  const [user, setUser] = useState(null);
  const router = useRouter();
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decoded = jwtDecode(token) // Extract user info from JWT
        setUser(decoded); 
      } catch (err) {
        console.error("Failed to decode token:", err);
      }
    }
  }, []);
  const handleLogout = () => {
    localStorage.removeItem("access_token"); // Remove token
    setUser(null); // Clear user state
    router.push("/"); // Redirect to login
  };
  return (
    <Navbar>
      <NavbarBrand>
        <p className="font-bold text-inherit">Pantheon 3D Print</p>
      </NavbarBrand>
      <NavbarContent className=" sm:flex gap-4" justify="center">
        <NavbarItem >
          <Link href="/inventory" >
          Inventory
          </Link>
        </NavbarItem>
        {user?.user_type_id === 2 && ( // Only render this if user_type_id is 2
          <NavbarItem>
            <Link href="/users">Users</Link>
          </NavbarItem>
        )}
        <NavbarItem>
          <Link href="/materialType">
            Material Type
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem className="lg:flex ">
        <Dropdown>
              <DropdownTrigger>
                <Avatar
                  showFallback
                  src={ "https://images.unsplash.com/broken"}
                  name={user?.username}
                  className="cursor-pointer"
                />
              </DropdownTrigger>
              <DropdownMenu>
                <DropdownItem key="profile">
                  <Link href="/profile">Edit Profile</Link>
                </DropdownItem>
                <DropdownItem className="text-danger" color="danger" key="logout" onClick={handleLogout}>Logout</DropdownItem>
              </DropdownMenu>
            </Dropdown>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
    
  );
}

export default Nav;