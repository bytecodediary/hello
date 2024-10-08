"use server";

export async function registerUser(formData: FormData) {
  const name = formData.get("name");
  const email = formData.get("email");
  const password = formData.get("password");
  const confirmPassword = formData.get("confirmPassword");

  // Simulate an API call and some logic (e.g., saving user to a database)
  console.log("Registration attempt:", {
    name,
    email,
    password,
    confirmPassword,
  });

  await new Promise((resolve) => setTimeout(resolve, 1000));

  return { success: true, message: "Registration successful" };
}
