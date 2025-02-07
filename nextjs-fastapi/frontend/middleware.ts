import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Define protected routes
const protectedRoutes = ["/inventory", "/users", "/materialType", "/profile"];

export function middleware(req: NextRequest) {
  const token = req.cookies.get("access_token")?.value; // Read token from cookies
  const { pathname } = req.nextUrl;

 

  // Check if pathname starts with any protected route and no token is found
  if (protectedRoutes.some((route) => pathname.startsWith(route)) && !token) {
    console.log(req)
    return NextResponse.redirect(new URL("/", req.url)); // Redirect to login if not authenticated
  }
  

  return NextResponse.next(); // Allow access if authenticated
}

// Apply middleware to the specified routes
export const config = {
  matcher: ["/inventory/:path*", "/users/:path*", "/materialType/:path*", "/profile/:path*"],
};
