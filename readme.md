# Stock Backtrader Web App

## 项目简介

本项目是一个基于 Python 的股票回测 Web 应用，使用了 Streamlit、AkShare、Backtrader 和 Pyecharts 四个核心库。该应用提供了一个用户友好的界面，允许用户获取股票数据、运行回测分析，并通过图表直观地展示结果。

**推荐**
- [FinVizAI](https://github.com/chenwr727/FinVizAI.git) 一键生成股票与期货分析视频
- [akshare-gpt](https://github.com/chenwr727/akshare-gpt.git) 将 Akshare 集成到 GPT 的工具中，实现自然语言问答。

## 主要功能

- **股票数据获取**：通过 AkShare 实时获取股票市场数据。
- **回测分析**：利用 Backtrader 进行多种策略的回测分析。
- **数据可视化**：使用 Pyecharts 实现回测结果的可视化展示。
- **Web 界面**：通过 Streamlit 搭建易用的交互式 Web 界面。

## 技术栈

- **[Streamlit](https://github.com/streamlit/streamlit)**：快速搭建数据应用的 Web 框架。
- **[AkShare](https://github.com/akfamily/akshare)**：金融数据获取库。
- **[Backtrader](https://github.com/mementum/backtrader)**：强大的回测框架，支持多种金融工具。
- **[Pyecharts](https://github.com/pyecharts/pyecharts)**：基于 Python 的数据可视化库。

## 安装依赖

在开始使用本项目之前，请确保已安装所有依赖。你可以通过以下命令安装：

```bash
pip install -r requirements.txt
```

## 运行应用

要启动 Web 应用，运行以下命令：

```bash
streamlit run backtrader_app.py
```

## 策略测试

你可以使用以下命令运行示例策略的单元测试：

```bash
python -m unittest tests.MaStrategyTest
```

本项目支持的策略包括：
- **MA**（移动平均线）
- **MACross**（均线交叉）

## 使用的库及其参数说明

### Streamlit
Streamlit 是一个用于快速开发数据可视化应用的 Web 框架。

![Streamlit 界面示例](https://i-blog.csdnimg.cn/blog_migrate/0d139c7f5891abb7ea9420627eddb3b8.png)

### AkShare
AkShare 是一个基于 Python 的金融数据接口库，提供丰富的数据源接口。

![AkShare 参数说明](https://i-blog.csdnimg.cn/blog_migrate/7424d1bb9a93931c27d206924e44b147.png)
- **symbol**：股票代码
- **period**：数据颗粒度（如日线、周线）
- **start date**：查询数据的开始日期
- **end date**：查询数据的结束日期
- **adjust**：复权类型（默认不复权；`qfq`：前复权；`hfq`：后复权）

### Backtrader
Backtrader 是一个用于量化交易的回测框架，支持多种交易策略的回测。

![Backtrader 参数说明](https://i-blog.csdnimg.cn/blog_migrate/a50e3fb6787ae0fe6513b24d35e347b6.png)
- **backtrader start date**：回测开始时间
- **backtrader end date**：回测结束时间
- **start cash**：初始资本
- **commission fee**：交易佣金费率
- **stake**：每次交易的买入数量

### Pyecharts
Pyecharts 是一个结合了 Python 和 Echarts 的数据可视化工具，支持丰富的图表类型。

![Pyecharts Kline 示例](https://i-blog.csdnimg.cn/blog_migrate/a7d7f43891664654909a4bd232dd50bc.png)
