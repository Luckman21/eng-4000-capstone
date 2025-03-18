import { Card, CardHeader, CardBody, CardFooter, Divider, Link, Image } from "@heroui/react";
import { MaterialCardType } from "@/types";


const MaterialCard = ({ material }: { material: MaterialCardType }) => {
  return (
    <Card className="bg-primary max-w-sm">
      <CardHeader className="flex gap-3">
      
        <div className="flex flex-col">
          <p className="text-md font-semibold">{material.colour}</p>
          <p className="text-small text-default-500">Material ID: {material.id}</p>
        </div>
      </CardHeader>
      <Divider />
      <CardBody>
        <p>Mass: <span className="font-bold">{material.mass}g</span></p>
      </CardBody>
      <Divider />
      <CardFooter>
        <Link isExternal showAnchorIcon href={material.supplier_link} className="text-white cursor-pointer">
          View Supplier
        </Link>
      </CardFooter>
    </Card>
  );
};

export default MaterialCard;