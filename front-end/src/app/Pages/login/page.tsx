"use client";

import { Button } from "@/app/Components/ui/Button";
import Input from "@/app/Components/ui/Input";
import Label from "@/app/Components/ui/label";
import { useState } from "react";
import { loginUser } from "@/app/action/loginuser";
import router from "next/router";

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (formData: FormData) => {
    setIsLoading(true);
    setMessage("");
    try {
      const result = await loginUser(formData);
      setMessage(result.message);
      setTimeout(() => router.push("/"), 2000);
    } catch (error) {
      setMessage("An error occurred during login");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-gray-900">Login</h1>
        <form action={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" name="email" type="email" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" name="password" type="password" required />
          </div>
          <Button variant="darker" size="lg">
            Login
          </Button>
        </form>
        {message && (
          <p className="text-sm text-center text-green-600">{message}</p>
        )}
      </div>
    </div>
  );
}
