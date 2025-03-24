"use client";
import {Nav,UserProfile } from "@/components";



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