"use client";

import React from 'react';
import { useObra } from '@/context/ObraContext';

export default function ProjectSelector() {
  const { obraAtiva, setObraAtiva, listaObras } = useObra();

  if (listaObras.length <= 1) {
    return <h2 className="text-xl font-semibold text-zinc-100">Projeto: {obraAtiva}</h2>;
  }

  return (
    <div className="flex items-center space-x-2">
      <h2 className="text-xl font-semibold text-zinc-100">Projeto:</h2>
      <select 
        value={obraAtiva}
        onChange={(e) => setObraAtiva(e.target.value)}
        className="bg-zinc-800 text-white text-lg font-semibold border border-zinc-700 rounded-md px-3 py-1 focus:outline-none focus:border-blue-500"
      >
        {listaObras.map(obra => (
          <option key={obra} value={obra}>{obra}</option>
        ))}
      </select>
    </div>
  );
}
