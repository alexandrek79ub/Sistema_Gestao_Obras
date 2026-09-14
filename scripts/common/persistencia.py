"""Persistência segura para artefatos de obra.

Serializa mutações por recurso e promove arquivos temporários somente por troca
atômica no mesmo diretório. O arquivo oficial nunca é aberto para escrita direta.
"""

import json
import os
import tempfile
import time
from contextlib import contextmanager


class TimeoutBloqueio(RuntimeError):
    """Indica que uma mutação concorrente não liberou o recurso a tempo."""


@contextmanager
def bloquear_recurso(diretorio, recurso, timeout_segundos=15, intervalo_segundos=0.05):
    """Obtém lock exclusivo por arquivo, com timeout e recuperação de lock obsoleto."""
    os.makedirs(diretorio, exist_ok=True)
    lock_path = os.path.join(diretorio, f".{recurso}.lock")
    limite = time.monotonic() + timeout_segundos
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as lock_file:
                lock_file.write(str(os.getpid()))
                lock_file.flush()
                os.fsync(lock_file.fileno())
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(lock_path) > timeout_segundos:
                    os.unlink(lock_path)
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= limite:
                raise TimeoutBloqueio(f"Recurso ocupado: {recurso}")
            time.sleep(intervalo_segundos)
    try:
        yield
    finally:
        try:
            os.unlink(lock_path)
        except FileNotFoundError:
            pass


def _escrever_atomico(caminho, escritor):
    diretorio = os.path.dirname(caminho)
    os.makedirs(diretorio, exist_ok=True)
    fd, temporario = tempfile.mkstemp(prefix=f".{os.path.basename(caminho)}.", suffix=".tmp", dir=diretorio)
    try:
        with os.fdopen(fd, "wb") as arquivo:
            escritor(arquivo, temporario)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, caminho)
    except Exception:
        try:
            os.unlink(temporario)
        except FileNotFoundError:
            pass
        raise


def salvar_texto_atomico(caminho, conteudo, encoding="utf-8"):
    def escrever(arquivo, _):
        arquivo.write(conteudo.encode(encoding))
    _escrever_atomico(caminho, escrever)


def salvar_json_atomico(caminho, dados, indent=2):
    salvar_texto_atomico(caminho, json.dumps(dados, ensure_ascii=False, indent=indent) + "\n")


def salvar_workbook_atomico(caminho, workbook):
    diretorio = os.path.dirname(caminho)
    os.makedirs(diretorio, exist_ok=True)
    fd, temporario = tempfile.mkstemp(prefix=f".{os.path.basename(caminho)}.", suffix=".tmp", dir=diretorio)
    os.close(fd)
    try:
        workbook.save(temporario)
        with open(temporario, "rb") as arquivo:
            os.fsync(arquivo.fileno())
        os.replace(temporario, caminho)
    except Exception:
        try:
            os.unlink(temporario)
        except FileNotFoundError:
            pass
        raise
