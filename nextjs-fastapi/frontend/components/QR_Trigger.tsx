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
                const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/qr_display/${id}`);
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
            const response = await axios.patch(`${process.env.NEXT_PUBLIC_API_URL}/replenish_mass/${id}`, {
                mass_change: customMass,
            });
            if (response.status === 200) {
                alert(`${customMass} grams has been replenished successfully!`);
                router.push("/inventory");
            }
        } catch (err) {
            console.error("Failed to update material:", err);
            alert("Update failed.");
        }
    };

    const handleConsume = async () => {
        try {
            const response = await axios.patch(`${process.env.NEXT_PUBLIC_API_URL}/consume_mass/${id}`, {
                mass_change: customMass,
            });
            if (response.status === 200) {
                alert(`${customMass} gram has been consumed successfully!`);
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
        <div className="flex flex-col items-center pt-30 px-4" style={{ marginTop: "150px" }}>
          <Card className="w-full max-w-md p-15 rounded-lg shadow-lg bg-gray-800 mt-4">
          <CardBody className="text-center">
            <h2 className="text-2xl font-bold">{material?.material_type_name} - {material?.material.colour}</h2>
            <p className="text-sm text-gray-400">Shelf: {material?.material.shelf_id || "N/A"}</p>
            <p className="text-sm text-gray-400 mt-4"> Enter Mass Change (Grams):
                <Input
                    label="Mass Change (Grams)"
                    type="number"
                    inputMode="numeric"
                    placeholder="Enter mass change in grams"
                    value={customMass.toString()}
                    onChange={(e) => setCustomMass(parseFloat(e.target.value))}
                    className="mb-4"
                />
            </p>
            <div className="flex justify-center items-center mt-6">
                <Button color="primary" style={{marginRight: "50px", marginTop: "5px"}} onPress={handleReplenish}>
                    Add Mass
                </Button>
                <Button color="primary" style={{marginTop: "5px"}} onPress={handleConsume}>
                    Remove Mass
                </Button>
                <Button color="danger" variant="flat" style={{marginLeft: "50px", marginTop: "5px"}} onPress={() => router.push("/inventory")}>
                    Cancel
                </Button>
            </div>
          </CardBody>
          </Card>  
        </div>
    );

};

export default QR_Trigger;