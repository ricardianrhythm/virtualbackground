// src/App.js
import React, { useState } from "react";
import Form from "./components/Form";
import "./styles/styles.css"; // Import the styles

function App() {
  const [finalImage, setFinalImage] = useState(null);

  const handleFormSubmit = async (formData) => {
    try {
      const response = await fetch("/api/process", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (result.final_image) {
        setFinalImage(result.final_image);
      } else {
        alert("Error: " + result.error);
      }
    } catch (error) {
      console.error("Error submitting the form:", error);
    }
  };

  return (
    <div className="App">
      <h1>Create Your Custom Image</h1>
      <Form onSubmit={handleFormSubmit} />
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