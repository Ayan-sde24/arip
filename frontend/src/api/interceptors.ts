import type { AxiosInstance, InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "../store/authStore";

let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

export function setupInterceptors(axiosInstance: AxiosInstance) {
  // Request interceptor: attach bearer token
  axiosInstance.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const token = useAuthStore.getState().accessToken;
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response interceptor: handle token refresh on 401
  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;

      if (error.response?.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject });
          })
            .then((token) => {
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${token}`;
              }
              return axiosInstance(originalRequest);
            })
            .catch((err) => Promise.reject(err));
        }

        originalRequest._retry = true;
        isRefreshing = true;

        const refresh = useAuthStore.getState().refreshToken;

        if (!refresh) {
          useAuthStore.getState().logout();
          return Promise.reject(error);
        }

        try {
          const res = await axiosInstance.post("/api/auth/refresh", {
            refresh_token: refresh,
          });

          const { access_token, refresh_token } = res.data;

          useAuthStore.getState().setAccessToken(access_token);
          if (refresh_token) {
            useAuthStore.setState({ refreshToken: refresh_token });
          }

          processQueue(null, access_token);
          isRefreshing = false;

          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
          }
          return axiosInstance(originalRequest);
        } catch (refreshError) {
          processQueue(refreshError, null);
          isRefreshing = false;
          useAuthStore.getState().logout();
          return Promise.reject(refreshError);
        }
      }

      return Promise.reject(error);
    }
  );
}
