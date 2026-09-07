import type { NextConfig } from "next";

import path from 'path';

const nextConfig: NextConfig = {
  env: {
    OBRA_PATH: path.resolve(process.cwd(), '../projetos/OBRA')
  }
};

export default nextConfig;
