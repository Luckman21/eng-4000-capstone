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
  id: number;
  name: string;
}

