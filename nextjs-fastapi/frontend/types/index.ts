export interface Material {
  id: number;
  colour: string;
  name: string;
  weight: number;
  status: string;
  material_type_id: number
}
export interface User {
    id: number;
    username: string;
    password: string;
    email: string;
    user_type_id: number;
    }

export interface MaterialType {
  shelf_id: number | null;
  colour: string;
  supplier_link: string | null;
  mass: number;
  material_type_id: number;
  id: number;
  type_name: string;
}

