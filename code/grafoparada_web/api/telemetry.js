'use strict';

/**
 * Vercel Serverless Function: GET / POST /api/telemetry
 * Coleta observações reais de espera/lotação (`demand_observations`) e expõe
 * métricas agregadas e último ciclo de treino (`training_runs`) para o GrafoParada.
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
  toNullableInt,
  toNullableBool,
  toNullableIso
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
          counts: {
            users: 0,
            routines: 0,
            demand_observations: 0,
            training_runs: 0
          },
          latest_training_run: null,
          recent_observations: []
        });
        return;
      }

      const routeCode = getQueryParam(req, 'route_code');
      const sinceIso = toNullableIso(getQueryParam(req, 'since'));
      const rawLimit = toNullableInt(getQueryParam(req, 'limit'));
      const limit = Number.isFinite(rawLimit) && rawLimit >= 1 ? Math.min(rawLimit, 500) : 100;

      let obsQuery;
      if (routeCode && sinceIso) {
        obsQuery = sql`
          SELECT * FROM demand_observations
          WHERE route_code = ${routeCode} AND created_at >= ${sinceIso}
          ORDER BY id DESC
          LIMIT ${limit}
        `;
      } else if (routeCode) {
        obsQuery = sql`
          SELECT * FROM demand_observations
          WHERE route_code = ${routeCode}
          ORDER BY id DESC
          LIMIT ${limit}
        `;
      } else if (sinceIso) {
        obsQuery = sql`
          SELECT * FROM demand_observations
          WHERE created_at >= ${sinceIso}
          ORDER BY id DESC
          LIMIT ${limit}
        `;
      } else {
        obsQuery = sql`
          SELECT * FROM demand_observations
          ORDER BY id DESC
          LIMIT ${limit}
        `;
      }

      const [userCnt, routineCnt, obsCnt, runCnt, latestRunRows, obsRows] = await Promise.all([
        sql`SELECT COUNT(*)::int AS total FROM users`,
        sql`SELECT COUNT(*)::int AS total FROM routines`,
        sql`SELECT COUNT(*)::int AS total FROM demand_observations`,
        sql`SELECT COUNT(*)::int AS total FROM training_runs`,
        sql`SELECT * FROM training_runs ORDER BY id DESC LIMIT 1`,
        obsQuery
      ]);

      sendJson(res, 200, {
        ok: true,
        available: true,
        db_configured: true,
        storage: 'neon_postgres',
        counts: {
          users: Number(userCnt[0] && userCnt[0].total) || 0,
          routines: Number(routineCnt[0] && routineCnt[0].total) || 0,
          demand_observations: Number(obsCnt[0] && obsCnt[0].total) || 0,
          training_runs: Number(runCnt[0] && runCnt[0].total) || 0
        },
        latest_training_run: latestRunRows[0] || null,
        recent_observations: obsRows
      });
    } catch (err) {
      console.error('[api/telemetry GET] error:', err && err.message ? err.message : err);
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

  if (sanitizeText(body.kind, 40) === 'training_run') {
    const expectedSyncToken =
      typeof process.env.GRAFOPARADA_SYNC_TOKEN === 'string'
        ? process.env.GRAFOPARADA_SYNC_TOKEN.trim()
        : '';
    if (expectedSyncToken) {
      const headerToken = req.headers
        ? req.headers['x-sync-token'] || req.headers['X-Sync-Token']
        : '';
      const rawHeaderToken = Array.isArray(headerToken) ? headerToken[0] : headerToken;
      const providedToken = sanitizeText(
        rawHeaderToken || body.sync_token || '',
        256
      );
      if (!providedToken || providedToken !== expectedSyncToken) {
        sendJson(res, 401, {
          ok: false,
          error: 'unauthorized',
          message: 'Sync token inválido ou ausente.'
        });
        return;
      }
    }

    const weightsHash = sanitizeText(body.weights_hash, 128);
    const stgcnMae = toNullableNumber(body.stgcn_mae);
    if (!weightsHash || stgcnMae === null || Number.isNaN(stgcnMae) || stgcnMae < 0) {
      sendJson(res, 400, {
        ok: false,
        error: 'invalid_training_run',
        message: 'Campos weights_hash e stgcn_mae numéricos válidos são obrigatórios.'
      });
      return;
    }

    const datasetRows =
      body.dataset_rows !== undefined && body.dataset_rows !== null && body.dataset_rows !== ''
        ? toNullableInt(body.dataset_rows)
        : 0;
    const realObservations =
      body.real_observations !== undefined && body.real_observations !== null && body.real_observations !== ''
        ? toNullableInt(body.real_observations)
        : 0;
    const linesCovered =
      body.lines_covered !== undefined && body.lines_covered !== null && body.lines_covered !== ''
        ? toNullableInt(body.lines_covered)
        : 0;
    const olsMae =
      body.ols_mae !== undefined && body.ols_mae !== null && body.ols_mae !== ''
        ? toNullableNumber(body.ols_mae)
        : 0;
    const persistenceMae =
      body.persistence_mae !== undefined && body.persistence_mae !== null && body.persistence_mae !== ''
        ? toNullableNumber(body.persistence_mae)
        : 0;

    if (
      Number.isNaN(datasetRows) ||
      Number.isNaN(realObservations) ||
      Number.isNaN(linesCovered) ||
      Number.isNaN(olsMae) ||
      Number.isNaN(persistenceMae) ||
      datasetRows < 0 ||
      realObservations < 0 ||
      linesCovered < 0 ||
      olsMae < 0 ||
      persistenceMae < 0
    ) {
      sendJson(res, 400, { ok: false, error: 'invalid_metrics' });
      return;
    }

    const localTrainingRun = {
      dataset_rows: datasetRows,
      real_observations: realObservations,
      lines_covered: linesCovered,
      stgcn_mae: stgcnMae,
      ols_mae: olsMae,
      persistence_mae: persistenceMae,
      weights_hash: weightsHash,
      notes: toNullableText(body.notes, 500),
      created_at: toNullableIso(body.created_at) || new Date().toISOString()
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
          kind: 'training_run',
          reason,
          training_run: localTrainingRun
        });
        return;
      }

      const rows = await sql`
        INSERT INTO training_runs (
          dataset_rows, real_observations, lines_covered,
          stgcn_mae, ols_mae, persistence_mae,
          weights_hash, notes, created_at
        ) VALUES (
          ${localTrainingRun.dataset_rows},
          ${localTrainingRun.real_observations},
          ${localTrainingRun.lines_covered},
          ${localTrainingRun.stgcn_mae},
          ${localTrainingRun.ols_mae},
          ${localTrainingRun.persistence_mae},
          ${localTrainingRun.weights_hash},
          ${localTrainingRun.notes},
          ${localTrainingRun.created_at}
        )
        RETURNING *
      `;

      sendJson(res, 201, {
        ok: true,
        persisted: 'neon_postgres',
        db_configured: true,
        available: true,
        storage: 'neon_postgres',
        kind: 'training_run',
        training_run: rows[0] || localTrainingRun
      });
    } catch (err) {
      console.error('[api/telemetry POST training_run] error:', err && err.message ? err.message : err);
      sendJson(res, 503, {
        ok: false,
        persisted: 'client_local_pending_db',
        db_configured: true,
        available: false,
        storage: 'client_local',
        kind: 'training_run',
        reason: 'db_query_error',
        training_run: localTrainingRun
      });
    }
    return;
  }

  const eventType = sanitizeText(body.event_type, 80);
  if (eventType) {
    let payloadJson = null;
    if (typeof body.payload_json === 'string') {
      payloadJson = toNullableText(body.payload_json, 8000);
    } else if (body.payload !== undefined && body.payload !== null) {
      try {
        payloadJson = JSON.stringify(body.payload).slice(0, 8000);
      } catch (_) {
        payloadJson = null;
      }
    }

    const localEvent = {
      user_id: toNullableText(body.user_id, 80),
      event_type: eventType,
      route_code: toNullableText(body.route_code, 32),
      stop_id: toNullableText(body.stop_id, 64),
      payload_json: payloadJson,
      created_at: new Date().toISOString()
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
          record: localEvent
        });
        return;
      }

      const rows = await sql`
        INSERT INTO app_events (
          user_id, event_type, route_code, stop_id, payload_json, created_at
        ) VALUES (
          ${localEvent.user_id}, ${localEvent.event_type}, ${localEvent.route_code},
          ${localEvent.stop_id}, ${localEvent.payload_json}, ${localEvent.created_at}
        )
        RETURNING *
      `;

      sendJson(res, 201, {
        ok: true,
        persisted: 'neon_postgres',
        db_configured: true,
        available: true,
        storage: 'neon_postgres',
        record: rows[0] || localEvent
      });
    } catch (err) {
      console.error('[api/telemetry POST event] error:', err && err.message ? err.message : err);
      sendJson(res, 503, {
        ok: false,
        persisted: 'client_local_pending_db',
        db_configured: true,
        available: false,
        storage: 'client_local',
        reason: 'db_query_error',
        record: localEvent
      });
    }
    return;
  }

  const routeCode = sanitizeText(body.route_code, 32);
  const source = sanitizeText(body.source, 80);
  if (!routeCode || !source) {
    sendJson(res, 400, {
      ok: false,
      error: 'missing_required_fields',
      message: 'Campos route_code e source são obrigatórios.'
    });
    return;
  }

  const observedWait = toNullableNumber(body.observed_wait_min);
  const predictedWait = toNullableNumber(body.predicted_wait_min);
  const occupancyEst = toNullableInt(body.occupancy_est);
  const delayMin = toNullableNumber(body.delay_min);

  if (
    Number.isNaN(observedWait) ||
    Number.isNaN(predictedWait) ||
    Number.isNaN(occupancyEst) ||
    Number.isNaN(delayMin) ||
    (observedWait !== null && observedWait < 0) ||
    (predictedWait !== null && predictedWait < 0) ||
    (occupancyEst !== null && (occupancyEst < 0 || occupancyEst > 100))
  ) {
    sendJson(res, 400, { ok: false, error: 'invalid_metrics' });
    return;
  }

  const now = new Date().toISOString();
  const rawNotes = body.notes !== undefined && body.notes !== null ? body.notes : body.label;
  const localRecord = {
    user_id: toNullableText(body.user_id, 80),
    stop_id: toNullableText(body.stop_id, 64),
    route_code: routeCode,
    direction: toNullableText(body.direction, 24),
    observed_wait_min: observedWait,
    predicted_wait_min: predictedWait,
    occupancy_est: occupancyEst,
    delay_min: delayMin,
    wait_report_type: toNullableText(body.wait_report_type, 64),
    ti_hub_id: toNullableText(body.ti_hub_id, 64),
    transfer_ok: toNullableBool(body.transfer_ok),
    notes: toNullableText(rawNotes, 500),
    source,
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
      INSERT INTO demand_observations (
        user_id, stop_id, route_code, direction,
        observed_wait_min, predicted_wait_min, occupancy_est,
        delay_min, wait_report_type, ti_hub_id, transfer_ok, notes,
        source, created_at
      ) VALUES (
        ${localRecord.user_id}, ${localRecord.stop_id}, ${localRecord.route_code},
        ${localRecord.direction}, ${localRecord.observed_wait_min}, ${localRecord.predicted_wait_min},
        ${localRecord.occupancy_est}, ${localRecord.delay_min}, ${localRecord.wait_report_type},
        ${localRecord.ti_hub_id}, ${localRecord.transfer_ok}, ${localRecord.notes},
        ${localRecord.source}, ${localRecord.created_at}
      )
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
    console.error('[api/telemetry POST] error:', err && err.message ? err.message : err);
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
