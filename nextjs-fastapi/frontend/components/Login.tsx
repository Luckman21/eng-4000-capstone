"use client";
import axios from "axios";
import React from "react";
import { useState } from "react";
import { Form, Input, Button } from "@heroui/react";
import { useRouter } from "next/navigation";
import ForgotPassword from "./ForgotPassword";

const Login = () => {
  const router = useRouter();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const login = async (data) => {
    try {
      const params= new URLSearchParams();
      params.append('username', data.username);
      params.append('password', data.password);
      const response = await axios.post("http://localhost:8000/login", params,{
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token } = response.data;

      // Store the token in localStorage
      localStorage.setItem("access_token", access_token);
      console.log("Login successful");
      router.push("/inventory"); // Redirect to dashboard
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };

  return (
    <><Form
      className="w-full max-w-xs flex flex-col gap-4"
      validationBehavior="native"
      onSubmit={async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(e.currentTarget));
        login(data);

      } }
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
    </Form><ForgotPassword isOpen={isModalOpen} onOpenChange={() => setIsModalOpen(false)}>

    </ForgotPassword>
    </>
    
  );
};

export default Login;
