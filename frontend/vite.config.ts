import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "/api": {
        target:
          // 開発時は、この API Gateway の ID を埋めてください。
          // 本番環境では、Nginx を使用してデプロイするのでこのファイルは使用しません。
          "https://<API Gateway の ID>.execute-api.ap-northeast-1.amazonaws.com/prod",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  build: {
    outDir: "dist",
  },
});
