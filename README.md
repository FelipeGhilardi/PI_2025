
# Simulação Execução x Planejado (rótulos MakeSense)

Este app **não treina modelo**. Ele **lê os .txt** exportados pelo MakeSense (formato YOLO) e
usa como se fossem a saída da visão computacional. Assim você tem um protótipo rápido e fiel ao que a banca espera.

## Estrutura
- `fotos/` imagens originais (copiadas do seu `Fotos.zip`)
- `overlays/` imagens com as caixas desenhadas
- `executado_counts.csv` contagem por imagem
- `classes.json` nomes de classes (se havia `classes.txt`)
- `planejado.xlsx` cópia do seu Excel para leitura automática (ajuste colunas para "Dia", "Classe", "Quantidade")

## Como rodar
```bash
pip install -r requirements.txt
streamlit run app.py
```
Abra o link local que aparecer no terminal.

## Observações
- O app tenta **inferir o "Dia"** a partir das pastas/nomes dos arquivos (ex.: `Dia1`, `day2`).
- O app tenta reconhecer automaticamente no Excel as colunas equivalentes a **Dia / Classe / Quantidade**.
  Se os nomes forem diferentes, renomeie as colunas no Excel ou altere a heurística no `app.py`.
