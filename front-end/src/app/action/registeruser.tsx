"use server";

export async function registerUser(formData: FormData) {
  try {
    // Log the registration attempt
    console.log(
      "Registration attempt (FormData):",
      Array.from(formData.entries())
    );

    // Fetch request to the Django backend
    const response = await fetch("http://127.0.0.1:8000/register/", {
      method: "POST",
      body: formData,
    });

    console.log("Server response status:", response.status);

    // Check if the response is ok (status 200-299)
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error response:", errorData);
      throw new Error(
        errorData.detail || "An unexpected error occurred during registration"
      );
    }

    // If successful, parse the response
    const result = await response.json();
    console.log("Success response:", result);
    return {
      success: true,
      message: result.message || "Registration successful",
    };
  } catch (error) {
    console.error("Error in registerUser function:", error);
    throw error; // Rethrow to be caught by the frontend
  }
}
