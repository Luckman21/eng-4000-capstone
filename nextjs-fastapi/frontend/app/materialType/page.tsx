"use client";
import {Nav, MaterialTypeTable } from "@/components";
import { useEffect, useState } from "react";
import { MaterialType } from "@/types";


export default function Home() {

  const [materialTypes, setMaterialTypes] = useState<MaterialType[]>([]);

  useEffect(() => {
    const fetchMaterialTypes = async () => {
      const response = await fetch("http://localhost:8000/material_types");
      const data: MaterialType[] = await response.json();
      setMaterialTypes(data); // Set the fetched material types
    };

    fetchMaterialTypes();
  }, []);

  return (
    <div>
      <Nav />

   
      <MaterialTypeTable materialTypes={materialTypes}/>
    </div>
    
  );
}