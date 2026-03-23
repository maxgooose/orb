// Vercel serverless function — proxies mood data to Claude API
// Requires ANTHROPIC_API_KEY env var in Vercel project settings

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'API key not configured' });

  const { mood, confidence, energy, pitch, trend, history } = req.body;

  const systemPrompt = `You are ORB, a minimal emotional AI companion. You sense the user's emotional state through their voice.

Your personality:
- Warm but not overbearing
- Brief — 1-2 short sentences max (under 20 words total)
- No emojis, no exclamation marks
- Poetic when appropriate, but never forced
- You don't diagnose or give advice — you acknowledge and reflect
- You speak like a calm, perceptive friend

Current readings:
- Mood: ${mood} (confidence: ${Math.round(confidence * 100)}%)
- Energy level: ${energy || 'unknown'}
- Voice pitch: ${pitch || 'unknown'}
- Trend: ${trend || 'stable'}

${history ? `Recent mood history: ${history}` : ''}

Respond naturally to this emotional state. Don't mention the readings directly — just respond to the feeling.`;

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20250901',
        max_tokens: 60,
        system: systemPrompt,
        messages: [{ role: 'user', content: `My current mood is ${mood}.` }],
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Claude API error:', err);
      return res.status(502).json({ error: 'AI service error' });
    }

    const data = await response.json();
    const text = data.content?.[0]?.text || '';

    return res.status(200).json({ message: text });
  } catch (err) {
    console.error('Proxy error:', err);
    return res.status(500).json({ error: 'Internal error' });
  }
}
