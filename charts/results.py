import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar


def draw_result_bar(df: pd.DataFrame, n_scors: int = 3) -> Bar:
    params_columns = df.columns[:-n_scors]
    scores_columns = df.columns[-n_scors:]
    x_data = (
        df[params_columns]
        .apply(
            lambda x: "\n".join([f"{name}_{value}" for name, value in zip(params_columns, x)]),
            axis=1,
        )
        .values.tolist()
    )
    bar = (
        Bar()
        .add_xaxis(x_data)
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(selected_mode="single"),
        )
    )
    for col in scores_columns:
        bar.add_yaxis(col, df[col].values.tolist())
    bar.set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
    )

    return bar
