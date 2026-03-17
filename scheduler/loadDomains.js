const fs = require("fs");
const pool = require("../db/db");

async function loadDomains() {

  const domains = [
    "trendsanat.com",
    "google.com",
    "openai.com",
    "amazon.com",
    "microsoft.com"
  ];

  for (const domain of domains) {

    await pool.query(
      `
      INSERT INTO domains (domain, status)
      VALUES ($1, 'pending')
      ON CONFLICT (domain) DO NOTHING
      `,
      [domain]
    );

    console.log("added:", domain);
  }

  process.exit();
}

loadDomains();