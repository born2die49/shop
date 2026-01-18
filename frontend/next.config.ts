import type { NextConfig } from "next";

const nextConfig: NextConfig = {
	/* config options here */
	reactCompiler: true,
	images: {
		remotePatterns: [
			{
        protocol: "https",
        hostname: "*.s3.amazonaws.com", // Matches all S3 buckets and regions
      },
      {
        protocol: "https",
        hostname: "s3.amazonaws.com", // Matches path-style S3 URLs
      },
		],
	},

  // turbopack: {},

  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.watchOptions = {
        poll: 200, // Check for changes every 0.1 second
        aggregateTimeout: 100, // Delay before rebuilding
      };
    }
    return config;
  },
};

export default nextConfig;
