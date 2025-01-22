import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Button} from "@heroui/react";
import Link from "next/link";



const Nav= ()=> {
  return (
    <Navbar>
      <NavbarBrand>
        <p className="font-bold text-inherit">Pantheon 3D Print</p>
      </NavbarBrand>
      <NavbarContent className=" sm:flex gap-4" justify="center">
        <NavbarItem>
          <Link href="/inventory">
            Inventory
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link href="/users">
            Users
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link href="/materialtype">
            Material Type
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem className="lg:flex">
          <Link href="#">Login</Link>
        </NavbarItem>
        <NavbarItem>
          <Button as={Link} color="primary" href="#" variant="flat">
            Sign Up
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
    
  );
}

export default Nav;