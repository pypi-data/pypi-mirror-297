from ttgen import combinations as ttgen_combinations
from itertools import combinations as itert_combinations

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import polars as pl

from time import perf_counter_ns
from typing import NamedTuple

class Record(NamedTuple):
    test_set_name: str
    lib_name: str
    time_ns: int
    count: int
    all_count: int
    replication_index: int

class TestSet(NamedTuple):
    k_range: list[int]
    element_sets: list[int]

test_sets = {
    '1× each element': TestSet(range(2, 13), [i for i in range(22)]),
    '2× each element': TestSet(range(3, 14), [i for i in range(13)]*2),
    '5× each element': TestSet(range(3, 9), [i for i in range(5)]*7),
}

rows = []
for replication_index in range(3):
    for test_set_name, (k_range, element_set) in test_sets.items():
        for k in k_range:

            t0 = perf_counter_ns()
            found_1 = set()
            all_count = 0
            for i in itert_combinations(element_set, k):
                found_1.add(tuple(sorted(i)))
                all_count += 1
            count = len(found_1)
            t1 = perf_counter_ns()
            # print(f'{k=} Itertools: {t1 - t0:,} ns, {count}')

            rows.append(Record(
                test_set_name=test_set_name,
                lib_name='Itertools',
                time_ns=t1 - t0,
                count=len(found_1),
                all_count=all_count,
                replication_index=replication_index,
            ))

            t2 = perf_counter_ns()
            found_2 = set()
            for i in ttgen_combinations(element_set, k):
                found_2.add(tuple(sorted(i)))
            count = len(found_2)
            t3 = perf_counter_ns()
            # print(f'{k=} TTGen: {t3 - t2:,} ns, {count}')

            rows.append(Record(
                test_set_name=test_set_name,
                lib_name='TTGen',
                time_ns=t3 - t2,
                count=len(found_2),
                all_count=all_count,
                replication_index=replication_index,
            ))


df = pl.DataFrame(rows)
medians_df = df.group_by(['test_set_name', 'lib_name', 'count', 'all_count']).agg([
    pl.col('time_ns').median().alias('time_ns'),
]).sort(['test_set_name', 'lib_name', 'count'])

fig = make_subplots(rows=len(test_sets), cols=1, subplot_titles=[f'<span style="font-size: 0.8rem">{title}</span>' for title in list(test_sets.keys())])

for (test_set_name, lib_name), subset_df in medians_df.group_by(['test_set_name', 'lib_name']):
    colour = {'TTGen': '#636EFA', 'Itertools': '#EF553B'}.get(lib_name)
    row_num = list(test_sets.keys()).index(test_set_name)
    fig.add_trace(go.Scatter(
        x=subset_df['count'].to_list(),
        y=(subset_df['time_ns']/1e9).to_list(),
        name=lib_name,
        showlegend=True if row_num == 0 else False,
        legendgroup=lib_name,
        mode='markers+lines',
        marker=dict(color=colour),
    ), row=row_num+1, col=1)

fig.update_layout(
    xaxis1=dict(type='log'),
    yaxis1=dict(type='log'),
    xaxis2=dict(type='log'),
    yaxis2=dict(type='log'),
    xaxis3=dict(type='log'),
    yaxis3=dict(type='log'),
    title='Itertools vs TTGen performance',
    xaxis3_title='Count of result combinations',
    yaxis2_title='Runtime (s)',
)

fig.write_html('benchmarking/benchmarks.html')
fig.show('browser')