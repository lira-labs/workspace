/**
 * GrafoParada · Laya Voice Engine (Camada Desacoplada de TTS)
 * Arquitetura polimórfica em cascata silenciosa:
 *   1) PrebakedStaticTTSProvider (<30ms via ./audio/laya/*.wav)
 *   2) CloudProxyTTSProvider (POST /api/tts com cache LRU e cooldown 60s)
 *   3) WebSpeechFallbackProvider (PT-BR offline com ranking inteligente e chunking <=165 chars)
 * Zero dependências externas · Seguro em Browser, Headless Chrome e Node.js.
 */

(function(root) {
  'use strict';

  const STORAGE_KEY_PROFILE = 'grafoparada_voice_profile';
  const STORAGE_KEY_MUTED = 'grafoparada_voice_muted';
  const STORAGE_KEY_VOICE_IDX = 'grafoparada_voice_idx';

  const TONE_PRESETS = Object.freeze({
    info: Object.freeze({
      id: 'info',
      label: 'Normal · Tranquila',
      rate: 0.99,
      pitch: 1.02
    }),
    arriving: Object.freeze({
      id: 'arriving',
      label: 'Chegada · Atenta',
      rate: 1.03,
      pitch: 1.04
    }),
    alert: Object.freeze({
      id: 'alert',
      label: 'Alerta/Atraso · Serena',
      rate: 0.95,
      pitch: 0.99
    }),
    cheerful: Object.freeze({
      id: 'cheerful',
      label: 'Boa notícia · Leve',
      rate: 1.03,
      pitch: 1.05
    })
  });

  const VOICE_PROFILES = Object.freeze({
    ptbr_warm: Object.freeze({
      id: 'ptbr_warm',
      buttonLabel: 'Laya PT-BR',
      title: 'Laya pt-BR Nativa (Gemini 3.8 Lite)',
      staticKey: 'ptbr_warm'
    }),
    sulafat_expressive: Object.freeze({
      id: 'sulafat_expressive',
      buttonLabel: 'Sulafat IA',
      title: 'Laya Expressiva (Gemini 3.8 Sulafat)',
      staticKey: 'sulafat_expressive'
    }),
    offline_only: Object.freeze({
      id: 'offline_only',
      buttonLabel: 'Offline',
      title: 'Voz Local Offline PT-BR (Web Speech)',
      staticKey: null
    })
  });

  const VOICE_PROFILE_ORDER = Object.freeze([
    'ptbr_warm',
    'sulafat_expressive',
    'offline_only'
  ]);

  const VOICE_STATES = Object.freeze({
    muted: Object.freeze({ state: 'muted', label: 'Silenciada' }),
    loading: Object.freeze({ state: 'loading', label: 'Sintetizando...' }),
    static: Object.freeze({ state: 'static', label: 'Estático <30ms' }),
    cloud: Object.freeze({ state: 'cloud', label: 'Gemini Nuvem' }),
    offline: Object.freeze({ state: 'offline', label: 'Offline PT-BR' })
  });

  const STATIC_CLIPS_MAP = Object.freeze({
    ptbr_warm: Object.freeze({
      boas_vindas: './audio/laya/ptbr_boas_vindas.wav',
      alerta_pe60: './audio/laya/ptbr_alerta_pe60.wav'
    }),
    sulafat_expressive: Object.freeze({
      boas_vindas: './audio/laya/sulafat_boas_vindas.wav',
      chegada_199: './audio/laya/sulafat_chegada_199.wav',
      atraso: './audio/laya/sulafat_atraso.wav',
      alerta_pe60: './audio/laya/sulafat_alerta_pe60.wav',
      conversa_casual: './audio/laya/sulafat_conversa_casual.wav'
    })
  });

  function safeStorageGet(storage, key) {
    if (!storage || typeof storage.getItem !== 'function') return null;
    try {
      return storage.getItem(key);
    } catch (_err) {
      return null;
    }
  }

  function safeStorageSet(storage, key, value) {
    if (!storage || typeof storage.setItem !== 'function') return false;
    try {
      storage.setItem(key, String(value));
      return true;
    } catch (_err) {
      return false;
    }
  }

  function createAudioPlayer(options = {}) {
    const audioFactory = typeof options.audioFactory === 'function'
      ? options.audioFactory
      : (typeof Audio !== 'undefined' ? (url) => new Audio(url) : null);
    const customPlay = typeof options.playAudioFn === 'function' ? options.playAudioFn : null;

    let currentAudio = null;
    let playToken = 0;

    function stop() {
      playToken += 1;
      if (!currentAudio) return;
      try {
        if (typeof currentAudio.pause === 'function') {
          currentAudio.pause();
        }
        if ('currentTime' in currentAudio) {
          currentAudio.currentTime = 0;
        }
        currentAudio.onended = null;
        currentAudio.onerror = null;
        if ('src' in currentAudio) {
          currentAudio.src = '';
        }
      } catch (_err) {
        // Ignora erro de limpeza de elemento Audio
      }
      currentAudio = null;
    }

    async function play(url) {
      stop();
      const myToken = playToken;

      if (customPlay) {
        return customPlay(url, { token: myToken, isCancelled: () => myToken !== playToken });
      }
      if (!audioFactory) {
        throw new Error('Audio playback API unavailable');
      }

      const audio = audioFactory(url);
      if (!audio || typeof audio.play !== 'function') {
        throw new Error('Invalid Audio instance');
      }
      currentAudio = audio;
      if ('preload' in audio) {
        try {
          audio.preload = 'auto';
        } catch (_err) {
          // noop
        }
      }

      return new Promise((resolve, reject) => {
        let settled = false;
        const cleanupIfCurrent = () => {
          if (currentAudio === audio) {
            currentAudio = null;
          }
        };
        const fail = (err) => {
          if (settled) return;
          settled = true;
          cleanupIfCurrent();
          reject(err instanceof Error ? err : new Error(String(err || 'Audio playback failed')));
        };

        audio.onended = () => {
          cleanupIfCurrent();
        };
        audio.onerror = () => {
          if (myToken !== playToken) return;
          fail(new Error('Audio playback error'));
        };

        try {
          Promise.resolve(audio.play()).then(
            () => {
              if (myToken !== playToken) {
                try {
                  if (typeof audio.pause === 'function') audio.pause();
                } catch (_err) {
                  // noop
                }
                fail(new Error('Audio playback cancelled'));
                return;
              }
              if (!settled) {
                settled = true;
                resolve({ played: true, url });
              }
            },
            (err) => {
              fail(err);
            }
          );
        } catch (err) {
          fail(err);
        }
      });
    }

    return {
      play,
      stop,
      isSupported: () => Boolean(customPlay || audioFactory)
    };
  }

  // ===========================================================================
  // PROVEDORES POLIMÓRFICOS DE SÍNTESE (BaseTTSProvider)
  // ===========================================================================

  class BaseTTSProvider {
    constructor(name) {
      this.name = name || 'base';
    }

    isAvailable() {
      return false;
    }

    async synthesize(_text, _options) {
      throw new Error('BaseTTSProvider.synthesize() must be implemented by subclasses');
    }

    stop() {}
  }

  class PrebakedStaticTTSProvider extends BaseTTSProvider {
    constructor(options = {}) {
      super('static');
      this.clipsMap = options.clipsMap || STATIC_CLIPS_MAP;
      this._player = createAudioPlayer(options);
    }

    getClipUrl(clipId, profileId) {
      if (!clipId || !profileId) return null;
      const profile = Object.prototype.hasOwnProperty.call(VOICE_PROFILES, profileId)
        ? VOICE_PROFILES[profileId]
        : null;
      if (!profile || !profile.staticKey) return null;
      const bucket = Object.prototype.hasOwnProperty.call(this.clipsMap, profile.staticKey)
        ? this.clipsMap[profile.staticKey]
        : null;
      if (!bucket) return null;
      return Object.prototype.hasOwnProperty.call(bucket, clipId) ? bucket[clipId] : null;
    }

    hasClip(clipId, profileId) {
      return Boolean(this.getClipUrl(clipId, profileId));
    }

    isAvailable(clipId, profileId) {
      if (!this._player.isSupported()) return false;
      if (clipId !== undefined || profileId !== undefined) {
        return this.hasClip(clipId, profileId);
      }
      return true;
    }

    async synthesize(_text, options = {}) {
      const clipId = options.clipId;
      const profileId = options.voicePreset || options.profileId || 'ptbr_warm';
      const url = this.getClipUrl(clipId, profileId);
      if (!url) {
        throw new Error(`Static clip "${clipId}" unavailable for profile "${profileId}"`);
      }
      await this._player.play(url);
      return {
        provider: 'static',
        mode: 'static',
        clipId,
        profileId,
        url
      };
    }

    stop() {
      this._player.stop();
    }
  }

  class CloudProxyTTSProvider extends BaseTTSProvider {
    constructor(options = {}) {
      super('cloud');
      this.endpoint = options.endpoint || '/api/tts';
      this.timeoutMs = typeof options.timeoutMs === 'number' ? options.timeoutMs : 6000;
      this.cooldownMs = typeof options.cooldownMs === 'number' ? options.cooldownMs : 60000;
      this.maxCacheEntries = typeof options.maxCacheEntries === 'number' ? options.maxCacheEntries : 40;
      this.maxTextLength = typeof options.maxTextLength === 'number' ? options.maxTextLength : 600;
      this._hasExplicitWindow = options.window !== undefined;
      this._win = this._hasExplicitWindow
        ? options.window
        : (typeof window !== 'undefined' ? window : null);
      this._storage = options.storage !== undefined
        ? options.storage
        : (typeof localStorage !== 'undefined' ? localStorage : null);
      this._hasCustomFetch = typeof options.fetchFn === 'function';
      this.allowLocalProxy = Boolean(options.allowLocalProxy);
      this.skipCapabilityCheck = Boolean(options.skipCapabilityCheck);
      this._fetchFn = this._hasCustomFetch
        ? options.fetchFn
        : (typeof fetch === 'function' ? fetch.bind(globalThis) : null);
      this._createObjectURL = typeof options.createObjectURL === 'function'
        ? options.createObjectURL
        : (typeof URL !== 'undefined' && typeof URL.createObjectURL === 'function' ? URL.createObjectURL.bind(URL) : null);
      this._revokeObjectURL = typeof options.revokeObjectURL === 'function'
        ? options.revokeObjectURL
        : (typeof URL !== 'undefined' && typeof URL.revokeObjectURL === 'function' ? URL.revokeObjectURL.bind(URL) : null);
      this._now = typeof options.now === 'function' ? options.now : () => Date.now();
      this._player = createAudioPlayer(options);
      this._cache = new Map();
      this._proxyUnavailableUntil = 0;
      this._proxyCapability = null;
      this._activeController = null;
    }

    resetAvailability() {
      this._proxyUnavailableUntil = 0;
      this._proxyCapability = null;
    }

    _isBrowserLocalStaticEnv() {
      if (this.allowLocalProxy) return false;
      const win = this._win;
      if (!win || !win.location) return false;
      const proto = String(win.location.protocol || '');
      const host = String(win.location.hostname || '');
      const forcedLocal = Boolean(safeStorageGet(this._storage, 'grafoparada_enable_local_cloud_tts') === '1');
      if (forcedLocal) return false;
      if (proto === 'file:') return true;
      return (proto === 'http:') && (host === '127.0.0.1' || host === 'localhost' || host === '[::1]');
    }

    isAvailable() {
      if (!this._fetchFn || !this._player.isSupported() || !this._createObjectURL) {
        return false;
      }
      if (this._isBrowserLocalStaticEnv()) {
        return false;
      }
      if (typeof navigator !== 'undefined' && navigator && navigator.onLine === false) {
        return false;
      }
      return this._now() >= this._proxyUnavailableUntil;
    }

    _cacheGet(key) {
      if (!this._cache.has(key)) return null;
      const value = this._cache.get(key);
      // Atualiza recência no LRU
      this._cache.delete(key);
      this._cache.set(key, value);
      return value;
    }

    _cacheSet(key, blobUrl) {
      if (this._cache.has(key)) {
        const prev = this._cache.get(key);
        this._cache.delete(key);
        if (prev && prev !== blobUrl && this._revokeObjectURL) {
          try { this._revokeObjectURL(prev); } catch (_err) {}
        }
      } else if (this._cache.size >= this.maxCacheEntries) {
        const oldestKey = this._cache.keys().next().value;
        const oldestUrl = this._cache.get(oldestKey);
        this._cache.delete(oldestKey);
        if (oldestUrl && this._revokeObjectURL) {
          try { this._revokeObjectURL(oldestUrl); } catch (_err) {}
        }
      }
      this._cache.set(key, blobUrl);
    }

    clearCache() {
      if (this._revokeObjectURL) {
        for (const url of this._cache.values()) {
          try { this._revokeObjectURL(url); } catch (_err) {}
        }
      }
      this._cache.clear();
    }

    async synthesize(text, options = {}) {
      const cleanText = String(text || '').trim();
      if (!cleanText || cleanText.length > this.maxTextLength) {
        throw new Error('Text length outside cloud TTS range');
      }

      const voicePreset = options.voicePreset || options.voice_preset || 'ptbr_warm';
      const tone = options.tone || 'info';
      const cacheKey = `${voicePreset}::${tone}::${cleanText}`;

      const cachedUrl = this._cacheGet(cacheKey);
      if (cachedUrl) {
        await this._player.play(cachedUrl);
        return {
          provider: 'cloud',
          mode: 'cloud',
          cached: true,
          voicePreset,
          tone,
          url: cachedUrl
        };
      }

      if (!this.isAvailable()) {
        throw new Error('Cloud TTS proxy temporarily unavailable');
      }

      // Em browser remoto, consulta GET /api/tts antes de POST para evitar 501 vermelho no console
      if (!this.skipCapabilityCheck && this._proxyCapability === null) {
        try {
          const capRes = await this._fetchFn(this.endpoint, { method: 'GET' });
          if (capRes && capRes.ok) {
            const capData = typeof capRes.json === 'function' ? await capRes.json() : null;
            if (capData && capData.available === false) {
              this._proxyCapability = false;
              this._proxyUnavailableUntil = this._now() + this.cooldownMs;
              throw new Error('Cloud TTS proxy key not configured');
            }
            this._proxyCapability = true;
          } else if (capRes && (capRes.status === 404 || capRes.status === 405 || capRes.status === 501 || capRes.status === 503)) {
            this._proxyCapability = false;
            this._proxyUnavailableUntil = this._now() + this.cooldownMs;
            throw new Error(`Cloud TTS proxy unavailable (HTTP ${capRes.status})`);
          }
        } catch (capErr) {
          if (this._proxyCapability === false) throw capErr;
        }
      } else if (this._proxyCapability === false && this._now() < this._proxyUnavailableUntil) {
        throw new Error('Cloud TTS proxy key not configured');
      }

      const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
      if (controller) {
        this._activeController = controller;
      }
      const timeoutId = controller
        ? setTimeout(() => controller.abort(), this.timeoutMs)
        : null;

      let response;
      try {
        response = await this._fetchFn(this.endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: cleanText,
            voice_preset: voicePreset,
            tone
          }),
          signal: controller ? controller.signal : undefined
        });
      } finally {
        if (timeoutId !== null) clearTimeout(timeoutId);
        if (this._activeController === controller) {
          this._activeController = null;
        }
      }

      if (!response) {
        throw new Error('Empty response from cloud TTS proxy');
      }

      if (response.status === 501 || response.status === 503 || response.status === 404 || response.status === 405) {
        this._proxyUnavailableUntil = this._now() + this.cooldownMs;
        throw new Error(`Cloud TTS proxy unavailable (HTTP ${response.status})`);
      }

      if (!response.ok) {
        throw new Error(`Cloud TTS proxy returned HTTP ${response.status}`);
      }

      const contentType = response.headers && typeof response.headers.get === 'function'
        ? String(response.headers.get('content-type') || '').toLowerCase()
        : '';
      if (contentType.includes('application/json')) {
        throw new Error('Cloud TTS proxy returned fallback JSON');
      }

      const blob = typeof response.blob === 'function' ? await response.blob() : null;
      if (!blob || (typeof blob.size === 'number' && blob.size === 0)) {
        throw new Error('Cloud TTS proxy returned empty audio blob');
      }

      const blobUrl = this._createObjectURL(blob);
      if (!blobUrl) {
        throw new Error('Failed to allocate object URL for cloud TTS');
      }

      this._cacheSet(cacheKey, blobUrl);
      await this._player.play(blobUrl);

      return {
        provider: 'cloud',
        mode: 'cloud',
        cached: false,
        voicePreset,
        tone,
        url: blobUrl
      };
    }

    stop() {
      if (this._activeController) {
        try { this._activeController.abort(); } catch (_err) {}
        this._activeController = null;
      }
      this._player.stop();
    }
  }

  class WebSpeechFallbackProvider extends BaseTTSProvider {
    constructor(options = {}) {
      super('offline');
      this._hasExplicitWindow = options.window !== undefined;
      this._win = this._hasExplicitWindow
        ? options.window
        : (typeof window !== 'undefined' ? window : globalThis);
      this._storage = options.storage !== undefined
        ? options.storage
        : (typeof localStorage !== 'undefined' ? localStorage : null);
      this.maxChunkLength = typeof options.maxChunkLength === 'number' ? options.maxChunkLength : 165;
      this.preferredVoiceIndex = this._loadPreferredVoiceIndex();
      this._playToken = 0;
      this._cachedVoice = null;
      this._bindVoicesChanged();
    }

    _loadPreferredVoiceIndex() {
      const raw = safeStorageGet(this._storage, STORAGE_KEY_VOICE_IDX);
      const parsed = Number(raw);
      return Number.isFinite(parsed) && parsed >= 0 ? Math.floor(parsed) : 0;
    }

    _bindVoicesChanged() {
      const synth = this.getSpeechSynthesis();
      if (!synth) return;
      try {
        const prev = synth.onvoiceschanged;
        synth.onvoiceschanged = () => {
          this._cachedVoice = this.findBestVoice();
          if (typeof prev === 'function') {
            try { prev(); } catch (_err) {}
          }
        };
      } catch (_err) {
        // Headless pode bloquear atribuição em speechSynthesis
      }
    }

    getSpeechSynthesis() {
      if (this._win && 'speechSynthesis' in this._win && this._win.speechSynthesis) {
        return this._win.speechSynthesis;
      }
      if (!this._hasExplicitWindow && typeof speechSynthesis !== 'undefined' && speechSynthesis) {
        return speechSynthesis;
      }
      return null;
    }

    _getUtteranceConstructor() {
      if (this._win && typeof this._win.SpeechSynthesisUtterance === 'function') {
        return this._win.SpeechSynthesisUtterance;
      }
      if (!this._hasExplicitWindow && typeof SpeechSynthesisUtterance === 'function') {
        return SpeechSynthesisUtterance;
      }
      return null;
    }

    isAvailable() {
      return Boolean(this.getSpeechSynthesis() && this._getUtteranceConstructor());
    }

    getRankedPortugueseVoices() {
      const synth = this.getSpeechSynthesis();
      if (!synth || typeof synth.getVoices !== 'function') return [];
      let voices = [];
      try {
        voices = synth.getVoices() || [];
      } catch (_err) {
        return [];
      }
      const ptVoices = voices.filter((v) => String((v && v.lang) || '').toLowerCase().startsWith('pt'));
      if (!ptVoices.length) return [];

      const scored = ptVoices.map((v) => {
        const n = String((v && v.name) || '').toLowerCase();
        const l = String((v && v.lang) || '').toLowerCase();
        let s = 0;
        if (l === 'pt-br' || l === 'pt_br') s += 35;
        if (
          n.includes('thalita') ||
          n.includes('francisca') ||
          n.includes('giovanna') ||
          n.includes('brenda') ||
          n.includes('leticia') ||
          n.includes('letícia') ||
          n.includes('antonio') ||
          n.includes('antônio') ||
          n.includes('humberto')
        ) {
          s += 110;
        }
        if (
          n.includes('natural') ||
          n.includes('neural') ||
          n.includes('online') ||
          n.includes('wavenet') ||
          n.includes('enhanced') ||
          n.includes('google')
        ) {
          s += 85;
        }
        if (n.includes('luciana') || n.includes('felipe') || n.includes('maria') || n.includes('raquel')) {
          s += 55;
        }
        if (!v.localService) s += 20;
        if (n.includes('espeak') || n.includes('compact') || n.includes('robot')) {
          s -= 60;
        }
        return { voice: v, score: s };
      });

      scored.sort((a, b) => b.score - a.score);
      return scored.map((item) => item.voice);
    }

    findBestVoice() {
      const ranked = this.getRankedPortugueseVoices();
      if (!ranked.length) return null;
      const idx = ((this.preferredVoiceIndex % ranked.length) + ranked.length) % ranked.length;
      this._cachedVoice = ranked[idx];
      return this._cachedVoice;
    }

    cyclePreferredVoice() {
      const ranked = this.getRankedPortugueseVoices();
      if (!ranked.length) return null;
      this.preferredVoiceIndex = (this.preferredVoiceIndex + 1) % ranked.length;
      safeStorageSet(this._storage, STORAGE_KEY_VOICE_IDX, String(this.preferredVoiceIndex));
      this._cachedVoice = ranked[this.preferredVoiceIndex];
      return this._cachedVoice;
    }

    splitSpeechSentences(text, maxLen = this.maxChunkLength) {
      const clean = String(text || '').trim();
      if (!clean) return [];
      if (clean.length <= maxLen) return [clean];

      const rawParts = clean.split(/(?<=[.!?;])\s+/);
      const boundedParts = [];

      for (let i = 0; i < rawParts.length; i++) {
        const part = rawParts[i].trim();
        if (!part) continue;
        if (part.length <= maxLen) {
          boundedParts.push(part);
          continue;
        }
        // Sub-divide sentenças longas por vírgula ou palavras para respeitar <=165 chars
        const subParts = part.split(/(?<=,)\s+/);
        let acc = '';
        for (let j = 0; j < subParts.length; j++) {
          const sp = subParts[j].trim();
          if (!sp) continue;
          if (sp.length > maxLen) {
            if (acc) {
              boundedParts.push(acc);
              acc = '';
            }
            const words = sp.split(/\s+/);
            let wordLine = '';
            for (let w = 0; w < words.length; w++) {
              const candidate = wordLine ? `${wordLine} ${words[w]}` : words[w];
              if (candidate.length <= maxLen) {
                wordLine = candidate;
              } else {
                if (wordLine) boundedParts.push(wordLine);
                wordLine = words[w].length > maxLen ? words[w].slice(0, maxLen) : words[w];
              }
            }
            if (wordLine) boundedParts.push(wordLine);
          } else if (!acc) {
            acc = sp;
          } else if ((acc + ' ' + sp).length <= maxLen) {
            acc = acc + ' ' + sp;
          } else {
            boundedParts.push(acc);
            acc = sp;
          }
        }
        if (acc) boundedParts.push(acc);
      }

      const chunks = [];
      let current = '';
      for (let i = 0; i < boundedParts.length; i++) {
        const piece = boundedParts[i];
        if ((current ? `${current} ${piece}` : piece).length <= maxLen) {
          current = current ? `${current} ${piece}` : piece;
        } else {
          if (current) chunks.push(current);
          current = piece;
        }
      }
      if (current) chunks.push(current);
      return chunks.length ? chunks : [clean.slice(0, maxLen)];
    }

    async synthesize(text, options = {}) {
      const synth = this.getSpeechSynthesis();
      const UtteranceCtor = this._getUtteranceConstructor();
      const cleanText = String(text || '').trim();
      const tonePreset = TONE_PRESETS[options.tone] || TONE_PRESETS.info;

      if (!synth || !UtteranceCtor || !cleanText) {
        return {
          provider: 'offline',
          mode: 'offline',
          spoken: false,
          tone: tonePreset.id,
          reason: !cleanText ? 'empty_text' : 'speech_synthesis_unavailable'
        };
      }

      const chunks = this.splitSpeechSentences(cleanText, this.maxChunkLength);
      const voice = this.findBestVoice();
      this._playToken += 1;
      const myToken = this._playToken;

      try {
        if (typeof synth.cancel === 'function') {
          synth.cancel();
        }
      } catch (_err) {
        // Ignora erro de cancel em headless
      }

      let idx = 0;
      const speakNextChunk = () => {
        if (myToken !== this._playToken || idx >= chunks.length) return;
        try {
          const utter = new UtteranceCtor(chunks[idx++]);
          utter.lang = 'pt-BR';
          utter.rate = tonePreset.rate;
          utter.pitch = tonePreset.pitch;
          if (voice) {
            utter.voice = voice;
          }
          utter.onend = speakNextChunk;
          utter.onerror = speakNextChunk;
          synth.speak(utter);
        } catch (_err) {
          // Protegido contra falhas em navegadores headless sem TTS ativo
        }
      };

      try {
        speakNextChunk();
      } catch (_err) {
        return {
          provider: 'offline',
          mode: 'offline',
          spoken: false,
          tone: tonePreset.id,
          reason: 'speech_synthesis_failed'
        };
      }

      return {
        provider: 'offline',
        mode: 'offline',
        spoken: true,
        tone: tonePreset.id,
        rate: tonePreset.rate,
        pitch: tonePreset.pitch,
        voiceName: voice ? voice.name : null,
        chunks
      };
    }

    stop() {
      this._playToken += 1;
      const synth = this.getSpeechSynthesis();
      if (synth && typeof synth.cancel === 'function') {
        try {
          synth.cancel();
        } catch (_err) {
          // noop
        }
      }
    }
  }

  // ===========================================================================
  // ORQUESTRADOR DE VOZ (LayaVoiceDirector)
  // ===========================================================================

  class LayaVoiceDirector {
    constructor(options = {}) {
      this._storage = options.storage !== undefined
        ? options.storage
        : (typeof localStorage !== 'undefined' ? localStorage : null);

      this.staticProvider = options.staticProvider || new PrebakedStaticTTSProvider(options.staticOptions);
      this.cloudProvider = options.cloudProvider || new CloudProxyTTSProvider(options.cloudOptions);
      this.offlineProvider = options.offlineProvider || new WebSpeechFallbackProvider({
        storage: this._storage,
        window: options.window
      });

      const savedProfile = safeStorageGet(this._storage, STORAGE_KEY_PROFILE);
      const initialProfile = options.profile || savedProfile || 'ptbr_warm';
      this._profileId = Object.prototype.hasOwnProperty.call(VOICE_PROFILES, initialProfile)
        ? initialProfile
        : 'ptbr_warm';

      if (typeof options.muted === 'boolean') {
        this._muted = options.muted;
      } else {
        this._muted = safeStorageGet(this._storage, STORAGE_KEY_MUTED) !== '0';
      }

      this._listeners = new Set();
      this._speakSeq = 0;

      const initState = this._muted
        ? 'muted'
        : (this._profileId === 'offline_only' ? 'offline' : 'cloud');
      this._state = VOICE_STATES[initState].state;
      this._stateLabel = VOICE_STATES[initState].label;
    }

    get muted() {
      return this._muted;
    }

    isMuted() {
      return this._muted;
    }

    setMuted(muted) {
      this._muted = Boolean(muted);
      safeStorageSet(this._storage, STORAGE_KEY_MUTED, this._muted ? '1' : '0');
      if (this._muted) {
        this.stopAll();
        this._emitState('muted');
      } else {
        this._emitState(this._profileId === 'offline_only' ? 'offline' : 'cloud');
      }
      return this._muted;
    }

    toggleMute() {
      return this.setMuted(!this._muted);
    }

    getProfileId() {
      return this._profileId;
    }

    getProfile() {
      return VOICE_PROFILES[this._profileId] || VOICE_PROFILES.ptbr_warm;
    }

    getProfiles() {
      return VOICE_PROFILE_ORDER.map((id) => VOICE_PROFILES[id]);
    }

    setProfile(profileId) {
      const nextId = Object.prototype.hasOwnProperty.call(VOICE_PROFILES, profileId)
        ? profileId
        : 'ptbr_warm';
      this._profileId = nextId;
      safeStorageSet(this._storage, STORAGE_KEY_PROFILE, nextId);
      if (this.cloudProvider && typeof this.cloudProvider.resetAvailability === 'function') {
        this.cloudProvider.resetAvailability();
      }
      if (!this._muted) {
        this._emitState(nextId === 'offline_only' ? 'offline' : 'cloud');
      } else {
        this._emitState('muted');
      }
      return this.getProfile();
    }

    cycleProfile() {
      const curIdx = VOICE_PROFILE_ORDER.indexOf(this._profileId);
      const nextId = VOICE_PROFILE_ORDER[(curIdx + 1) % VOICE_PROFILE_ORDER.length];
      return this.setProfile(nextId);
    }

    getState() {
      return {
        state: this._state,
        label: this._stateLabel,
        profile: this.getProfile(),
        muted: this._muted
      };
    }

    onStateChange(listener) {
      if (typeof listener !== 'function') return () => {};
      this._listeners.add(listener);
      return () => {
        this._listeners.delete(listener);
      };
    }

    offStateChange(listener) {
      this._listeners.delete(listener);
    }

    _emitState(stateKey, extra = {}) {
      const meta = VOICE_STATES[stateKey] || VOICE_STATES.offline;
      this._state = meta.state;
      this._stateLabel = meta.label;
      const snapshot = {
        state: meta.state,
        label: meta.label,
        profile: this.getProfile(),
        muted: this._muted,
        ...extra
      };
      for (const listener of this._listeners) {
        try {
          listener(snapshot);
        } catch (_err) {
          // Listener de UI nunca deve interromper o motor de voz
        }
      }
    }

    formatForSpeech(raw) {
      if (!raw) return '';
      let s = String(raw);
      s = s.replace(/<[^>]+>/g, ' ');
      s = s.replace(/&nbsp;/gi, ' ');
      s = s.replace(/&amp;/gi, ' e ');
      s = s.replace(/&lt;|&gt;/gi, ' ');
      s = s.replace(/\s*(?:➔|→|->)\s*/g, ', depois ');
      s = s.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}\u{200D}]/gu, ' ');
      s = s.replace(/\bT[Ii]\s+/g, 'T I ');
      s = s.replace(/\bPE-?60\b/gi, 'P E sessenta');
      s = s.replace(/\bPE-(\d+)\b/gi, 'P E $1');
      s = s.replace(/\bBR-(\d+)\b/gi, 'B R $1');
      s = s.replace(/\bST-?GCN\b/gi, 'rede neural espaço-temporal');
      s = s.replace(/\bUFRPE\b/gi, 'Universidade Federal Rural de Pernambuco');
      s = s.replace(/\bUFPE\b/gi, 'Universidade Federal de Pernambuco');
      s = s.replace(/\bGTFS\b/gi, 'base oficial de linhas');
      s = s.replace(/\bCTM\b/gi, 'Consórcio Grande Recife');
      s = s.replace(/\bRMR\b/g, 'Região Metropolitana do Recife');
      s = s.replace(/\bETA\b/g, 'previsão de chegada');
      s = s.replace(/\bMAE\b/g, 'erro médio absoluto');
      s = s.replace(/\bCDU\b/gi, 'C D U');
      s = s.replace(/\bSEI\b/g, 'sistema SEI');
      s = s.replace(/\bVEM\b/g, 'cartão VEM');
      s = s.replace(/(\d+(?:[.,]\d+)?)\s*km\/h\b/gi, (_m, n) => `${n} ${n === '1' ? 'quilômetro' : 'quilômetros'} por hora`);
      s = s.replace(/\b(\d+(?:[.,]\d+)?)\s*min\.?\b/gi, (_m, n) => `${n} ${n === '1' ? 'minuto' : 'minutos'}`);
      s = s.replace(/\b(\d+(?:[.,]\d+)?)\s*km\b/gi, (_m, n) => `${n} ${n === '1' ? 'quilômetro' : 'quilômetros'}`);
      s = s.replace(/\b(\d+(?:[.,]\d+)?)\s*ms\b/gi, (_m, n) => `${n} milissegundos`);
      s = s.replace(/(\d+(?:[.,]\d+)?)\s*µs\b/gi, (_m, n) => `${n} microssegundos`);
      s = s.replace(/\b(\d+(?:[.,]\d+)?)\s*m\b/gi, (_m, n) => `${n} ${n === '1' ? 'metro' : 'metros'}`);
      s = s.replace(/\s+/g, ' ').trim();
      return s;
    }

    inferTone(text, explicitTone) {
      if (explicitTone && Object.prototype.hasOwnProperty.call(TONE_PRESETS, explicitTone)) {
        return explicitTone;
      }
      const s = String(text || '').toLowerCase();
      if (/\b(atraso|atrasou|atrasad[oa]|alagamento|trava h[ií]brida|over-?smoothing|anomalia|alerta|aten[cç][aã]o|cuidado|queima|desvio|lotad[oa]|cr[ií]tica|emerg[eê]ncia|perigo|n[aã]o localizei|n[aã]o encontrei|fora da cobertura)\b/i.test(s)) {
        return 'alert';
      }
      if (/\b(chega(?:ndo)?|pr[oó]ximo [oô]nibus|minutinhos|em \d+ min|a caminho|se ajeitar na parada|est[aá] prevista para chegar|chega em uns)\b/i.test(s)) {
        return 'arriving';
      }
      if (/\b(boa not[ií]cia|consegui|melhor op[cç][aã]o|linha direta|vazio|assentos livres|tranquila|favoritos|adicionada|pronto)\b/i.test(s)) {
        return 'cheerful';
      }
      return 'info';
    }

    stopAll() {
      this._speakSeq += 1;
      try {
        if (this.staticProvider && typeof this.staticProvider.stop === 'function') {
          this.staticProvider.stop();
        }
      } catch (_err) {}
      try {
        if (this.cloudProvider && typeof this.cloudProvider.stop === 'function') {
          this.cloudProvider.stop();
        }
      } catch (_err) {}
      try {
        if (this.offlineProvider && typeof this.offlineProvider.stop === 'function') {
          this.offlineProvider.stop();
        }
      } catch (_err) {}
    }

    async speak(text, opts) {
      if (!opts || !opts.explicit || this._muted) {
        if (this._muted) {
          this._emitState('muted');
        }
        return {
          spoken: false,
          muted: Boolean(this._muted),
          reason: !opts || !opts.explicit ? 'not_explicit' : 'muted'
        };
      }

      const rawText = String(text || '').trim();
      const formatted = this.formatForSpeech(rawText);
      if (!formatted) {
        return { spoken: false, muted: false, reason: 'empty_text' };
      }

      const tone = this.inferTone(rawText, opts.tone);
      const profile = this.getProfile();

      this.stopAll();
      const mySeq = this._speakSeq;
      this._emitState('loading', { tone, profileId: profile.id });

      // 1. Provedor estático pré-gerado (latência <30ms, sem misturar timbres entre perfis)
      if (
        opts.clipId &&
        this.staticProvider &&
        typeof this.staticProvider.hasClip === 'function' &&
        this.staticProvider.hasClip(opts.clipId, profile.id)
      ) {
        try {
          const staticRes = await this.staticProvider.synthesize(formatted, {
            clipId: opts.clipId,
            voicePreset: profile.id,
            profileId: profile.id,
            tone
          });
          if (mySeq !== this._speakSeq) {
            return { spoken: false, muted: this._muted, cancelled: true };
          }
          this._emitState('static', { tone, profileId: profile.id, clipId: opts.clipId });
          return {
            spoken: true,
            muted: false,
            mode: 'static',
            provider: 'static',
            tone,
            text: formatted,
            clipId: opts.clipId,
            url: staticRes && staticRes.url ? staticRes.url : undefined
          };
        } catch (_err) {
          if (mySeq !== this._speakSeq) {
            return { spoken: false, muted: this._muted, cancelled: true };
          }
        }
      }

      // 2. Provedor Proxy Nuvem (POST /api/tts -> Gemini TTS) quando perfil não for offline_only
      if (
        profile.id !== 'offline_only' &&
        this.cloudProvider &&
        typeof this.cloudProvider.isAvailable === 'function' &&
        this.cloudProvider.isAvailable()
      ) {
        try {
          const cloudRes = await this.cloudProvider.synthesize(formatted, {
            voicePreset: profile.id,
            tone
          });
          if (mySeq !== this._speakSeq) {
            return { spoken: false, muted: this._muted, cancelled: true };
          }
          this._emitState('cloud', {
            tone,
            profileId: profile.id,
            cached: Boolean(cloudRes && cloudRes.cached)
          });
          return {
            spoken: true,
            muted: false,
            mode: 'cloud',
            provider: 'cloud',
            tone,
            text: formatted,
            cached: Boolean(cloudRes && cloudRes.cached),
            url: cloudRes && cloudRes.url ? cloudRes.url : undefined
          };
        } catch (_err) {
          if (mySeq !== this._speakSeq) {
            return { spoken: false, muted: this._muted, cancelled: true };
          }
        }
      }

      // 3. Fallback silencioso para Web Speech API PT-BR offline
      if (mySeq !== this._speakSeq) {
        return { spoken: false, muted: this._muted, cancelled: true };
      }
      this._emitState('offline', { tone, profileId: profile.id });
      try {
        const offlineRes = await this.offlineProvider.synthesize(formatted, {
          tone,
          profileId: profile.id
        });
        return {
          spoken: Boolean(offlineRes && offlineRes.spoken !== false),
          muted: false,
          mode: 'offline',
          provider: 'offline',
          tone,
          text: formatted
        };
      } catch (_err) {
        return {
          spoken: false,
          muted: false,
          mode: 'offline',
          provider: 'offline',
          tone,
          text: formatted
        };
      }
    }
  }

  const director = new LayaVoiceDirector();

  // Anexa constantes e construtores na instância e no módulo para testes Node/browser
  director.TONE_PRESETS = TONE_PRESETS;
  director.VOICE_PROFILES = VOICE_PROFILES;
  director.VOICE_PROFILE_ORDER = VOICE_PROFILE_ORDER;
  director.VOICE_STATES = VOICE_STATES;
  director.STATIC_CLIPS_MAP = STATIC_CLIPS_MAP;
  director.BaseTTSProvider = BaseTTSProvider;
  director.PrebakedStaticTTSProvider = PrebakedStaticTTSProvider;
  director.CloudProxyTTSProvider = CloudProxyTTSProvider;
  director.WebSpeechFallbackProvider = WebSpeechFallbackProvider;
  director.LayaVoiceDirector = LayaVoiceDirector;

  if (root) {
    root.LayaVoice = director;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      LayaVoice: director,
      TONE_PRESETS,
      VOICE_PROFILES,
      VOICE_PROFILE_ORDER,
      VOICE_STATES,
      STATIC_CLIPS_MAP,
      BaseTTSProvider,
      PrebakedStaticTTSProvider,
      CloudProxyTTSProvider,
      WebSpeechFallbackProvider,
      LayaVoiceDirector
    };
  }
})(typeof window !== 'undefined' ? window : globalThis);
