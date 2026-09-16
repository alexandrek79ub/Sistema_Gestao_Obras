import re

from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    erros_console: list[str] = []
    page.on("console", lambda message: erros_console.append(message.text) if message.type == "error" else None)

    tarefas = [
        {"id": 1, "pav": "Zona 01", "tipo": "Fundação", "vagao": "02. Fundações", "color": "bg-blue-600", "start": 1, "duration": 12, "equipe": "Equipe A", "dataInicio": "01/10/2026", "dataFim": "12/10/2026"},
        {"id": 2, "pav": "Zona 02", "tipo": "Fundação", "vagao": "02. Fundações", "color": "bg-blue-600", "start": 7, "duration": 12, "equipe": "Equipe A", "dataInicio": "07/10/2026", "dataFim": "18/10/2026"},
    ]
    cronograma = {
        "tarefas": tarefas,
        "vagoesFluxo": [{
            "id": "02-fundacoes",
            "nome": "02. Fundações",
            "equipe": "Equipe A",
            "color": "bg-blue-600",
            "pontos": [
                {"id": 1, "pav": "Zona 01", "start": 1, "duration": 12},
                {"id": 2, "pav": "Zona 02", "start": 7, "duration": 12},
            ],
            "startMin": 1,
            "endMax": 19,
        }],
        "pavimentos": ["Zona 01", "Zona 02"],
        "totalDias": 182,
        "cpm": [],
        "curvaS": [],
        "lotesCurtoPrazo": [],
        "histogramaMensal": [],
        "histogramaPorFuncao": [],
        "resumoHistograma": {"totalGeralHH": 0, "totalHeadcountMeses": 0, "mediaHeadcount": 0, "picoHeadcount": 0},
        "relatorioSobreposicao": None,
        "metaGlobal": {"diasCorridos": 180, "semanas": 26, "valorTurnkey": 0, "caminhoCriticoDias": 0},
    }
    page.route("**/api/obras", lambda route: route.fulfill(json={"obras": ["OBRA_TESTE"]}))
    page.route("**/api/cronograma?*", lambda route: route.fulfill(json=cronograma))

    page.goto("http://127.0.0.1:3000/dashboard/cronograma", wait_until="networkidle")
    page.get_by_role("button", name=re.compile("Longo Prazo: Linha de Balanço")).click()
    page.get_by_role("button", name="Blocos Mestres (Engenharia)").wait_for()

    assert page.get_by_test_id("lob-blocks-layer").count() == 1
    assert page.get_by_test_id("lob-lines-layer").count() == 0

    page.get_by_role("button", name="Linhas Contínuas").click()
    page.get_by_test_id("lob-lines-layer").wait_for()
    assert page.locator('rect[fill="url(#stripe-sobreposicao)"]').count() == 0

    botao_sobreposicoes = page.get_by_role("button", name="Ver sobreposições potenciais")
    if botao_sobreposicoes.is_enabled():
        botao_sobreposicoes.click()
        assert page.locator('rect[fill="url(#stripe-sobreposicao)"]').count() > 0

    page.screenshot(path="tests/lob-corrigida.png", full_page=True)
    assert not erros_console, f"Erros no console do navegador: {erros_console}"
    browser.close()
