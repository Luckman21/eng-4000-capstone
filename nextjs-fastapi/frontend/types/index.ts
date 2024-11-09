export interface Material {
  id: number;
  colour: string;
  name: string;
  weight: number;
  status: string;
}

export interface MaterialType {
  id: number;
  name: string;
  materials: Material[];
}