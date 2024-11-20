"use client"; // Client-side component

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/app/Components/ui/Button";
import Input from "@/app/Components/ui/Input";
import Label from "@/app/Components/ui/label";
import { Alert, AlertDescription } from "@/app/Components/ui/alert";
import { registerUser } from "@/app/action/registeruser";

export default function RegisterPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Create state variables for form fields
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [first_name, setfirst_name] = useState<string>("");

  const [csrfToken, setCsrfToken] = useState<string>("");

  useEffect(() => {
    // Fetch CSRF token when the component mounts
    const fetchCsrfToken = async () => {
      const res = await fetch("http://127.0.0.1:8000/user/get_csrf_token/", {
        method: "GET",
        credentials: "include",
      });
      const data = await res.json();
      setCsrfToken(data.csrfToken);
    };
    fetchCsrfToken();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent default form submission
    setIsLoading(true);
    setMessage(null);
    setError(null);

    // Password match validation
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      setIsLoading(false);
      return;
    }

    // Prepare FormData to send to the API
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("confirmPassword", confirmPassword);
    formData.append('first_name', first_name);

    try {
      const result = await registerUser(formData, csrfToken);
      setMessage(result.message);
      setTimeout(() => {
        router.push("/");
      }, 2000);
    } catch (err: any) {
      // Handle different types of errors
      if (err.response && err.response.data) {
        setError(
          err.response.data.message || "Registration failed. Please try again."
        );
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setIsLoading(false); // Stop loading indicator
    }
  };


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-gray-900">
          Register
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              name="username"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="first_name">first_name</Label>
            <Input
              id="first_name"
              name="first_name"
              type="text"
              required
              value={first_name}
              onChange={(e) => setfirst_name(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Registering..." : "Register"}
          </Button>
        </form>
        {message && (
          <Alert>
            <AlertDescription className="text-sm text-center text-green-600">
              {message}
            </AlertDescription>
          </Alert>
        )}
        {error && (
          <Alert variant="destructive">
            <AlertDescription className="text-sm text-center">
              {error}
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
}
