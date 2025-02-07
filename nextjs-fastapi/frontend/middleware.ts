import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Define protected routes
const protectedRoutes = ["/inventory", "/users", "/materialType", "/profile"];

export function middleware(req: NextRequest) {
  const token = req.cookies.get("access_token")?.value; // Read token from cookies
  console.log(token);
  const { pathname } = req.nextUrl;

  // If user tries to access a protected route without a token, redirect to login
  // if (protectedRoutes.includes(pathname) && !token) {
  //   return NextResponse.redirect(new URL("/", req.url)); // Redirect to login
  // }

  return NextResponse.next(); // Allow access if authenticated
}

// Apply middleware to all routes under /inventory, /users, etc.
export const config = {
  matcher: ["/inventory", "/users", "/materialType", "/profile"],
};
