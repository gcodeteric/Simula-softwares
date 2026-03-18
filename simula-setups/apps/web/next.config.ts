import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Proxy API calls to Express in development
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: "http://localhost:3001/api/v1/:path*",
      },
    ];
  },

  // Transpile workspace packages
  transpilePackages: ["@simula-setups/types"],
};

export default nextConfig;
