"use server";

export async function registerUser(formData: FormData) {
  // Extract data from FormData
  const username = formData.get("username");
  const email = formData.get("email");
  const password = formData.get("password");
  const confirmPassword = formData.get("confirmPassword");

  // Log the registration attempt for debugging purposes
  console.log("Registration attempt:", {
    username,
    email,
    password,
    confirmPassword,
  });

  // Check if passwords match before making the API call
  if (password !== confirmPassword) {
    throw new Error("Passwords do not match");
  }

  // Prepare user data to send to the API
  const userData = {
    username,
    email,
    password,
  };

  // Fetch request to the Django backend
  const response = await fetch("http://127.0.0.1:8000/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData), // Send user data as JSON
  });

  // Check if the response is ok (status 200-299)
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || "An unexpected error occurred during registration"
    );
  }

  // If successful, parse the response and return a success message
  const result = await response.json();
  return {
    success: true,
    message: result.message || "Registration successful",
  };
}
