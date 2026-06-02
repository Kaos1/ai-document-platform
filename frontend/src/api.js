import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const getAuthHeaders = () => {
  const token = localStorage.getItem("token");

  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
};

export const registerUser = async (email, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/register`, {
    email,
    password,
  });

  return response.data;
};

export const loginUser = async (email, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/login`, {
    email,
    password,
  });

  localStorage.setItem("token", response.data.access_token);

  return response.data;
};

export const logoutUser = () => {
  localStorage.removeItem("token");
};

export const getCurrentUser = async () => {
  const response = await axios.get(`${API_BASE_URL}/auth/me`, {
    headers: getAuthHeaders(),
  });

  return response.data;
};

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(
    `${API_BASE_URL}/documents/upload`,
    formData,
    {
      headers: {
        ...getAuthHeaders(),
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const getDocuments = async () => {
  const response = await axios.get(`${API_BASE_URL}/documents/`, {
    headers: getAuthHeaders(),
  });

  return response.data;
};

export const searchDocuments = async (query) => {
  const response = await axios.get(`${API_BASE_URL}/documents/search/`, {
    params: { query },
    headers: getAuthHeaders(),
  });

  return response.data;
};

export const semanticSearchDocuments = async (query) => {
  const response = await axios.get(`${API_BASE_URL}/documents/semantic-search/`, {
    params: { query },
    headers: getAuthHeaders(),
  });

  return response.data;
};

export const deleteDocument = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/documents/${id}`, {
    headers: getAuthHeaders(),
  });

  return response.data;
};

export const getDownloadUrl = (id) => {
  return `${API_BASE_URL}/documents/${id}/download`;
};