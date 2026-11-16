'use strict';

/**
 * Vercel Serverless Function: POST /api/tts
 * Proxy seguro para síntese de voz da assistente Laya via Gemini TTS.
 * - Mantém GEMINI_API_KEY estritamente no servidor (header x-goog-api-key).
 * - Degrada graciosamente (HTTP 501 / 503) para Web Speech API offline/local.
 * - Zero dependências npm externas (Node.js 18+/20+ CommonJS).
 */

const MAX_TEXT_LENGTH = 600;
const UPSTREAM_TIMEOUT_MS = 8000;
const DEFAULT_PCM_SAMPLE_RATE = 24000;
const DEFAULT_VOICE_PRESET = 'ptbr_warm';
const DEFAULT_TONE = 'info';

const VOICE_PRESETS = Object.freeze({
  ptbr_warm: Object.freeze({
    model: 'gemini-3.8-flash-lite-tts',
    voice: 'pt-br-assistant-6'
  }),
  sulafat_expressive: Object.freeze({
    model: 'gemini-3.8-flash-tts',
    voice: 'Sulafat'
  }),
  vindemiatrix_calm: Object.freeze({
    model: 'gemini-3.8-flash-tts',
    voice: 'Vindemiatrix'
  })
});

const TONE_DIRECTIONS = Object.freeze({
  info: Object.freeze({
    audioProfile:
      'Laya, assistente de mobilidade urbana do Recife. Voz feminina natural, acolhedora, calma e próxima.',
    directorsNotes:
      'Fale em português brasileiro coloquial e acolhedor, ritmo natural de conversa, sem entusiasmo exagerado, sem tom publicitário e sem voz robótica.'
  }),
  arriving: Object.freeze({
    audioProfile:
      'Laya, assistente de mobilidade urbana acolhedora avisando quem está na parada que o ônibus está se aproximando.',
    directorsNotes:
      'Tom levemente atento e prestativo, mantendo tranquilidade, calor humano e naturalidade em português brasileiro, sem urgência exagerada nem som de sirene.'
  }),
  alert: Object.freeze({
    audioProfile:
      'Laya, guia urbana serena e empática orientando passageiros durante chuva, atraso ou desvio de rota.',
    directorsNotes:
      'Fala serena, calma, firme e reconfortante em português brasileiro, com pausas leves para passar segurança sem dramatizar nem soar robótica.'
  }),
  cheerful: Object.freeze({
    audioProfile:
      'Laya, amiga atenta compartilhando uma boa notícia cotidiana de ônibus livre ou conexão rápida.',
    directorsNotes:
      'Tom leve, casual e satisfeito, com sorriso sutil na voz e ritmo conversacional fluido em português brasileiro, sem euforia artificial nem tom de comercial.'
  })
});

function sendJsonFallback(res, statusCode, reason, extra = {}) {
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(
    JSON.stringify({
      fallback: 'web_speech',
      reason,
      ...extra
    })
  );
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

function isWavBuffer(buf) {
  return (
    Buffer.isBuffer(buf) &&
    buf.length >= 44 &&
    buf.subarray(0, 4).toString('ascii') === 'RIFF' &&
    buf.subarray(8, 12).toString('ascii') === 'WAVE'
  );
}

function parsePcmSampleRate(mimeType) {
  const match = /rate=(\d+)/i.exec(String(mimeType || ''));
  if (!match) return DEFAULT_PCM_SAMPLE_RATE;
  const parsed = Number.parseInt(match[1], 10);
  return Number.isFinite(parsed) && parsed >= 8000 && parsed <= 96000
    ? parsed
    : DEFAULT_PCM_SAMPLE_RATE;
}

function wrapPcmL16AsWav(pcmBuffer, sampleRate = DEFAULT_PCM_SAMPLE_RATE) {
  const numChannels = 1;
  const bitsPerSample = 16;
  const byteRate = sampleRate * numChannels * (bitsPerSample / 8);
  const blockAlign = numChannels * (bitsPerSample / 8);
  const dataSize = pcmBuffer.length;

  const header = Buffer.alloc(44);
  header.write('RIFF', 0, 'ascii');
  header.writeUInt32LE(36 + dataSize, 4);
  header.write('WAVE', 8, 'ascii');
  header.write('fmt ', 12, 'ascii');
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(numChannels, 22);
  header.writeUInt32LE(sampleRate, 24);
  header.writeUInt32LE(byteRate, 28);
  header.writeUInt16LE(blockAlign, 32);
  header.writeUInt16LE(bitsPerSample, 34);
  header.write('data', 36, 'ascii');
  header.writeUInt32LE(dataSize, 40);

  return Buffer.concat([header, pcmBuffer]);
}

function buildTtsPrompt(text, toneDirection) {
  return (
    `[AUDIO PROFILE: ${toneDirection.audioProfile}]\n` +
    `[DIRECTOR'S NOTES: ${toneDirection.directorsNotes}]\n\n` +
    `Say: ${text}`
  );
}

function extractInlineAudio(upstreamBody) {
  const candidates = Array.isArray(upstreamBody && upstreamBody.candidates)
    ? upstreamBody.candidates
    : [];
  for (const candidate of candidates) {
    const parts = Array.isArray(candidate && candidate.content && candidate.content.parts)
      ? candidate.content.parts
      : [];
    for (const part of parts) {
      if (part && part.inlineData && typeof part.inlineData.data === 'string' && part.inlineData.data) {
        return {
          mimeType: String(part.inlineData.mimeType || ''),
          data: part.inlineData.data
        };
      }
    }
  }
  return null;
}

module.exports = async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.setHeader('Allow', 'GET, POST, OPTIONS');
    res.end();
    return;
  }

  if (req.method === 'GET') {
    const hasKey = Boolean(typeof process.env.GEMINI_API_KEY === 'string' && process.env.GEMINI_API_KEY.trim());
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.end(
      JSON.stringify({
        available: hasKey,
        fallback: 'web_speech',
        reason: hasKey ? 'ready' : 'missing_api_key',
        presets: Object.keys(VOICE_PRESETS)
      })
    );
    return;
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST, OPTIONS');
    sendJsonFallback(res, 405, 'method_not_allowed');
    return;
  }

  const apiKey = typeof process.env.GEMINI_API_KEY === 'string'
    ? process.env.GEMINI_API_KEY.trim()
    : '';
  if (!apiKey) {
    sendJsonFallback(res, 501, 'missing_api_key');
    return;
  }

  let body;
  try {
    body = await readJsonBody(req);
  } catch (_) {
    sendJsonFallback(res, 400, 'invalid_json');
    return;
  }

  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    sendJsonFallback(res, 400, 'invalid_request');
    return;
  }

  const rawText = typeof body.text === 'string' ? body.text.trim() : '';
  if (!rawText) {
    sendJsonFallback(res, 400, 'missing_text');
    return;
  }
  if (rawText.length > MAX_TEXT_LENGTH) {
    sendJsonFallback(res, 400, 'text_too_long');
    return;
  }

  const voicePresetKey = body.voice_preset === undefined || body.voice_preset === null || body.voice_preset === ''
    ? DEFAULT_VOICE_PRESET
    : String(body.voice_preset);
  const preset = Object.prototype.hasOwnProperty.call(VOICE_PRESETS, voicePresetKey)
    ? VOICE_PRESETS[voicePresetKey]
    : null;
  if (!preset) {
    sendJsonFallback(res, 400, 'invalid_voice_preset');
    return;
  }

  const toneKey = body.tone === undefined || body.tone === null || body.tone === ''
    ? DEFAULT_TONE
    : String(body.tone);
  const toneDirection = Object.prototype.hasOwnProperty.call(TONE_DIRECTIONS, toneKey)
    ? TONE_DIRECTIONS[toneKey]
    : null;
  if (!toneDirection) {
    sendJsonFallback(res, 400, 'invalid_tone');
    return;
  }

  const prompt = buildTtsPrompt(rawText, toneDirection);
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(preset.model)}:generateContent`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), UPSTREAM_TIMEOUT_MS);

  try {
    const upstreamRes = await fetch(endpoint, {
      method: 'POST',
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'x-goog-api-key': apiKey
      },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: prompt }] }],
        generationConfig: {
          responseModalities: ['AUDIO'],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: {
                voiceName: preset.voice
              }
            }
          }
        }
      })
    });

    if (upstreamRes.status === 429 || !upstreamRes.ok) {
      sendJsonFallback(res, 503, 'upstream_unavailable');
      return;
    }

    const upstreamJson = await upstreamRes.json();
    const inlineAudio = extractInlineAudio(upstreamJson);
    if (!inlineAudio) {
      sendJsonFallback(res, 503, 'upstream_unavailable');
      return;
    }

    const rawBuffer = Buffer.from(inlineAudio.data, 'base64');
    if (!rawBuffer.length) {
      sendJsonFallback(res, 503, 'upstream_unavailable');
      return;
    }

    const wavBuffer = isWavBuffer(rawBuffer)
      ? rawBuffer
      : wrapPcmL16AsWav(rawBuffer, parsePcmSampleRate(inlineAudio.mimeType));

    res.statusCode = 200;
    res.setHeader('Content-Type', 'audio/wav');
    res.setHeader('Content-Length', String(wavBuffer.length));
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Laya-TTS-Provider', preset.model);
    res.setHeader('X-Laya-TTS-Voice', preset.voice);
    res.end(wavBuffer);
  } catch (_) {
    sendJsonFallback(res, 503, 'upstream_unavailable');
  } finally {
    clearTimeout(timeoutId);
  }
};
