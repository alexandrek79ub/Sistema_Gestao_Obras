import { DatabaseSync } from 'node:sqlite';
import path from 'path';
import fs from 'fs';

export function getDb(): DatabaseSync | null {
  const candidates = [
    process.env.SQLITE_DB_PATH,
    path.resolve(process.cwd(), '../data/pmo_virtual.sqlite'),
    path.resolve(process.cwd(), 'data/pmo_virtual.sqlite'),
  ].filter(Boolean) as string[];

  const dbPath = candidates.find(p => fs.existsSync(p));
  if (!dbPath) {
    return null;
  }

  try {
    return new DatabaseSync(dbPath, { readOnly: true });
  } catch (err) {
    console.error('Falha ao conectar no SQLite:', err);
    return null;
  }
}
