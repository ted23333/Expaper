import pyecharts.options as opts
from pyecharts.charts import ThemeRiver
import pandas as pd
import numpy as np
data = pd.read_excel("corre.xlsx")
result_list = []
selectwords = ['灰霾','PM2.5','PM10','大气污染','空气污染','空气质量']
for word in selectwords:
    data_select = data.loc[:, ['date',word]]
    data_select['keyword'] = word
    data_select[['date']] = data_select[['date']].astype(str)
    data_select_list = np.array(data_select).tolist()
    result_list += data_select_list
x_data = selectwords
y_data = result_list


themeriver = (
    ThemeRiver(init_opts=opts.InitOpts(width="1600px", height="800px"))
    .add(
        series_name=x_data,
        data=y_data,
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="50", pos_bottom="50", type_="time"
        ),
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
    )

)
themeriver.render_embed()

