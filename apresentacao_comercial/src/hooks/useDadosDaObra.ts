"use client";

import { useEffect, useState } from 'react';
import { useObra } from '@/context/ObraContext';

export interface EstadoDadosObra<T> {
  data: T;
  loading: boolean;
  error: string | null;
}

export function useDadosDaObra<T>(endpoint: string, valorInicial: T): EstadoDadosObra<T> {
  const { obraAtiva } = useObra();
  const [valorInicialEstavel] = useState(() => valorInicial);
  const [state, setState] = useState<EstadoDadosObra<T> & { obra: string | null }>({ data: valorInicialEstavel, loading: false, error: null, obra: null });

  useEffect(() => {
    if (!obraAtiva) {
      return;
    }
    const controller = new AbortController();
    fetch(`${endpoint}?obra=${encodeURIComponent(obraAtiva)}`, { signal: controller.signal })
      .then(async (resposta) => {
        const corpo = await resposta.json() as T & { error?: string };
        if (!resposta.ok) throw new Error(corpo.error || 'Falha ao carregar dados da obra.');
        return corpo;
      })
      .then((data) => setState({ data, loading: false, error: null, obra: obraAtiva }))
      .catch((error: unknown) => {
        if ((error as DOMException).name !== 'AbortError') {
          setState({ data: valorInicialEstavel, loading: false, error: error instanceof Error ? error.message : 'Falha ao carregar dados da obra.', obra: obraAtiva });
        }
      });
    return () => controller.abort();
  }, [endpoint, obraAtiva, valorInicialEstavel]);

  if (!obraAtiva) return { data: valorInicialEstavel, loading: false, error: 'Nenhuma obra disponível para consulta.' };
  if (state.obra !== obraAtiva) return { data: valorInicialEstavel, loading: true, error: null };
  return state;
}
