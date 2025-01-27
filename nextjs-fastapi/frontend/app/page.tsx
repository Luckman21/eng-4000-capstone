import {TableComponent,Nav, MaterialTypeTable, Login } from "@/components";
import Image from "next/image";


export default function Home() {
  return (
    <div>
      <div className="flex flex-col items-center justify-center">
      <img
  alt="HeroUI hero Image"
  src="https://images.squarespace-cdn.com/content/v1/60a8596ca42a161bf6c0f763/1677882569090-KOBZVPPP0CHH9U8GCHEI/logotype_horizontal.png"
  width={500}
/>
        <Login/>
      </div>
      
      

   
      
    </div>
    
  );
}
