export interface Material { 
    id: number;
    colour: string;
    name: string;
    mass: number;
    
    }

export interface MaterialType {
    id: number;
    name: string;
    materials: Material[];
}