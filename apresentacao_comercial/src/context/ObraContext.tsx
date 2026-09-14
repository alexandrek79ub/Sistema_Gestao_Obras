"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface ObraContextType {
  obraAtiva: string;
  setObraAtiva: (obra: string) => void;
  listaObras: string[];
}

const ObraContext = createContext<ObraContextType | undefined>(undefined);

export function ObraProvider({ children }: { children: ReactNode }) {
  const [obraAtiva, setObraAtiva] = useState<string>('');
  const [listaObras, setListaObras] = useState<string[]>([]);

  useEffect(() => {
    fetch('/api/obras')
      .then(async (res) => {
        if (!res.ok) throw new Error('Não foi possível listar as obras disponíveis.');
        return res.json() as Promise<{ obras?: unknown }>;
      })
      .then(data => {
        const obras = Array.isArray(data?.obras) ? data.obras.filter((obra): obra is string => typeof obra === 'string') : [];
        setListaObras(obras);
        if (obras.length > 0) {
          setObraAtiva((atual) => obras.includes(atual) ? atual : obras[0]);
        } else {
          setObraAtiva('');
        }
      })
      .catch(err => {
        console.error('Erro ao buscar lista de obras:', err);
        setListaObras([]);
        setObraAtiva('');
      });
  }, []);

  return (
    <ObraContext.Provider value={{ obraAtiva, setObraAtiva, listaObras }}>
      {children}
    </ObraContext.Provider>
  );
}

export function useObra(): ObraContextType {
  const context = useContext(ObraContext);
  if (context === undefined) {
    throw new Error('useObra deve ser usado dentro de um ObraProvider');
  }
  return context;
}
