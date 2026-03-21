// ORB — IndexedDB mood storage
// Stores sessions and mood entries for journal + analytics

const DB_NAME = 'orb-mood';
const DB_VERSION = 1;

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = e => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains('sessions')) {
        const store = db.createObjectStore('sessions', { keyPath: 'id', autoIncrement: true });
        store.createIndex('date', 'date');
      }
      if (!db.objectStoreNames.contains('entries')) {
        const store = db.createObjectStore('entries', { keyPath: 'id', autoIncrement: true });
        store.createIndex('sessionId', 'sessionId');
        store.createIndex('timestamp', 'timestamp');
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function startSession() {
  const db = await openDB();
  const tx = db.transaction('sessions', 'readwrite');
  const now = new Date();
  const session = {
    date: now.toISOString().slice(0, 10),
    startTime: now.toISOString(),
    endTime: null,
    moodSummary: {},
    dominantMood: 'neutral',
    entryCount: 0,
    note: ''
  };
  return new Promise((resolve, reject) => {
    const req = tx.objectStore('sessions').add(session);
    req.onsuccess = () => resolve(req.result); // returns session id
    req.onerror = () => reject(req.error);
  });
}

export async function endSession(sessionId, summary) {
  const db = await openDB();
  const tx = db.transaction('sessions', 'readwrite');
  const store = tx.objectStore('sessions');
  return new Promise((resolve, reject) => {
    const req = store.get(sessionId);
    req.onsuccess = () => {
      const session = req.result;
      if (!session) return reject(new Error('Session not found'));
      session.endTime = new Date().toISOString();
      Object.assign(session, summary);
      store.put(session);
      resolve(session);
    };
    req.onerror = () => reject(req.error);
  });
}

export async function addEntry(sessionId, mood, confidence, features) {
  const db = await openDB();
  const tx = db.transaction('entries', 'readwrite');
  const entry = {
    sessionId,
    timestamp: new Date().toISOString(),
    mood,
    confidence,
    pitch: features.pitch,
    energy: features.energy,
    speakingRate: features.speakingRate,
  };
  return new Promise((resolve, reject) => {
    const req = tx.objectStore('entries').add(entry);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function getSessions(limit = 50) {
  const db = await openDB();
  const tx = db.transaction('sessions', 'readonly');
  return new Promise((resolve, reject) => {
    const req = tx.objectStore('sessions').index('date').getAll();
    req.onsuccess = () => resolve(req.result.reverse().slice(0, limit));
    req.onerror = () => reject(req.error);
  });
}

export async function getSessionEntries(sessionId) {
  const db = await openDB();
  const tx = db.transaction('entries', 'readonly');
  return new Promise((resolve, reject) => {
    const req = tx.objectStore('entries').index('sessionId').getAll(sessionId);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function getAllEntries(days = 30) {
  const db = await openDB();
  const tx = db.transaction('entries', 'readonly');
  const cutoff = new Date(Date.now() - days * 86400000).toISOString();
  return new Promise((resolve, reject) => {
    const req = tx.objectStore('entries').index('timestamp').getAll(IDBKeyRange.lowerBound(cutoff));
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function exportData() {
  const sessions = await getSessions(999);
  const db = await openDB();
  const tx = db.transaction('entries', 'readonly');
  const entries = await new Promise((resolve, reject) => {
    const req = tx.objectStore('entries').getAll();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return { sessions, entries, exportDate: new Date().toISOString() };
}
