      const { m } = require('framer-motion');

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ["images.squarespace-cdn.com"], // Allow Squarespace images
  },
  async rewrites() {
    return [
      {
        source: "/access_management/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/access_management/:path*`,
      },
      {
        source: "/materials/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/materials/:path*`,
      },
      {
        source: "/materials",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/materials`,
      },
      {
        source: "/material_types/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/material_types/:path*`,
      },
      {
        source: "/material_types",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/material_types`,
      },
      {
        source: "/users/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/users/:path*`,
      },
      {
        source: "/user_types",
        destination: `${process.env.NEXT_PUBLIC_API_URL}/user_types`,
      },


      
    ];
  },
  reactStrictMode: true,
};

module.exports = nextConfig;