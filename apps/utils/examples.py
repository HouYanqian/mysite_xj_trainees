import datetime

from agent.models import ShenYeAccessRecord, Agent
from utils.tools import color_list, step_data


class ExamplesTemp:
    def __init__(self):
        self.axis_option = {
            'title': {},
            'tooltip': {
                'trigger': 'axis'
            },
            'legend': {
                'data': [
                    # '侯焱骞',
                ]
            },
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': 'true'
            },
            'toolbox': {
                'feature': {
                    'saveAsImage': {}
                }
            },
            'xAxis': {
                'type': 'category',
                'boundaryGap': 'false',
                'data': [
                    # 1, 2,
                ]
            },
            'yAxis': {
                'type': 'value'
            },
            'series': [
                # {
                #     'name': '侯焱骞',
                #     'type': 'line',
                #     'stack': '总量',
                #     'data': [120, 132, 101, 134, 90, 230, 210],
                #     'itemStyle': {'color': "#FF5722"}
                # },
            ],
            'animationDuration': 2000,
        }
        self.pie_option = {
            'title': {},
            'tooltip': {
                'trigger': 'item',
                'formatter': "{a} <br/>{b} : {c} ({d}%)"
            },
            'series': [
                {
                    'name': '占比',
                    'type': 'pie',
                    'radius': '60%',
                    'center': ['50%', '50%'],
                    'data': [
                        # {'value': 300, 'name': '侯焱骞', 'itemStyle': {'color': "#FF5722"}},
                    ],  # .sort(function (a, b) {return a.value - b.value}),
                    'roseType': 'angle',
                    'selectedMode': 'single',
                }
            ]
        }
        self.all_access_records = ShenYeAccessRecord.objects.all()
        self.today = datetime.datetime.today()

    def date_data(self, start_time, end_time, step, distinct=False):
        agents = Agent.objects.all()
        agent_count_dic = dict()
        objects = ShenYeAccessRecord.objects.filter(
            access_time__range=(start_time, end_time)
        )
        if distinct:
            objects = objects.distinct().values('ip').order_by('ip')
        for agent in agents:
            agent_access_records = objects.filter(
                agent__agent_name=agent.agent_name,
            )
            if agent_access_records:
                agent_count_dic[agent.agent_name] = agent_access_records
        agent_list = sorted(agent_count_dic.items(), key=lambda x: x[1].count(), reverse=True)
        for n in range(len(agent_list)):
            if n < len(color_list):
                agent_name, agent_records = agent_list[n]
                # 折线图数据
                self.axis_option['legend']['data'].append(agent_name)
                step_data_count = step_data(agent_records, start_time, end_time, step)
                self.axis_option['xAxis']['data'] = list(step_data_count.keys())
                self.axis_option['series'].append({
                    'name': agent_name,
                    'type': 'line',
                    'data': list(step_data_count.values()),
                    'itemStyle': {'color': color_list[n]}
                })

                # 饼状图数据
                self.pie_option['series'][0]['data'].append(
                    {'value': agent_records.count(), 'name': agent_name, 'itemStyle': {'color': color_list[n]}},
                )
        return self.axis_option, self.pie_option
