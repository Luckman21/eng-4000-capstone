"use client";
import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Avatar,Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from "@heroui/react";
import Link from "next/link";
import { jwtDecode } from "jwt-decode";
import { JwtPayload } from "jwt-decode";
import { useState, useEffect } from "react";
import { useRouter,usePathname } from "next/navigation";
import { getUserServer } from "../app/userCreds";

interface customJWTPayload extends JwtPayload {
  user_type_id: number;
  username: string;
}




<<<<<<< HEAD
const Nav= ()=> {
  const [user, setUser] = useState<customJWTPayload | null>(null);
  const router = useRouter();
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decoded = jwtDecode<customJWTPayload>(token) // Extract user info from JWT
        setUser(decoded); 
      } catch (err) {
        console.error("Failed to decode token:", err);
      }
    }
=======


const Nav=  ()=> {
  
  const pathname = usePathname(); // Get the current path
  const [user, setUser] = useState(null);
  const router = useRouter();
  useEffect(() => {
    fetch("http://127.0.0.1:8000/protected", {
      method: "GET",
      credentials: "include", // Ensures cookies are included in the request
    })
      .then((res) => res.json())
      .then((data) => setUser(data.user))
      .catch((err) => console.error(err));

>>>>>>> main
  }, []);
 
  const handleLogout = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/logout", {
        method: "POST",
        credentials: "include", // REQUIRED to send cookies
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      if (!response.ok) throw new Error("Logout failed");
  
      // setUser(null); // Clear user state
      router.push("/"); // Redirect to login
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };
  
  return (
    <Navbar>
      <NavbarBrand>
        <p className="font-bold text-inherit">Pantheon 3D Print</p>
      </NavbarBrand>
      <NavbarContent className=" sm:flex gap-4" justify="center">
       
        <NavbarItem isActive={pathname === "/inventory"} >
          <Link href="/inventory" >
          Inventory
          </Link>
        </NavbarItem>
        {user?.user_type_id === 2 && ( // Only render this if user_type_id is 2
          <NavbarItem isActive={pathname === "/users"}>
            <Link href="/users">Users</Link>
          </NavbarItem>
        )}
        <NavbarItem  isActive={pathname === "/materialType"}>
          <Link href="/materialType">
            Material Type
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem className="lg:flex " >
        <Dropdown>
              <DropdownTrigger>
                <Avatar
                  color="primary"
                  src="https://img.icons8.com/?size=100&id=23265&format=png&color=FFFFFF"
                  isBordered
                  showFallback
                  
                  name={user?.username}
                  className="cursor-pointer"
                />
                
                
              </DropdownTrigger>
              <DropdownMenu>
                <DropdownItem key="profile">
                  <Link href="/userProfile">Edit Profile</Link>
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