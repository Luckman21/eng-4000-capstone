
import {Nav, MaterialTypeTable } from "@/components";
import { useEffect, useState } from "react";
import { MaterialType } from "@/types";


export default function Home() {



  return (
    <div>
      <Nav />

   
      <MaterialTypeTable materialTypes={[]}      />
    </div>
    
  );
}