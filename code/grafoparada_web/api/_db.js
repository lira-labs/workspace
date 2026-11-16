'use strict';

/**
 * Helper compartilhado de persistência lazy (Neon Postgres via @neondatabase/serverless)
 * e utilitários HTTP CommonJS para as rotas /api/register, /api/routine e /api/telemetry.
 *
 * - Nunca instancia neon() no import/cold start.
 * - Nunca falha se DATABASE_URL estiver ausente ou se @neondatabase/serverless não estiver instalado.
 */

const crypto = require('crypto');

let _cachedUrl = null;
let _cachedSql = null;
let _schemaReadyPromise = null;

function getDatabaseUrl() {
  return typeof process.env.DATABASE_URL === 'string'
    ? process.env.DATABASE_URL.trim()
    : '';
}

function getSqlClient() {
  const url = getDatabaseUrl();
  if (!url) {
    return null;
  }
  if (_cachedSql && _cachedUrl === url) {
    return _cachedSql;
  }

  let neonFactory;
  try {
    ({ neon: neonFactory } = require('@neondatabase/serverless'));
  } catch (_) {
    return null;
  }

  if (typeof neonFactory !== 'function') {
    return null;
  }

  _cachedUrl = url;
  _cachedSql = neonFactory(url);
  _schemaReadyPromise = null;
  return _cachedSql;
}

async function ensureSchema(sql) {
  if (!sql) return false;
  if (_schemaReadyPromise) {
    return _schemaReadyPromise;
  }

  _schemaReadyPromise = (async () => {
    await sql`
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        contact_hint TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    `;
    await sql`
      CREATE TABLE IF NOT EXISTS routines (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        origin_city TEXT NOT NULL,
        origin_neighborhood TEXT,
        origin_stop_id TEXT,
        origin_stop_name TEXT NOT NULL,
        origin_lat DOUBLE PRECISION,
        origin_lon DOUBLE PRECISION,
        dest_city TEXT NOT NULL,
        dest_neighborhood TEXT,
        dest_stop_id TEXT,
        dest_stop_name TEXT NOT NULL,
        dest_lat DOUBLE PRECISION,
        dest_lon DOUBLE PRECISION,
        departure_time TEXT,
        return_time TEXT,
        preferred_line TEXT,
        frequency TEXT,
        created_at TEXT NOT NULL
      )
    `;
    await sql`
      CREATE TABLE IF NOT EXISTS demand_observations (
        id SERIAL PRIMARY KEY,
        user_id TEXT,
        stop_id TEXT,
        route_code TEXT NOT NULL,
        direction TEXT,
        observed_wait_min DOUBLE PRECISION,
        predicted_wait_min DOUBLE PRECISION,
        occupancy_est INTEGER,
        source TEXT NOT NULL,
        created_at TEXT NOT NULL
      )
    `;
    await sql`
      CREATE TABLE IF NOT EXISTS training_runs (
        id SERIAL PRIMARY KEY,
        dataset_rows INTEGER NOT NULL,
        real_observations INTEGER NOT NULL,
        lines_covered INTEGER NOT NULL,
        stgcn_mae DOUBLE PRECISION NOT NULL,
        ols_mae DOUBLE PRECISION NOT NULL,
        persistence_mae DOUBLE PRECISION NOT NULL,
        weights_hash TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
      )
    `;
    await sql`CREATE INDEX IF NOT EXISTS idx_routines_user_id ON routines (user_id)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_obs_route_code ON demand_observations (route_code)`;
    await sql`CREATE INDEX IF NOT EXISTS idx_obs_created_at ON demand_observations (created_at)`;
    return true;
  })().catch((err) => {
    _schemaReadyPromise = null;
    throw err;
  });

  return _schemaReadyPromise;
}

async function getReadyDb() {
  const url = getDatabaseUrl();
  if (!url) {
    return { sql: null, reason: 'missing_database_url' };
  }
  const sql = getSqlClient();
  if (!sql) {
    return { sql: null, reason: 'driver_unavailable' };
  }
  await ensureSchema(sql);
  return { sql, reason: 'ready' };
}

function sendJson(res, statusCode, payload) {
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(payload));
}

function handleOptions(res, allowedMethods = 'GET, POST, OPTIONS') {
  res.statusCode = 204;
  res.setHeader('Allow', allowedMethods);
  res.end();
}

async function readJsonBody(req) {
  if (req.body !== undefined && req.body !== null) {
    if (typeof req.body === 'object' && !Buffer.isBuffer(req.body)) {
      return req.body;
    }
    const raw = Buffer.isBuffer(req.body) ? req.body.toString('utf8') : String(req.body);
    return raw.trim() ? JSON.parse(raw) : {};
  }

  const chunks = [];
  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  return raw ? JSON.parse(raw) : {};
}

function getQueryParam(req, name) {
  if (req.query && typeof req.query === 'object' && req.query[name] !== undefined) {
    return String(req.query[name]).trim();
  }
  try {
    const parsed = new URL(req.url || '/', 'http://localhost');
    const val = parsed.searchParams.get(name);
    return val ? val.trim() : '';
  } catch (_) {
    return '';
  }
}

function sanitizeText(value, maxLen = 180) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, maxLen);
}

function toNullableText(value, maxLen = 180) {
  if (value === undefined || value === null) return null;
  const cleaned = String(value).trim().slice(0, maxLen);
  return cleaned || null;
}

function toNullableNumber(value) {
  if (value === undefined || value === null || value === '') return null;
  const num = Number(value);
  return Number.isFinite(num) ? num : NaN;
}

function toNullableInt(value) {
  if (value === undefined || value === null || value === '') return null;
  const num = Number.parseInt(String(value), 10);
  return Number.isFinite(num) ? num : NaN;
}

function generateId(prefix) {
  return `${prefix}_${crypto.randomBytes(6).toString('hex')}`;
}

module.exports = {
  getDatabaseUrl,
  getSqlClient,
  ensureSchema,
  getReadyDb,
  sendJson,
  handleOptions,
  readJsonBody,
  getQueryParam,
  sanitizeText,
  toNullableText,
  toNullableNumber,
  toNullableInt,
  generateId
};
