const express = require("express");
const app = express();

app.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "product-service", version: "1.0.0" });
});

app.get("/api/products", (req, res) => {
  res.json({
    products: [
      { id: 1, name: "Widget", price: 9.99 },
      { id: 2, name: "Gadget", price: 24.99 },
    ],
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Product service on port ${PORT}`));

module.exports = app;
