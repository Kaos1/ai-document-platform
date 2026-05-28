import { useEffect, useState } from "react";
import {
  uploadDocument,
  getDocuments,
  searchDocuments,
  semanticSearchDocuments,
  deleteDocument,
  getDownloadUrl,
} from "./api";
import "./App.css";

function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const loadDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error(error);
      setMessage("Failed to load documents.");
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleUpload = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setMessage("Please choose a file first.");
      return;
    }

    try {
      setLoading(true);
      setMessage("Uploading and processing document...");

      await uploadDocument(selectedFile);

      setSelectedFile(null);
      setMessage("Document uploaded successfully.");
      await loadDocuments();
    } catch (error) {
      console.error(error);
      setMessage("Upload failed. Check your backend terminal for errors.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeywordSearch = async () => {
    if (!searchQuery.trim()) {
      await loadDocuments();
      return;
    }

    try {
      setLoading(true);
      const data = await searchDocuments(searchQuery);
      setDocuments(data);
      setMessage(`Keyword search completed for: ${searchQuery}`);
    } catch (error) {
      console.error(error);
      setMessage("Keyword search failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleSemanticSearch = async () => {
    if (!searchQuery.trim()) {
      await loadDocuments();
      return;
    }

    try {
      setLoading(true);
      const data = await semanticSearchDocuments(searchQuery);
      setDocuments(data);
      setMessage(`Semantic search completed for: ${searchQuery}`);
    } catch (error) {
      console.error(error);
      setMessage("Semantic search failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteDocument(id);
      setMessage("Document deleted successfully.");
      await loadDocuments();
    } catch (error) {
      console.error(error);
      setMessage("Delete failed.");
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <h1>AI Document Management Platform</h1>
        <p>
          Upload documents, extract text, generate summaries and tags, and search
          by keyword or meaning.
        </p>
      </header>

      <section className="card">
        <h2>Upload Document</h2>

        <form onSubmit={handleUpload} className="upload-form">
          <input
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={(event) => setSelectedFile(event.target.files[0])}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Processing..." : "Upload"}
          </button>
        </form>

        {message && <p className="message">{message}</p>}
      </section>

      <section className="card">
        <h2>Search Documents</h2>

        <div className="search-row">
          <input
            type="text"
            placeholder="Search by keyword or meaning..."
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
          />

          <button onClick={handleKeywordSearch} disabled={loading}>
            Keyword Search
          </button>

          <button onClick={handleSemanticSearch} disabled={loading}>
            Semantic Search
          </button>

          <button onClick={loadDocuments} disabled={loading}>
            Reset
          </button>
        </div>
      </section>

      <section className="documents">
        <h2>Uploaded Documents</h2>

        {documents.length === 0 ? (
          <p>No documents found.</p>
        ) : (
          <div className="document-grid">
            {documents.map((document) => (
              <article key={document.id} className="document-card">
                <h3>{document.original_filename}</h3>

                <p>
                  <strong>Type:</strong> {document.content_type}
                </p>

                <p>
                  <strong>Uploaded:</strong>{" "}
                  {new Date(document.created_at).toLocaleString()}
                </p>

                {document.tags && (
                  <p>
                    <strong>Tags:</strong> {document.tags}
                  </p>
                )}

                {document.summary && (
                  <div>
                    <strong>Summary:</strong>
                    <p>{document.summary}</p>
                  </div>
                )}

                {document.extracted_text && (
                  <details>
                    <summary>View extracted text</summary>
                    <p className="extracted-text">{document.extracted_text}</p>
                  </details>
                )}

                <div className="actions">
                  <a
                    href={getDownloadUrl(document.id)}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Download
                  </a>

                  <button onClick={() => handleDelete(document.id)}>
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default App;