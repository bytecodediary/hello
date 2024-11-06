"use client";

import { useState, useEffect } from "react";
import { Button } from "@/app/Components/ui/Button";
import Input from "@/app/Components/ui/Input";
import Label from "@/app/Components/ui/label";
import { loginUser } from "@/app/action/loginuser";
import { useRouter } from "next/navigation";

// Define API URL using environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isTokenLoading, setIsTokenLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [csrfToken, setCsrfToken] = useState<string>("");

  const router = useRouter();

  useEffect(() => {
    const fetchCsrfToken = async () => {
      setIsTokenLoading(true);
      setError("");
      
      try {
        const res = await fetch('127.0.0.1:8000/user/get_csrf_token/', {
          method: "GET",
          credentials: "include",
          headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
          },
        });

        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        if (data.csrfToken) {
          setCsrfToken(data.csrfToken);
        } else {
          throw new Error("CSRF token not found in response");
        }
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
        setError("Failed to connect to server. Please try again later.");
      } finally {
        setIsTokenLoading(false);
      }
    };

    fetchCsrfToken();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage("");
    setError("");

    if (!csrfToken) {
      setError("Security token not available. Please refresh the page.");
      setIsLoading(false);
      return;
    }

    const formData = new FormData(e.currentTarget);

    try {
      const result = await loginUser(formData, csrfToken);
      if (result.success) {
        setMessage(result.message || "Login successful!");
        setTimeout(() => router.push("/"), 2000);
      } else {
        setError(result.message || "Login failed. Please try again.");
      }
    } catch (error) {
      console.error("Login error:", error);
      setError("An error occurred during login. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-gray-900">Login</h1>
        
        {isTokenLoading && (
          <div className="text-center text-gray-600">
            Loading...
          </div>
        )}

        {error && (
          <div className="p-3 text-sm text-red-600 bg-red-100 rounded">
            {error}
          </div>
        )}

        {message && (
          <div className="p-3 text-sm text-green-600 bg-green-100 rounded">
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</ Label>
            <Input id="email" name="email" type="email" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" name="password" type="password" required />
          </div>
          <Button 
            type="submit" 
            className="w-full" 
            disabled={isLoading || isTokenLoading || !csrfToken}
          >
            {isLoading ? "Logging in..." : "Login"}
          </Button>
        </form>
      </div>
    </div>
  );
}