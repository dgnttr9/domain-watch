const fs = require("fs");
const readline = require("readline");
const pool = require("../db/db");

const FILE = process.env.DOMAIN_FILE || "domains.txt";
const BATCH = parseInt(process.env.BATCH || "5000", 10);

function normalize(d) {
  return d.trim().toLowerCase();
}

async function insertBatch(domains) {
  // multi-values insert
  const values = [];
  const params = [];
  let i = 1;
  for (const d of domains) {
    values.push(`($${i++}, 'pending', NOW())`);
    params.push(d);
  }

  const sql = `
    INSERT INTO domains (domain, status, next_check_at)
    VALUES ${values.join(",")}
    ON CONFLICT (domain) DO NOTHING
  `;
  await pool.query(sql, params);
}

async function main() {
  if (!fs.existsSync(FILE)) {
    console.error(`File not found: ${FILE}`);
    process.exit(1);
  }

  const rl = readline.createInterface({
    input: fs.createReadStream(FILE, { encoding: "utf8" }),
    crlfDelay: Infinity,
  });

  let buf = [];
  let total = 0;

  for await (const line of rl) {
    const d = normalize(line);
    if (!d) continue;
    buf.push(d);

    if (buf.length >= BATCH) {
      await insertBatch(buf);
      total += buf.length;
      console.log(`inserted (or skipped duplicates): ${total}`);
      buf = [];
    }
  }

  if (buf.length) {
    await insertBatch(buf);
    total += buf.length;
    console.log(`inserted (or skipped duplicates): ${total}`);
  }

  console.log("done.");
  process.exit(0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});