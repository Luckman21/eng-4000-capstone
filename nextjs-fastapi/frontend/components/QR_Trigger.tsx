"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { Button, Spinner, Card, CardBody} from "@heroui/react";
import axios from "axios";

const QR_Trigger = () => {
    const router = useRouter();
    const { id } = router.query;
    const [material, setMaterial] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!id) return;

        const fetchMaterialData = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/qr_display/${id}`);
                setMaterial(response.data);
            } catch (err) {
                setError("Failed to fetch material details.");
            } finally {
                setLoading(false);
            }
        };
        fetchMaterialData();
    }, [id]);

    const handleUpdate = async () => {
        try {
            const response = await axios.patch(`http://127.0.0.1:8000/consume_mass/${id}`, {
                mass_change: material?.mass || 0,
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

    if (loading) return <Spinner label="Loading material details..." />;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <div className="flex flex-col items-center justify-center h-screen p-4 bg-gray-900 text-white">
          <Card className="w-full max-w-md p-6 rounded-lg shadow-lg bg-gray-800">
          <CardBody className="text-center">
            <h2 className="text-2xl font-bold">{material?.material_type_name} - {material?.material.colour}</h2>
            <p className="text-lg mt-2">Mass left: {material?.mass} grams</p>
            <p className="text-sm text-gray-400">Shelf: {material?.material.shelf_id || "N/A"}</p>
            <div className="flex justify-center gap-4 mt-6">
                <Button color="primary" onPress={handleUpdate}>
                    Yes
                </Button>
                <Button color="danger" variant="flat" onPress={() => router.push("/inventory")}>
                    No
                </Button>
          </div>
          </CardBody>
          </Card>  
        </div>
    );

};

export default QR_Trigger;