import { Card, CardHeader, CardBody, CardFooter, Divider, Link, Image } from "@heroui/react";
import { ShelftCardType } from "@/types";


const ShelfCard = ({ shelf }: { shelf: ShelftCardType }) => {
  return (
    <Card className="bg-primary max-w-sm">
      <CardHeader className="flex gap-3">
      
        <div className="flex flex-col">
          <p className="text-md font-semibold">Shelf ID: {shelf.id}</p>
        </div>
      </CardHeader>
      <Divider />
      <CardBody>
        <p>Humidity: <span className="font-bold">{shelf.humidity}%</span></p>
        <p>Temperature: <span className="font-bold">{shelf.temperature}&deg;C</span></p>

      </CardBody>
      <Divider />
      
    </Card>
  );
};

export default ShelfCard;