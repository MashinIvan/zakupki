### 1. Install python and pip

[link](https://www.python.org/)

### 2. Install dependencies

```bash
pip install pipenv
pipenv install
```

### 3. Set all required filters on [zakupki](https://zakupki.gov.ru/epz/order/extendedsearch/results.html)
or you can use example url below (copy it and paste when program launches)
```python
example_url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&currencyIdGeneral=-1&selectedSubjectsIdNameHidden=%7B%7D&participantName=7724931166&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D"
```

### 4. Run the app

```bash
python main.py scrap --limit 5
python main.py scrap-headless
```

parameters:

- --limit : limit number of observations
