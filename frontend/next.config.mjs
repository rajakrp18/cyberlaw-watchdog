/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',        // Generates static HTML/CSS/JS in /out
  trailingSlash: true,     // Ensures clean paths for static file serving
  images: {
    unoptimized: true,     // Required for static export (no Next.js image server)
  },
};

export default nextConfig;
