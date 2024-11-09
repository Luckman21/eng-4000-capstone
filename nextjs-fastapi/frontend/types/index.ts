export interface Material {
    id: number;
  color: string;
  name: string;
  mass: number;
}

export interface MaterialType {
  id: number;
  name: string;
  materials: Material[];
}