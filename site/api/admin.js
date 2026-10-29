import { redis, body } from './_redis.js';

// Presenter-only actions, gated by ADMIN_KEY: set the live checkpoint, hide a question.
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  const b = body(req);
  if (!process.env.ADMIN_KEY || b.key !== process.env.ADMIN_KEY) return res.status(401).json({ error: 'no' });
  if (b.action === 'state') await redis([['SET', 'ship:state', String(Math.min(Math.max(parseInt(b.cp) || 1, 1), 3))]]);
  else if (b.action === 'hide') await redis([['SADD', 'ship:hidden', String(b.id).slice(0, 20)]]);
  else if (b.action === 'unhide') await redis([['SREM', 'ship:hidden', String(b.id).slice(0, 20)]]);
  else if (b.action === 'clear') {
    const [ids] = await redis([['HKEYS', 'ship:q']]);
    await redis([['DEL', 'ship:q', 'ship:votes', 'ship:hidden', ...(ids || []).map(id => 'ship:voters:' + id)], ['SET', 'ship:state', '1']]);
  }
  else return res.status(400).json({ error: 'unknown action' });
  res.status(200).json({ ok: true });
}
