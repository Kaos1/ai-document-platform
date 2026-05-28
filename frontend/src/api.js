import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(
    `${API_BASE_URL}/documents/upload`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const getDocuments = async () => {
  const response = await axios.get(`${API_BASE_URL}/documents/`);
  return response.data;
};

export const searchDocuments = async (query) => {
  const response = await axios.get(`${API_BASE_URL}/documents/search/`, {
    params: { query },
  });

  return response.data;
};

export const semanticSearchDocuments = async (query) => {
  const response = await axios.get(`${API_BASE_URL}/documents/semantic-search/`, {
    params: { query },
  });

  return response.data;
};

export const deleteDocument = async (id) => {
  const response = await axios.delete(`${API_BASE_URL}/documents/${id}`);
  return response.data;
};

export const getDownloadUrl = (id) => {
  return `${API_BASE_URL}/documents/${id}/download`;
};