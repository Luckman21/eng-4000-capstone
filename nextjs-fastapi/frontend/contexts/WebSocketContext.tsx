"use client";
import React, { createContext, useContext, useEffect, useRef, useState } from "react";
import { MaterialCardType } from "@/types";

interface WebSocketContextType {
  lowStockMaterials: MaterialCardType[];
  shelfStatus: any[];
  notificationCount: number;
}

const WebSocketContext = createContext<WebSocketContextType>({
  lowStockMaterials: [],
  shelfStatus: [],
  notificationCount: 0,
});

export const useWebSocket = () => useContext(WebSocketContext);

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [lowStockMaterials, setLowStockMaterials] = useState<MaterialCardType[]>([]);
  const [shelfStatus, setShelfStatus] = useState<any[]>([]);
  const [notificationCount, setNotificationCount] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedLowStock = JSON.parse(localStorage.getItem("lowStockMaterials") || "[]");
      const storedShelfStatus = JSON.parse(localStorage.getItem("shelfStatus") || "[]");
      const storedNotificationCount = parseInt(localStorage.getItem("notificationCount") || "0", 10);

      setLowStockMaterials(storedLowStock);
      setShelfStatus(storedShelfStatus);
      setNotificationCount(storedNotificationCount);
    }
  }, []);

  useEffect(() => {
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL}/ws/alerts`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("🔌 WebSocket connected");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "material_alert") {
          setLowStockMaterials(data.data);
          localStorage.setItem("lowStockMaterials", JSON.stringify(data.data));
        } else if (data.type === "shelf_alert") {
          setShelfStatus(data.data);
          localStorage.setItem("shelfStatus", JSON.stringify(data.data));
        }
      } catch (err) {
        console.error("Failed to parse WebSocket data:", err);
      }
    };

    ws.onclose = () => {
      console.log("🔌 WebSocket disconnected");
    };

    return () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    const newCount = lowStockMaterials.length + shelfStatus.length;
    setNotificationCount(newCount);
    localStorage.setItem("notificationCount", newCount.toString());
  }, [lowStockMaterials, shelfStatus]);

  return (
    <WebSocketContext.Provider value={{ lowStockMaterials, shelfStatus, notificationCount }}>
      {children}
    </WebSocketContext.Provider>
  );
};
