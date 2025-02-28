"use client";
import axios from "axios";
import React from "react";
import { useState } from "react";
import { Form, Input, Button } from "@heroui/react";
import { useRouter } from "next/navigation";
import ForgotPassword from "./ForgotPassword";

type LoginData = {
  username: string;
  password: string;
};



const Login = () => {
  const router = useRouter();
<<<<<<< HEAD
  const login = async (data: LoginData) => {
    try {
      const params= new URLSearchParams();
=======
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const login = async (data) => {
    setErrorMessage(""); // Clear previous errors

    const params= new URLSearchParams();
>>>>>>> main
      params.append('username', data.username);
      params.append('password', data.password);
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      body: params,
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      credentials: "include", // Ensures cookies are sent & received
    });

    if (response.ok) {
      router.push("/inventory");
      console.log("Login successful");
    } else {
      const errorData = await response.json();
      console.error("Login failed:", errorData);

      // Extract "detail" if it exists
      const errorMessage = errorData?.detail || "Login failed. Please try again.";
      setErrorMessage(errorMessage);
    }
  };

  return (
    <><Form
      className="w-full max-w-xs flex flex-col gap-4"
      validationBehavior="native"
      onSubmit={async (e) => {
        e.preventDefault();
<<<<<<< HEAD
        const data = Object.fromEntries(new FormData(e.currentTarget)) as LoginData;
        login(data); 
        
      }}
=======
        const data = Object.fromEntries(new FormData(e.currentTarget));
        login(data);

      } }
>>>>>>> main
    >
      <Input
        isRequired
        errorMessage="Please enter a valid username"
        label="Username"
        labelPlacement="outside"
        name="username"
        placeholder="Enter your username"
        type="text" />

      <Input
        isRequired
        errorMessage="Please enter a valid password"
        label="Password"
        labelPlacement="outside"
        name="password"
        placeholder="Enter your password"
        type="password" />
      <div className="flex gap-2">
        <Button color="primary" type="submit">
          Login
        </Button>
        <Button variant="flat" onPress={() => setIsModalOpen(true)}>
          Forgot Password
        </Button>
      </div>
        {errorMessage && (
            <p className="text-red-500 bg-red-100 border border-red-400 text-sm mt-2 p-2 rounded">
        {errorMessage}
            </p>
        )}

    </Form><ForgotPassword isOpen={isModalOpen} onOpenChange={() => setIsModalOpen(false)}>

    </ForgotPassword>
    </>

  );
};

export default Login;
