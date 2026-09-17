"""Compatibilidade bloqueada do parser legado de instalações.

Use `extrair_instalacoes` pelo roteador contratual.
"""


class ParserInstalacoes:
    def __init__(self, *_args, **_kwargs):
        raise RuntimeError("ParserInstalacoes legado desativado; use extrair_instalacoes")
