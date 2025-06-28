import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000/api", // ✅ Important: Must match your backend
});

export default API;
