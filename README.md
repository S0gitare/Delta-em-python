# Delta Calculator

**Calculadora de equações do segundo grau com visualização gráfica.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Testes](https://img.shields.io/badge/Testes-28%20passando-brightgreen?logo=pytest)

Dados os coeficientes **a**, **b** e **c**, resolve `ax² + bx + c = 0`, classifica as raízes (reais ou complexas) e plota a parábola com as raízes marcadas no gráfico.

---

## Instalação

```bash
git clone https://github.com/S0gitare/Delta-em-python.git
cd Delta-em-python
pip install -e ".[dev]"
```

## Uso

```bash
# Modo interativo
python Delta.py

# Passar os coeficientes direto pela linha de comando
python Delta.py 1 -5 6

# Salvar o gráfico em arquivo
python Delta.py 1 -5 6 --save grafico.png
```

## Testes

```bash
python -m pytest tests/ -v --cov=src
```

---

Feito com [NumPy](https://numpy.org) · [Matplotlib](https://matplotlib.org) · [pytest](https://pytest.org)
