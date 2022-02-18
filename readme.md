# stock-backtrader-web-app

回测看板

* [akshare](https://github.com/akfamily/akshare)，获取数据
* [backtrader](https://github.com/mementum/backtrader)，回测
* [pyecharts](https://github.com/pyecharts/pyecharts)，可视化
* [streamlit](https://github.com/streamlit/streamlit)，web搭建

## 依赖
```shell
pip install -r requirements.txt
```

## 运行
```shell
streamlit run backtrader_app.py
```

## 策略
```shell
python -m unittest tests.MaStrategyTest
```