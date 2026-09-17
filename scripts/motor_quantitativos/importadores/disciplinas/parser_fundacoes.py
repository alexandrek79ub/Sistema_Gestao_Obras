"""Compatibilidade bloqueada do parser legado de fundações.

Use `ParserFundacoesContrato` pelo roteador contratual. Este módulo não possui
valores de obra, fórmulas executáveis, preços ou fallbacks.
"""


class ParserFundacoes:
    def __init__(self, *_args, **_kwargs):
        raise RuntimeError("ParserFundacoes legado desativado; use ParserFundacoesContrato")
