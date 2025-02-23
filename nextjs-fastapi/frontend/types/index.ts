export interface Material {
  totalDistance: any;
  shelf_id: any;
  mass: number;
  id: number;
  colour: string;
  name: string;
  weight: number;
  status: string;
  material_type_id: number
}
export interface User {
    role: string;
    id: number;
    username: string;
    password: string;
    email: string;
    user_type_id: number;
    }

export interface MaterialType {
  weight: number;
  name: string;
  totalDistance: number;
  status: any;
  key: number;
  label: string;
  shelf_id: number | null;
  colour: string;
  supplier_link: string | null;
  mass: number;
  material_type_id: number;
  id: number;
  type_name: string;
}

