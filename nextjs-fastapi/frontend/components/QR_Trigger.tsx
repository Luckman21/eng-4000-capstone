"use client";
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { Button, Spinner, Card, CardBody, Input} from "@heroui/react";
import axios from "axios";

const QR_Trigger = () => {
    const router = useRouter();
    const { id } = useParams();
    const [material, setMaterial] = useState<any>(null);
    const [customMass, setCustomMass] = useState<number>(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!id) return;

        const fetchMaterialData = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/qr_display/${id}`);
                setMaterial(response.data);
                setCustomMass(response.data.mass || 0);
            } catch (err) {
                setError("Failed to fetch material details.");
            } finally {
                setLoading(false);
            }
        };
        fetchMaterialData();
    }, [id]);

    const handleReplenish = async () => {
        try {
            const response = await axios.patch(`http://127.0.0.1:8000/replenish_mass/${id}`, {
                mass_change: customMass,
            });
            if (response.status === 200) {
                alert("Material updated successfully!");
                router.push("/inventory");
            }
        } catch (err) {
            console.error("Failed to update material:", err);
            alert("Update failed.");
        }
    };

    const handleConsume = async () => {
        try {
            const response = await axios.patch(`http://127.0.0.1:8000/consume_mass/${id}`, {
                mass_change: customMass,
            });
            if (response.status === 200) {
                alert("Mass consumed successfully!");
                router.push("/inventory");
            }
        } catch (err) {
            console.error("Failed to consume mass:", err);
            alert("Consume failed.");
        }
    };

    if (loading) return <Spinner label="Loading material details..." />;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <div className="flex flex-col items-center justify-center h-screen p-4 bg-gray-900 text-white">
          <Card className="w-full max-w-md p-6 rounded-lg shadow-lg bg-gray-800">
          <CardBody className="text-center">
            <h2 className="text-2xl font-bold">{material?.material_type_name} - {material?.material.colour}</h2>
            <p className="text-sm text-gray-400">Shelf: {material?.material.shelf_id || "N/A"}</p>
            <p className="text-sm text-gray-400 mt-4"> Enter mass change (grams):
                <Input
                    type="number"
                    value={customMass.toString()}
                    onChange={(e) => setCustomMass(parseFloat(e.target.value))}
                    className="mb-4"
                />
            </p>
            <div className="flex justify-center gap-4 mt-6">
                <Button color="primary" onPress={handleReplenish}>
                    Add Mass
                </Button>
                <Button color="primary" onPress={handleConsume}>
                    Remove Mass
                </Button>
                <Button color="danger" variant="flat" onPress={() => router.push("/inventory")}>
                    Cancel
                </Button>
            </div>
          </CardBody>
          </Card>  
        </div>
    );

};

export default QR_Trigger;