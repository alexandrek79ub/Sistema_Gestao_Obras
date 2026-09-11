"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface ObraContextType {
  obraAtiva: string;
  setObraAtiva: (obra: string) => void;
  listaObras: string[];
}

const ObraContext = createContext<ObraContextType | undefined>(undefined);

export function ObraProvider({ children }: { children: ReactNode }) {
  const [obraAtiva, setObraAtiva] = useState<string>('OBRA_TMULT');
  const [listaObras, setListaObras] = useState<string[]>(['OBRA_TMULT', 'RESIDENCIAL_ALPHA']);

  useEffect(() => {
    fetch('/api/obras')
      .then(res => res.json())
      .then(data => {
        if (data && data.obras && data.obras.length > 0) {
          setListaObras(data.obras);
          if (!data.obras.includes(obraAtiva)) {
            setObraAtiva(data.obras[0]);
          }
        }
      })
      .catch(err => {
        console.error('Erro ao buscar lista de obras:', err);
        setListaObras(['OBRA_TMULT', 'RESIDENCIAL_ALPHA']);
      });
  }, []);

  return (
    <ObraContext.Provider value={{ obraAtiva, setObraAtiva, listaObras }}>
      {children}
    </ObraContext.Provider>
  );
}

export function useObra() {
  const context = useContext(ObraContext);
  if (context === undefined) {
    throw new Error('useObra deve ser usado dentro de um ObraProvider');
  }
  return context;
}
