"use server";

export async function loginUser(formData: FormData) {
  const email = formData.get("email");
  const password = formData.get("password");

  // In a real application, you would validate the credentials here
  console.log("Login attempt:", { email, password });

  // Simulate a delay to mimic an API call
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Return a dummy result
  return { success: true, message: "Login successful" };
}
