import { axiosInstance } from "./axios";
import { setupInterceptors } from "./interceptors";

setupInterceptors(axiosInstance);

export default axiosInstance;
export { axiosInstance as api };
