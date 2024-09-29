// src/components/Form.js
import React, { useState } from "react";

const Form = () => {
  const [movie, setMovie] = useState("");
  const [book, setBook] = useState("");
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("movie", movie);
    formData.append("book", book);
    formData.append("file", file);

    const response = await fetch("/api/process", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    // Handle displaying the result, maybe set state with image URL
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Favorite Movie:
        <input type="text" value={movie} onChange={(e) => setMovie(e.target.value)} />
      </label>
      <label>
        Favorite Book:
        <input type="text" value={book} onChange={(e) => setBook(e.target.value)} />
      </label>
      <label>
        Upload a photo:
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default Form;