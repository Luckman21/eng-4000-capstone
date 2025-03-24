"use client";
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Avatar, Dropdown, DropdownTrigger, DropdownMenu, DropdownItem, useDisclosure, Badge } from "@heroui/react";
import Link from "next/link";
import { useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { NotificationPanel } from "@/components";
import { NotificationIcon } from "@/constants/NotificationIcon";
import { MaterialCardType } from "@/types";

const Nav = () => {
  const [isInvisible, setIsInvisible] = useState(false);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const pathname = usePathname();
  interface UserType {
    user_type_id: number;
    username: string;
  }

  const [user, setUser] = useState<UserType | null>(null);
  const router = useRouter();
  const [lowStockMaterials, setLowStockMaterials] = useState<MaterialCardType[]>([]);
  const [shelfStatus, setShelfStatus] = useState([]);
  const [notificationCount, setNotificationCount] = useState(0);

  
  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedLowStock = JSON.parse(localStorage.getItem("lowStockMaterials") || "[]");
      const storedShelfStatus = JSON.parse(localStorage.getItem("shelfStatus") || "[]");
      const storedNotificationCount = parseInt(localStorage.getItem("notificationCount") || "0", 10);

      setLowStockMaterials(storedLowStock);
      setShelfStatus(storedShelfStatus);
      setNotificationCount(storedNotificationCount);
    }
  }, []);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/alerts");
    ws.onopen = () => {
      console.log("🔌 WebSocket connected")
    }
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "material_alert") {
          setLowStockMaterials((prev) => {
            const updatedMaterials = data.data;
            localStorage.setItem("lowStockMaterials", JSON.stringify(updatedMaterials));
            return updatedMaterials;
          });
        }if (data.type === "shelf_alert") {
          setShelfStatus((prev) => {
            const updatedShelfStatus = data.data;
            localStorage.setItem("shelfStatus", JSON.stringify(updatedShelfStatus));
            return updatedShelfStatus;

          });
        }
      } catch (error) {
        console.error("Error parsing WebSocket data:", error);
      }
    };
    ws.onclose = () => {
      console.log("🔌 WebSocket disconnected");
    }

    return () => ws.close();
  }, []);

  
  useEffect(() => {
    const newNotificationCount = lowStockMaterials.length + shelfStatus.length;
    setNotificationCount(newNotificationCount);
    localStorage.setItem("notificationCount", newNotificationCount.toString());
  }, [lowStockMaterials, shelfStatus]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/access_management/protected", {
      method: "GET",
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => setUser(data.user))
      .catch((err) => console.error(err));
  }, []);

  const handleLogout = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/access_management/logout", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) throw new Error("Logout failed");

      router.push("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <Navbar >
      <NavbarBrand>
        <img src="/logo.svg" alt="Logo" className="h-12 w-auto"/>
     
      </NavbarBrand>
      <NavbarContent className=" sm:flex gap-4" justify="center">
       
        <NavbarItem isActive={pathname === "/inventory"}  className={pathname === "/inventory" ? "text-primary font-semibold" : "text-white"}>
          <Link href="/inventory" >
          Inventory
          </Link>
        </NavbarItem>
        {user?.user_type_id === 2 && ( // Only render this if user_type_id is 2
          <NavbarItem isActive={pathname === "/users"} className={pathname === "/users" ? "text-primary font-semibold" : "text-white"}>
            <Link href="/users">Users</Link>
          </NavbarItem>
        )}
        <NavbarItem  isActive={pathname === "/materialType"} className={pathname === "/materialType" ? "text-primary font-semibold" : "text-white"}>
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
                <DropdownItem className="text-danger" color="danger" key="logout" onClick={handleLogout}>
                  Logout
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </NavbarItem>
          <NavbarItem onClick={onOpen} style={{ cursor: "pointer" }}>
            <Badge color="danger" content={notificationCount} isInvisible={isInvisible} shape="circle">
              <NotificationIcon className="fill-current" size={30} height={30} width={30} />
            </Badge>
          </NavbarItem>
        </NavbarContent>
      </Navbar>
      <NotificationPanel
        lowstock={lowStockMaterials}
        shelfStat={shelfStatus}
        isOpen={isOpen}
        onOpen={onOpen}
        onOpenChange={onOpenChange}
      />
    </>
  );
};

export default Nav;
