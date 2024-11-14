"use server";

async function fetchCsrfToken() {
  const response = await fetch("http://127.0.0.1:8000/user/get_csrf_token/");
  const data = await response.json();
  return data.csrfToken; // Assuming the response is { csrfToken: 'your_token' }
}

export async function registerUser(formData: FormData, csrfToken: string) {
  try {
    console.log("Registration attempt (FormData):", Array.from(formData.entries()));

    // Fetch the CSRF token here
    const csrfToken = await fetchCsrfToken(); 

    const response = await fetch("http://127.0.0.1:8000/user/register/", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      },
    });

    console.log("Server response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Error response:", errorText);
      throw new Error("An unexpected error occurred during registration");
    }

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
