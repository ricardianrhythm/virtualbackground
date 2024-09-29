import React, { useState } from "react";
import Form from "./components/Form";
import "./styles/styles.css"; // Import the styles

function App() {
  const [finalImage, setFinalImage] = useState(null);
  const [loading, setLoading] = useState(false); // Add loading state
  const [error, setError] = useState(null); // Add error state

  const handleFormSubmit = async (formData) => {
    setLoading(true); // Set loading to true
    setError(null); // Reset error before a new submission

    try {
      const response = await fetch("/api/process", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.final_image) {
        setFinalImage(result.final_image);
      } else {
        setError("Error: " + result.error); // Set error in state instead of alert
      }
    } catch (error) {
      console.error("Error submitting the form:", error);
      setError("An unexpected error occurred. Please try again."); // Set generic error message
    } finally {
      setLoading(false); // Stop loading after fetch
    }
  };

  return (
    <div className="App">
      <h1>Create Your Custom Image</h1>
      
      {/* Display loading message */}
      {loading && <p>Processing...</p>}

      {/* Render form */}
      {!loading && <Form onSubmit={handleFormSubmit} />}

      {/* Display error if present */}
      {error && <p className="error">{error}</p>}

      {/* Render the final image if it's available */}
      {finalImage && (
        <div className="result">
          <h2>Your Final Image:</h2>
          <img src={finalImage} alt="Final Image" />
        </div>
      )}
    </div>
  );
}

export default App;