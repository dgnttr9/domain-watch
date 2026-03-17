const axios = require("axios");
const pool = require("../db/db");

// .com için Verisign RDAP
const RDAP_COM = "https://rdap.verisign.com/com/v1/domain/";

function pickExpirationEvent(rdapJson) {
  if (!rdapJson || !Array.isArray(rdapJson.events)) return null;
  return rdapJson.events.find((e) => e && e.eventAction === "expiration") || null;
}

async function upsertDomain({ domain, expireAt, status }) {
  const sql = `
    INSERT INTO domains (domain, expire_at, status, last_checked)
    VALUES ($1, $2, $3, NOW())
    ON CONFLICT (domain)
    DO UPDATE SET expire_at = EXCLUDED.expire_at,
                  status = EXCLUDED.status,
                  last_checked = NOW()
  `;
  await pool.query(sql, [domain, expireAt, status]);
}

async function checkDomain(domain) {
  const url = `${RDAP_COM}${domain}`;

  try {
    const { data } = await axios.get(url, { timeout: 15000 });
    const exp = pickExpirationEvent(data);

    const expireAt = exp ? new Date(exp.eventDate) : null;
    const status = "active"; // şimdilik basit tutuyoruz

    console.log("Domain:", domain);
    console.log("Expiration:", exp ? exp.eventDate : "not found");

    await upsertDomain({ domain, expireAt, status });
    console.log("DB: upsert OK");
  } catch (err) {
    const code = err?.response?.status || err?.code || "unknown";
    console.log("Error checking domain:", domain, "code:", code);

    // Hata durumunu da DB'ye yazalım (expire null)
    try {
      await upsertDomain({ domain, expireAt: null, status: `error:${code}` });
      console.log("DB: upsert error status OK");
    } catch (dbErr) {
      console.log("DB error:", dbErr.message);
    }
  }
}

checkDomain("trendsanat.com")
  .then(() => process.exit(0))
  .catch(() => process.exit(1));