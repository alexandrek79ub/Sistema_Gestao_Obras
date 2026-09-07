import fs from 'fs';

export function parseCSV<T = Record<string, string>>(absolutePath: string): T[] {
  try {
    const fileContent = fs.readFileSync(absolutePath, 'utf-8');
    const lines = fileContent.split(/\r?\n/).filter(line => line.trim() !== '');

    if (lines.length === 0) return [];

    // Parse header and remove quotes
    const headers = lines[0].split(';').map(header => header.replace(/^"|"$/g, '').trim());
    
    const results: T[] = [];

    for (let i = 1; i < lines.length; i++) {
      const line = lines[i];
      const values = line.split(';').map(val => val.replace(/^"|"$/g, '').trim());
      
      const row: Record<string, string> = {};
      headers.forEach((header, index) => {
        row[header] = values[index] || '';
      });
      
      results.push(row as unknown as T);
    }

    return results;
  } catch (error) {
    console.error(`Erro ao ler arquivo CSV: ${absolutePath}`, error);
    return [];
  }
}
