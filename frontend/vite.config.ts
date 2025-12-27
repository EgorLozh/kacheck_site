import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env variables from root directory (parent of frontend)
  const rootDir = path.resolve(__dirname, '..')
  const env = loadEnv(mode, rootDir, '')
  
  // Get backend port from root .env file
  const backendPort = env.BACKEND_PORT || '8000'
  
  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      host: '0.0.0.0', // Allow external connections
      port: parseInt(env.VITE_PORT || '3000', 10),
      proxy: {
        '/api': {
          // In Docker, use backend service name; locally use localhost
          target: env.DOCKER_ENV 
            ? `http://backend:${backendPort}` 
            : `http://localhost:${backendPort}`,
          changeOrigin: true,
        },
      },
    },
  }
})

