declare module 'node:sqlite' {
  export class DatabaseSync {
    constructor(location: string, options?: { readOnly?: boolean });
    prepare(sql: string): {
      all(...params: any[]): any[];
      get(...params: any[]): any;
      run(...params: any[]): { changes: number; lastInsertRowid: number };
    };
    close(): void;
  }
}
