"use client";
import {Nav } from "@/components";
import UserProfile from "@/components/UserProfile";


export default function Home() {
  const handleSave = () => {
    console.log("User profile saved");
  };
  return (
    <div>
      <Nav />
        
   
      <UserProfile onSave={handleSave}/>
    </div>
    
  );
}