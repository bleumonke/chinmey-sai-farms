// src/api.tsx
import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8080",
  headers: {
    "Content-Type": "application/json",
  },
});

// Customers
export const getCustomers = () => api.get("/customers");
export const getCustomer = (customerId: string) => api.get(`/customers/${customerId}`);
export const createCustomer = (data: any) => api.post("/customers", data);
export const updateCustomer = (customerId: string, data: any) => api.patch(`/customers/${customerId}`, data);
export const deleteCustomer = (customerId: string) => api.delete(`/customers/${customerId}`);

// Layouts
export const getLayouts = () => api.get("/layouts");
export const getLayout = (layoutId: string) => api.get(`/layouts/${layoutId}`);
export const createLayout = (data: any) => api.post("/layouts", data);
export const updateLayout = (layoutId: string, data: any) => api.patch(`/layouts/${layoutId}`, data);
export const deleteLayout = (layoutId: string) => api.delete(`/layouts/${layoutId}`);
export const getLayoutPlots = (layoutId: string) => api.get(`/layouts/${layoutId}/plots`);

// Plots
export const getPlots = () => api.get("/plots");
export const getPlot = (plotId: string) => api.get(`/plots/${plotId}`);
export const createPlot = (data: any) => api.post("/plots", data);
export const updatePlot = (plotId: string, data: any) => api.patch(`/plots/${plotId}`, data);
export const deletePlot = (plotId: string) => api.delete(`/plots/${plotId}`);

// Extent Ranges
export const getExtentRanges = () => api.get("/extent_ranges");
export const getExtentRange = (id: string) => api.get(`/extent_ranges/${id}`);
export const createExtentRange = (data: any) => api.post("/extent_ranges", data);
export const updateExtentRange = (id: string, data: any) => api.patch(`/extent_ranges/${id}`, data);
export const deleteExtentRange = (id: string) => api.delete(`/extent_ranges/${id}`);

// Crops
export const getCrops = () => api.get("/crops/");
export const getCrop = (cropId: string) => api.get(`/crops/${cropId}`);
export const createCrop = (data: any) => api.post("/crops/", data);
export const updateCrop = (cropId: string, data: any) => api.patch(`/crops/${cropId}`, data);
export const deleteCrop = (cropId: string) => api.delete(`/crops/${cropId}`);

// Payment Modes
export const getPaymentModes = () => api.get("/payment_modes");
export const getPaymentMode = (id: string) => api.get(`/payment_modes/${id}`);
export const createPaymentMode = (data: any) => api.post("/payment_modes", data);
export const updatePaymentMode = (id: string, data: any) => api.patch(`/payment_modes/${id}`, data);
export const deletePaymentMode = (id: string) => api.delete(`/payment_modes/${id}`);

// Root
export const readRoot = () => api.get("/");

export default api;