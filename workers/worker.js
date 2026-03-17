// workers/worker.js
const axios = require("axios");
const pool = require("../db/db");

// .com için Verisign RDAP
const RDAP_COM = "https://rdap.verisign.com/com/v1/domain/";

// Rate limit (ms). PowerShell'de set etmek için:
// $env:RDAP_MIN_INTERVAL_MS="250"; node workers/worker.js
const MIN_INTERVAL_MS = parseInt(process.env.RDAP_MIN_INTERVAL_MS || "250", 10);
let lastCall = 0;

async function rateLimit() {
  const now = Date.now();
  const wait = Math.max(0, MIN_INTERVAL_MS - (now - lastCall));
  if (wait) await new Promise((r) => setTimeout(r, wait));
  lastCall = Date.now();
}

function pickExpirationEvent(rdapJson) {
  if (!rdapJson || !Array.isArray(rdapJson.events)) return null;
  return rdapJson.events.find((e) => e && e.eventAction === "expiration") || null;
}

function computeNextCheck(expireAt, status) {
  const hour = 60 * 60 * 1000;
  const day = 24 * hour;

  // available yakaladıysan sık kontrol etmeye gerek yok; ama istersen sıklaştırabilirsin
  if (status === "available") return new Date(Date.now() + 12 * hour);

  // hata olduysa biraz sonra tekrar dene
  if (!expireAt) return new Date(Date.now() + 24 * hour);

  const ms = expireAt.getTime() - Date.now();

  if (ms > 180 * day) return new Date(Date.now() + 30 * day);
  if (ms > 60 * day) return new Date(Date.now() + 7 * day);
  if (ms > 14 * day) return new Date(Date.now() + 1 * day);
  if (ms > 3 * day) return new Date(Date.now() + 6 * hour);
  return new Date(Date.now() + 2 * hour);
}

async function lockOneDomain() {
  // DB kuyruğu: sıradaki domaini "locked_at" ile kap
  // locked_at 10 dakikadan eskiyse (crash vs) tekrar işlenebilir.
  const sql = `
    UPDATE domains
    SET locked_at = NOW()
    WHERE id = (
      SELECT id
      FROM domains
      WHERE (next_check_at IS NULL OR next_check_at <= NOW())
        AND (locked_at IS NULL OR locked_at < NOW() - INTERVAL '10 minutes')
      ORDER BY next_check_at NULLS FIRST, id
      LIMIT 1
      FOR UPDATE SKIP LOCKED
    )
    RETURNING id, domain
  `;
  const res = await pool.query(sql);
  return res.rows[0] || null;
}

async function saveResult(id, { expireAt, status, nextCheckAt, lastError }) {
  const sql = `
    UPDATE domains
    SET expire_at = $1,
        status = $2,
        last_checked = NOW(),
        next_check_at = $3,
        locked_at = NULL,
        last_error = $4
    WHERE id = $5
  `;
  await pool.query(sql, [expireAt, status, nextCheckAt, lastError || null, id]);
}

async function checkDomain(domain) {
  const url = `${RDAP_COM}${domain}`;

  // Rate limit mutlaka burada (axios'tan önce)
  await rateLimit();

  try {
    const { data } = await axios.get(url, { timeout: 15000 });
    const exp = pickExpirationEvent(data);
    const expireAt = exp ? new Date(exp.eventDate) : null;

    // Verisign RDAP response içinde status alanı olabilir ama biz şimdilik sabitliyoruz
    const status = "active";
    const nextCheckAt = computeNextCheck(expireAt, status);

    return {
      ok: true,
      expireAt,
      status,
      nextCheckAt,
      lastError: null,
      expRaw: exp ? exp.eventDate : null,
    };
  } catch (err) {
    const http = err?.response?.status;
    const code = http || err?.code || "unknown";

    // Verisign RDAP'ta bulunmayan domain genelde 404 => "available" diye yorumlayabiliriz
    if (http === 404) {
      const status = "available";
      const nextCheckAt = computeNextCheck(null, status);
      return { ok: true, expireAt: null, status, nextCheckAt, lastError: null, expRaw: null };
    }

    const status = `error:${code}`;
    const nextCheckAt = new Date(Date.now() + 6 * 60 * 60 * 1000); // 6 saat sonra tekrar dene
    return {
      ok: false,
      expireAt: null,
      status,
      nextCheckAt,
      lastError: String(code),
      expRaw: null,
    };
  }
}

async function runOnce() {
  const job = await lockOneDomain();
  if (!job) return false;

  const { id, domain } = job;

  const result = await checkDomain(domain);

  if (result.status === "active") {
    console.log(
      `[OK] ${domain} exp=${result.expRaw || "n/a"} next=${result.nextCheckAt.toISOString()} (minInterval=${MIN_INTERVAL_MS}ms)`
    );
  } else if (result.status === "available") {
    console.log(`[DROP?] ${domain} AVAILABLE next=${result.nextCheckAt.toISOString()} (minInterval=${MIN_INTERVAL_MS}ms)`);
  } else {
    console.log(`[ERR] ${domain} ${result.status} next=${result.nextCheckAt.toISOString()} (minInterval=${MIN_INTERVAL_MS}ms)`);
  }

  await saveResult(id, {
    expireAt: result.expireAt,
    status: result.status,
    nextCheckAt: result.nextCheckAt,
    lastError: result.lastError,
  });

  return true;
}

async function main() {
  while (true) {
    const didWork = await runOnce();
    if (!didWork) {
      console.log("Queue empty (for now). Sleeping 10s...");
      await new Promise((r) => setTimeout(r, 10_000));
    }
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});