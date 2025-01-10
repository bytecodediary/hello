export function logoutUser() {
  localStorage.removeItem("token"); // Clear the JWT token
  // Optionally, update the authentication state in your application context
}
