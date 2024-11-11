import { Material } from "@/types";
const columns = [
    {name: "ID", uid: "id"},
    {name: "COLOUR", uid: "colour"},
    {name: "NAME", uid: "name"},
    {name: "Weight (g)", uid: "mass"},
    {name: "STATUS", uid: "status"},
    {name: "ACTIONS", uid: "actions"},
  ];

  
  const hardcodedMaterials = [
    {
      id: 1,
      colour: "Red",
      name: "Apple",
      weight: 0.2,
      status: "In Stock",
    },
    {
      id: 2,
      colour: "Yellow",
      name: "Banana",
      weight: 0.3,
      status: "In Stock",
    },
    {
      id: 3,
      colour: "Green",
      name: "Grapes",
      weight: 0.4,
      status: "Out of Stock",
    },
    {
      id: 4,
      colour: "Orange",
      name: "Orange",
      weight: 0.5,
      status: "Low Stock",
    },
    {
      id: 5,
      colour: "Purple",
      name: "Plum",
      weight: 0.6,
      status: "In Stock",
    },
    {
      id: 6,
      colour: "Red",
      name: "Strawberry",
      weight: 0.7,
      status: "Out of Stock",
    },
      
  ];
  
  export {columns, hardcodedMaterials};