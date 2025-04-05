import { HeroUIProvider } from "@heroui/react";
import { WebSocketProvider } from "@/contexts/WebSocketContext";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <HeroUIProvider>
      <WebSocketProvider>
        {children}
      </WebSocketProvider>
    </HeroUIProvider>
  );
}
