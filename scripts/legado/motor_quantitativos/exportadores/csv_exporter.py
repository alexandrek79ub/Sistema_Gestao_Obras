import csv
from pathlib import Path
from typing import Any, Iterable

def escrever_csv(destino: Path, cabecalho: tuple[str, ...], linhas: Iterable[Iterable[Any]]) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
        writer = csv.writer(arquivo, delimiter=";")
        writer.writerow(cabecalho)
        writer.writerows(linhas)
