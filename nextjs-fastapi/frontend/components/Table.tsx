"use client";
import React from 'react';
import { useEffect, useState } from 'react';
import { Material,MaterialType } from '@/types';

const Table = () => {
    const [materialData, setMaterialData] = useState<MaterialType[]>([]);
const [loading, setLoading] = useState(true);
    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await fetch('http://localhost:8000/materials');
            const data = await response.json();
            setMaterialData(data);
          } catch (error) {
            console.error('Error fetching material data:', error);
          } finally {
            setLoading(false);
          }
        };
    
        fetchData();
      }, []);
    
      if (loading) return <p>Loading...</p>;

      return (
        <div>
          <h1>Materials</h1>
          <table>
            <thead>
              <tr>
                <th>Material Type</th>
                <th>Color</th>
                <th>Name</th>
                <th>Mass</th>
              </tr>
            </thead>
            <tbody>
              {materialData.map((type) => (
                <React.Fragment key={type.id}>
                  {type.materials.map((material, index) => (
                    <tr key={`${type.id}-${material.id}`}>
                      {index === 0 && (
                        <td rowSpan={type.materials.length}>{type.name}</td>
                      )}
                      <td>{material.colour}</td>
                      <td>{material.name}</td>
                      <td>{material.mass}</td>
                    </tr>
                  ))}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      );
}

export default Table