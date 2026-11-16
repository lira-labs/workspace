'use strict';

/**
 * Vercel Serverless Function: GET / POST /api/routine
 * Persistência de rotinas diárias de origem/destino (`routines`) no Neon Postgres
 * com degradação graciosa para `client_local` quando DATABASE_URL não estiver configurada.
 */

const {
  getReadyDb,
  sendJson,
  handleOptions,
  readJsonBody,
  getQueryParam,
  sanitizeText,
  toNullableText,
  toNullableNumber,
  generateId
} = require('./_db');

module.exports = async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    handleOptions(res);
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
          routines: []
        });
        return;
      }

      const userId = getQueryParam(req, 'user_id');
      const rows = userId
        ? await sql`
            SELECT * FROM routines
            WHERE user_id = ${userId}
            ORDER BY created_at DESC
            LIMIT 50
          `
        : await sql`
            SELECT * FROM routines
            ORDER BY created_at DESC
            LIMIT 25
          `;

      sendJson(res, 200, {
        ok: true,
        available: true,
        db_configured: true,
        storage: 'neon_postgres',
        routines: rows
      });
    } catch (err) {
      console.error('[api/routine GET] error:', err && err.message ? err.message : err);
      sendJson(res, 503, {
        ok: false,
        available: false,
        db_configured: true,
        reason: 'db_query_error',
        storage: 'client_local',
        routines: []
      });
    }
    return;
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST, OPTIONS');
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

  const userId = sanitizeText(body.user_id, 80);
  const originCity = sanitizeText(body.origin_city, 120);
  const originStopName = sanitizeText(body.origin_stop_name, 180);
  const destCity = sanitizeText(body.dest_city, 120);
  const destStopName = sanitizeText(body.dest_stop_name, 180);

  if (!userId || !originCity || !originStopName || !destCity || !destStopName) {
    sendJson(res, 400, {
      ok: false,
      error: 'missing_required_fields',
      message: 'Campos user_id, origin_city, origin_stop_name, dest_city e dest_stop_name são obrigatórios.'
    });
    return;
  }

  const originLat = toNullableNumber(body.origin_lat);
  const originLon = toNullableNumber(body.origin_lon);
  const destLat = toNullableNumber(body.dest_lat);
  const destLon = toNullableNumber(body.dest_lon);
  if ([originLat, originLon, destLat, destLon].some((v) => Number.isNaN(v))) {
    sendJson(res, 400, { ok: false, error: 'invalid_coordinates' });
    return;
  }

  const routineId = toNullableText(body.id, 80) || generateId('rtn');
  const now = new Date().toISOString();

  const localRecord = {
    id: routineId,
    user_id: userId,
    origin_city: originCity,
    origin_neighborhood: toNullableText(body.origin_neighborhood, 120),
    origin_stop_id: toNullableText(body.origin_stop_id, 64),
    origin_stop_name: originStopName,
    origin_lat: originLat,
    origin_lon: originLon,
    dest_city: destCity,
    dest_neighborhood: toNullableText(body.dest_neighborhood, 120),
    dest_stop_id: toNullableText(body.dest_stop_id, 64),
    dest_stop_name: destStopName,
    dest_lat: destLat,
    dest_lon: destLon,
    departure_time: toNullableText(body.departure_time, 16),
    return_time: toNullableText(body.return_time, 16),
    preferred_line: toNullableText(body.preferred_line, 32),
    frequency: toNullableText(body.frequency, 32),
    created_at: now
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
        record: localRecord
      });
      return;
    }

    const rows = await sql`
      INSERT INTO routines (
        id, user_id, origin_city, origin_neighborhood, origin_stop_id,
        origin_stop_name, origin_lat, origin_lon, dest_city,
        dest_neighborhood, dest_stop_id, dest_stop_name, dest_lat,
        dest_lon, departure_time, return_time, preferred_line,
        frequency, created_at
      ) VALUES (
        ${localRecord.id}, ${localRecord.user_id}, ${localRecord.origin_city},
        ${localRecord.origin_neighborhood}, ${localRecord.origin_stop_id},
        ${localRecord.origin_stop_name}, ${localRecord.origin_lat}, ${localRecord.origin_lon},
        ${localRecord.dest_city}, ${localRecord.dest_neighborhood}, ${localRecord.dest_stop_id},
        ${localRecord.dest_stop_name}, ${localRecord.dest_lat}, ${localRecord.dest_lon},
        ${localRecord.departure_time}, ${localRecord.return_time}, ${localRecord.preferred_line},
        ${localRecord.frequency}, ${localRecord.created_at}
      )
      ON CONFLICT (id) DO UPDATE SET
        user_id = EXCLUDED.user_id,
        origin_city = EXCLUDED.origin_city,
        origin_neighborhood = EXCLUDED.origin_neighborhood,
        origin_stop_id = EXCLUDED.origin_stop_id,
        origin_stop_name = EXCLUDED.origin_stop_name,
        origin_lat = EXCLUDED.origin_lat,
        origin_lon = EXCLUDED.origin_lon,
        dest_city = EXCLUDED.dest_city,
        dest_neighborhood = EXCLUDED.dest_neighborhood,
        dest_stop_id = EXCLUDED.dest_stop_id,
        dest_stop_name = EXCLUDED.dest_stop_name,
        dest_lat = EXCLUDED.dest_lat,
        dest_lon = EXCLUDED.dest_lon,
        departure_time = EXCLUDED.departure_time,
        return_time = EXCLUDED.return_time,
        preferred_line = EXCLUDED.preferred_line,
        frequency = EXCLUDED.frequency
      RETURNING *
    `;

    sendJson(res, 201, {
      ok: true,
      persisted: 'neon_postgres',
      db_configured: true,
      available: true,
      storage: 'neon_postgres',
      record: rows[0] || localRecord
    });
  } catch (err) {
    console.error('[api/routine POST] error:', err && err.message ? err.message : err);
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
