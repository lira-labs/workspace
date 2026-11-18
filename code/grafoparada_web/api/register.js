'use strict';

/**
 * Vercel Serverless Function: GET / POST /api/register
 * Cadastro leve LGPD (sem CPF) persistido em Neon Postgres quando DATABASE_URL existir,
 * com degradação graciosa para armazenamento local (`client_local`).
 */

const {
  getReadyDb,
  sendJson,
  handleOptions,
  readJsonBody,
  getQueryParam,
  sanitizeText,
  toNullableText,
  generateId
} = require('./_db');

module.exports = async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    handleOptions(res, 'GET, POST, DELETE, OPTIONS');
    return;
  }

  if (req.method === 'GET') {
    try {
      const { sql, reason } = await getReadyDb();
      if (!sql) {
        sendJson(res, 200, {
          ok: true,
          available: false,
          db_configured: false,
          reason,
          storage: 'client_local',
          user: null
        });
        return;
      }

      const userId = getQueryParam(req, 'user_id');
      if (userId) {
        const rows = await sql`
          SELECT id, name, contact_hint, consent_at, created_at, updated_at
          FROM users
          WHERE id = ${userId}
          LIMIT 1
        `;
        sendJson(res, 200, {
          ok: true,
          available: true,
          db_configured: true,
          storage: 'neon_postgres',
          user: rows[0] || null
        });
        return;
      }

      const contactHint = getQueryParam(req, 'contact_hint');
      if (contactHint.length >= 3) {
        const rows = await sql`
          SELECT id, name, contact_hint, consent_at, created_at, updated_at
          FROM users
          WHERE LOWER(TRIM(contact_hint)) = LOWER(TRIM(${contactHint}))
          ORDER BY updated_at DESC
          LIMIT 1
        `;
        sendJson(res, 200, {
          ok: true,
          available: true,
          db_configured: true,
          storage: 'neon_postgres',
          user: rows[0] || null
        });
        return;
      }

      const countRows = await sql`SELECT COUNT(*)::int AS total FROM users`;
      sendJson(res, 200, {
        ok: true,
        available: true,
        db_configured: true,
        storage: 'neon_postgres',
        users_count: Number(countRows[0] && countRows[0].total) || 0
      });
    } catch (err) {
      console.error('[api/register GET] error:', err && err.message ? err.message : err);
      sendJson(res, 503, {
        ok: false,
        available: false,
        db_configured: true,
        reason: 'db_query_error',
        storage: 'client_local'
      });
    }
    return;
  }

  if (req.method === 'DELETE') {
    const userId = getQueryParam(req, 'user_id');
    if (!userId) {
      sendJson(res, 400, {
        ok: false,
        error: 'missing_user_id',
        message: 'Informe user_id para exclusão LGPD.'
      });
      return;
    }

    try {
      const { sql, reason } = await getReadyDb();
      if (!sql) {
        sendJson(res, 200, {
          ok: true,
          deleted: false,
          available: false,
          db_configured: false,
          reason,
          storage: 'client_local',
          user_id: userId
        });
        return;
      }

      const deletedRoutines = await sql`
        DELETE FROM routines WHERE user_id = ${userId} RETURNING id
      `;
      const deletedUsers = await sql`
        DELETE FROM users WHERE id = ${userId} RETURNING id
      `;

      sendJson(res, 200, {
        ok: true,
        available: true,
        db_configured: true,
        storage: 'neon_postgres',
        deleted: deletedUsers.length > 0,
        user_id: userId,
        deleted_users: deletedUsers.length,
        deleted_routines: deletedRoutines.length
      });
    } catch (err) {
      console.error('[api/register DELETE] error:', err && err.message ? err.message : err);
      sendJson(res, 503, {
        ok: false,
        available: false,
        db_configured: true,
        reason: 'db_query_error',
        storage: 'client_local'
      });
    }
    return;
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST, DELETE, OPTIONS');
    sendJson(res, 405, { ok: false, error: 'method_not_allowed' });
    return;
  }

  let body;
  try {
    body = await readJsonBody(req);
  } catch (_) {
    sendJson(res, 400, { ok: false, error: 'invalid_json' });
    return;
  }

  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    sendJson(res, 400, { ok: false, error: 'invalid_request' });
    return;
  }

  const name = sanitizeText(body.name, 120);
  if (name.length < 2) {
    sendJson(res, 400, {
      ok: false,
      error: 'invalid_name',
      message: 'Informe um nome ou apelido com pelo menos 2 caracteres.'
    });
    return;
  }

  const contactHint = toNullableText(body.contact_hint, 120);
  const explicitUserId = toNullableText(body.user_id || body.id, 80);
  let userId = explicitUserId || generateId('usr');
  const now = new Date().toISOString();
  const consentAt =
    toNullableText(body.consent_at, 64) ||
    (body.consent === true || body.lgpd_consent === true ? now : null);

  const localRecord = {
    id: userId,
    name,
    contact_hint: contactHint,
    consent_at: consentAt,
    created_at: now,
    updated_at: now
  };

  try {
    const { sql, reason } = await getReadyDb();
    if (!sql) {
      sendJson(res, 202, {
        ok: true,
        persisted: 'client_local_pending_db',
        db_configured: false,
        available: false,
        storage: 'client_local',
        reason,
        record: localRecord,
        user: localRecord
      });
      return;
    }

    if (!explicitUserId && contactHint && contactHint.length >= 3) {
      const existing = await sql`
        SELECT id
        FROM users
        WHERE LOWER(TRIM(contact_hint)) = LOWER(TRIM(${contactHint}))
        ORDER BY updated_at DESC
        LIMIT 1
      `;
      if (existing[0] && existing[0].id) {
        userId = existing[0].id;
      }
    }

    const rows = await sql`
      INSERT INTO users (id, name, contact_hint, consent_at, created_at, updated_at)
      VALUES (${userId}, ${name}, ${contactHint}, ${consentAt}, ${now}, ${now})
      ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        contact_hint = EXCLUDED.contact_hint,
        consent_at = COALESCE(EXCLUDED.consent_at, users.consent_at),
        updated_at = EXCLUDED.updated_at
      RETURNING id, name, contact_hint, consent_at, created_at, updated_at
    `;

    const saved = rows[0] || localRecord;
    sendJson(res, 201, {
      ok: true,
      persisted: 'neon_postgres',
      db_configured: true,
      available: true,
      storage: 'neon_postgres',
      record: saved,
      user: saved
    });
  } catch (err) {
    console.error('[api/register POST] error:', err && err.message ? err.message : err);
    sendJson(res, 503, {
      ok: false,
      persisted: 'client_local_pending_db',
      db_configured: true,
      available: false,
      storage: 'client_local',
      reason: 'db_query_error',
      record: localRecord
    });
  }
};
