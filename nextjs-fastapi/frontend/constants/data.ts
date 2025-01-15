


const fetchMaterialTypes = async () => {
  try {
    const res = await fetch("http://localhost:8000/material_types");
    const data = await res.json();

    // Transform fetched data to match AutocompleteItem structure
    const types = data.map((type) => ({
      label: type.type_name,
      key: type.id,
    }));
    return types;
    
  } catch (error) {
    console.error("Error fetching material types:", error);
    return []; // Return an empty array in case of an error
  }
};

// Function to get material type name by ID
async function MaterialTypeName(id: number): Promise<string | null> {
  const types = await fetchMaterialTypes(); 
  const type = types.find((t) => t.id === id); 
  return type ? type.label : null; 
}

export { fetchMaterialTypes, MaterialTypeName };
