"""Compatibilidade bloqueada do parser legado de arquitetura.

Use `extrair_arquitetura` pelo roteador contratual.
"""


class ParserArquitetura:
    def __init__(self, *_args, **_kwargs):
        raise RuntimeError("ParserArquitetura legado desativado; use extrair_arquitetura")
