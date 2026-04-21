# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 13:13:05 2026

@author: 32404
"""

# ==================== 银发智伴点 · 智慧养老可视化平台 ====================
# 文件名: yingfazhiban.py
# 技术栈：Streamlit + Plotly + Pandas
# 运行方式：streamlit run yingfazhiban.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="银发智伴点 · 智慧养老中枢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 模拟数据生成器 ====================
class DataSimulator:
    def __init__(self):
        self.num_elders = 120
        self.num_communities = 6
        self.communities = ["阳光社区", "翠湖苑", "颐景园", "康桥花园", "紫藤里", "春申苑"]
        self.elder_names = self._generate_names()
        self.df_elders = self._generate_elder_profiles()
        self.df_devices = self._generate_device_status()
        self.df_health_records = self._generate_health_history()
        self.df_alerts = self._generate_alert_history()
        self.df_activities = self._generate_activity_data()
        self.df_emotion = self._generate_emotion_data()
        self.df_nutrition = self._generate_nutrition_data()
        self.df_finance = self._generate_finance_data()
        self.df_staff = self._generate_staff_data()

    def _generate_names(self):
        surnames = ["张", "王", "李", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "马", "朱", "胡"]
        names = []
        for _ in range(self.num_elders):
            surname = random.choice(surnames)
            if random.random() > 0.5:
                name = surname + random.choice(["秀英", "桂兰", "玉珍", "淑芬", "淑华", "秀珍", "桂芳", "秀兰", "桂英", "玉兰"])
            else:
                name = surname + random.choice(["建国", "建华", "国栋", "志强", "伟国", "振华", "德福", "明德", "学文", "永强"])
            names.append(name)
        return names

    def _generate_elder_profiles(self):
        data = []
        for i in range(self.num_elders):
            age = random.randint(65, 92)
            gender = "女" if random.random() > 0.45 else "男"
            community = random.choice(self.communities)
            chronic = random.choices(["高血压", "糖尿病", "冠心病", "关节炎", "无"], weights=[0.3, 0.2, 0.15, 0.15, 0.2])[0]
            data.append({
                "elder_id": f"E{1000+i:04d}",
                "name": self.elder_names[i],
                "age": age,
                "gender": gender,
                "community": community,
                "room": f"{random.choice(['A','B','C'])}{random.randint(101,305)}",
                "chronic_disease": chronic,
                "care_level": random.choices(["一级", "二级", "三级"], weights=[0.3, 0.5, 0.2])[0],
                "emergency_contact": f"138****{random.randint(1000,9999)}",
                "device_id": f"DEV{2000+i:04d}"
            })
        return pd.DataFrame(data)

    def _generate_device_status(self):
        statuses = []
        for dev_id in self.df_elders["device_id"]:
            battery = random.randint(15, 100)
            online = random.random() > 0.05
            statuses.append({
                "device_id": dev_id,
                "device_type": random.choice(["智伴终端", "智能手环", "跌倒监测雷达"]),
                "battery": battery,
                "online": online,
                "signal": random.randint(60, 100) if online else 0,
                "last_heartbeat": datetime.now() - timedelta(minutes=random.randint(1, 120)) if online else datetime.now() - timedelta(hours=random.randint(5, 48)),
                "firmware_version": f"v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,15)}"
            })
        return pd.DataFrame(data=statuses)

    def _generate_health_history(self, days=30):
        records = []
        end = datetime.now()
        for _, elder in self.df_elders.iterrows():
            base_hr = random.randint(65, 80) if elder["age"] < 75 else random.randint(70, 85)
            base_sys = 120 + (elder["age"]-65)*0.8 + random.randint(-5, 15)
            base_dia = 80 + (elder["age"]-65)*0.3 + random.randint(-3, 8)
            base_spo2 = 97 + random.randint(-2, 2)
            for day in range(days):
                date = end - timedelta(days=day)
                hr = base_hr + np.random.normal(0, 4) + 5*np.sin(day/3)
                sys = base_sys + np.random.normal(0, 6)
                dia = base_dia + np.random.normal(0, 4)
                spo2 = base_spo2 + np.random.normal(0, 1)
                steps = max(0, int(np.random.normal(3500, 1500) + 1000*np.sin(day/5)))
                sleep_hours = random.uniform(5.5, 8.5)
                records.append({
                    "elder_id": elder["elder_id"],
                    "date": date.date(),
                    "heart_rate": round(hr, 1),
                    "systolic": round(sys, 1),
                    "diastolic": round(dia, 1),
                    "spo2": round(spo2, 1),
                    "steps": steps,
                    "sleep_hours": round(sleep_hours, 1)
                })
        return pd.DataFrame(data=records)

    def _generate_alert_history(self, days=14):
        alerts = []
        alert_types = ["跌倒检测", "心率异常", "血压过高", "离床超时", "手动求救", "设备离线"]
        weights = [0.05, 0.15, 0.1, 0.2, 0.05, 0.45]
        end = datetime.now()
        for _ in range(500):
            elder = self.df_elders.sample(1).iloc[0]
            alert_type = random.choices(alert_types, weights=weights)[0]
            timestamp = end - timedelta(hours=random.randint(1, 24*days), minutes=random.randint(0, 59))
            resolved = random.random() > 0.15
            response_time = random.randint(2, 25) if resolved else None
            alerts.append({
                "alert_id": f"ALT{random.randint(10000,99999)}",
                "elder_id": elder["elder_id"],
                "elder_name": elder["name"],
                "community": elder["community"],
                "alert_type": alert_type,
                "timestamp": timestamp,
                "resolved": resolved,
                "response_time_min": response_time,
                "severity": "高危" if alert_type in ["跌倒检测", "心率异常"] else "中危" if alert_type != "设备离线" else "低危"
            })
        return pd.DataFrame(data=alerts)

    def _generate_activity_data(self, days=30):
        activities = []
        activity_names = ["太极拳", "书法班", "合唱团", "智能手机课", "健康讲座", "棋牌活动", "手工制作", "戏曲欣赏"]
        for day in range(days):
            date = datetime.now().date() - timedelta(days=day)
            for act in activity_names:
                if random.random() > 0.4:
                    participants = random.randint(8, 35)
                    activities.append({
                        "date": date,
                        "activity": act,
                        "participants": participants,
                        "satisfaction": round(random.uniform(4.0, 5.0), 1)
                    })
        return pd.DataFrame(data=activities)

    def _generate_emotion_data(self, days=30):
        records = []
        for _, elder in self.df_elders.iterrows():
            base_pos = 0.6 if elder["age"] < 75 else 0.5
            for day in range(days):
                date = datetime.now().date() - timedelta(days=day)
                positive = np.clip(base_pos + np.random.normal(0, 0.1) + 0.05*np.sin(day/4), 0.2, 0.9)
                neutral = np.random.uniform(0.1, 0.3)
                negative = 1 - positive - neutral
                records.append({
                    "elder_id": elder["elder_id"],
                    "date": date,
                    "positive": round(positive, 3),
                    "neutral": round(neutral, 3),
                    "negative": round(negative, 3),
                    "loneliness_index": round(1 - positive + np.random.uniform(0, 0.2), 2)
                })
        return pd.DataFrame(data=records)

    def _generate_nutrition_data(self):
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        meals = []
        for date in dates:
            meals.append({"date": date.date(), "meal": "早餐", "calories": random.randint(350,500), "protein": random.randint(15,25), "fat": random.randint(8,15), "carbs": random.randint(40,70)})
            meals.append({"date": date.date(), "meal": "午餐", "calories": random.randint(600,800), "protein": random.randint(25,40), "fat": random.randint(15,30), "carbs": random.randint(70,100)})
            meals.append({"date": date.date(), "meal": "晚餐", "calories": random.randint(500,700), "protein": random.randint(20,35), "fat": random.randint(10,20), "carbs": random.randint(60,90)})
        return pd.DataFrame(data=meals)

    def _generate_finance_data(self):
        months = pd.date_range(start='2024-01-01', periods=12, freq='M')
        data = []
        for m in months:
            data.append({
                "month": m.strftime("%Y-%m"),
                "revenue_gov": random.randint(80, 150)*10000,
                "revenue_self": random.randint(20, 60)*10000,
                "cost_staff": random.randint(100, 180)*10000,
                "cost_device": random.randint(30, 80)*10000,
                "cost_operation": random.randint(20, 50)*10000
            })
        return pd.DataFrame(data=data)

    def _generate_staff_data(self):
        staff = []
        roles = ["护工", "护士", "康复师", "社工", "营养师"]
        names = ["王芳", "李敏", "刘强", "陈静", "赵磊", "孙丽", "周涛", "吴霞", "郑明", "林红"]
        for i in range(30):
            role = random.choice(roles)
            staff.append({
                "staff_id": f"S{100+i:03d}",
                "name": random.choice(names),
                "role": role,
                "community": random.choice(self.communities),
                "elders_assigned": random.randint(8,20) if role in ["护工","护士"] else random.randint(30,80),
                "avg_response_min": round(random.uniform(3.5,12.0),1),
                "satisfaction_score": round(random.uniform(4.2,5.0),1)
            })
        return pd.DataFrame(data=staff)

# 初始化数据
sim = DataSimulator()

# ==================== 【第一层：模块选择】 ====================
st.sidebar.title("🧓 银发智伴点")
module = st.sidebar.radio("请选择功能模块", [
    "🏠 平台总览",
    "❤️ 健康档案",
    "⚠️ 安全预警",
    "😊 情感分析",
    "📱 设备管理",
    "🎭 社区活动",
    "📊 运营分析"
])

st.sidebar.markdown("---")
st.sidebar.success("智慧养老 · 数据赋能 · 实时守护")

# ==================== 【第二层：各模块详细页面】 ====================

# ------------------------------
# 模块1：平台总览
# ------------------------------
if module == "🏠 平台总览":
    st.title("🏠 智慧养老中枢 · 总览")
    st.markdown("### 实时运营数据中心")

    online_dev = sim.df_devices["online"].sum()
    total_dev = len(sim.df_devices)
    total_elders = len(sim.df_elders)
    today_alerts = len(sim.df_alerts[sim.df_alerts["timestamp"].dt.date == datetime.now().date()])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("在线设备", f"{online_dev}/{total_dev}", f"{online_dev/total_dev*100:.1f}%")
    with col2:
        st.metric("服务长者", total_elders)
    with col3:
        st.metric("今日告警", today_alerts)
    with col4:
        st.metric("覆盖社区", len(sim.communities))

    # 图表
    c1, c2, c3 = st.columns([3,2,2])
    with c1:
        recent = sim.df_alerts.copy()
        recent["date"] = recent["timestamp"].dt.date
        trend = recent.groupby("date").size().tail(7)
        fig = px.line(trend, title="近7日告警趋势")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        com_count = sim.df_elders["community"].value_counts()
        fig = px.pie(values=com_count.values, names=com_count.index, title="社区覆盖")
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        alert_type = sim.df_alerts["alert_type"].value_counts()
        fig = px.bar(alert_type, title="告警类型")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🚨 实时告警")
    alerts = sim.df_alerts.nlargest(10, "timestamp")[["timestamp", "elder_name", "alert_type", "community", "severity"]]
    st.dataframe(alerts, use_container_width=True)

# ------------------------------
# 模块2：健康档案
# ------------------------------
elif module == "❤️ 健康档案":
    st.title("❤️ 长者健康档案")
    elder_option = st.selectbox("选择长者", sim.df_elders["name"])
    elder = sim.df_elders[sim.df_elders["name"] == elder_option].iloc[0]
    eid = elder["elder_id"]

    st.markdown(f"#### 基本信息")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("姓名", elder["name"])
    col2.metric("年龄", f"{elder['age']} 岁")
    col3.metric("社区", elder["community"])
    col4.metric("慢病", elder["chronic_disease"])

    health = sim.df_health_records[sim.df_health_records["elder_id"] == eid].sort_values("date")

    c1, c2 = st.columns([3,1])
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=health.date, y=health.heart_rate, name="心率"))
        fig.add_trace(go.Scatter(x=health.date, y=health.systolic, name="收缩压"))
        fig.update_layout(title="30天生命体征")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        cats = ["身体机能", "心理", "社交", "自理", "认知"]
        vals = [random.randint(60,95) for _ in cats]
        fig = go.Figure(go.Scatterpolar(r=vals, theta=cats, fill="toself"))
        fig.update_layout(title="健康评分")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("睡眠 & 步数")
    fig = px.bar(health, x="date", y="steps")
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# 模块3：安全预警
# ------------------------------
elif module == "⚠️ 安全预警":
    st.title("⚠️ 安全预警中心")
    df = sim.df_alerts.copy()
    df["date"] = df["timestamp"].dt.date

    c1, c2 = st.columns(2)
    with c1:
        by_date = df.groupby("date").size()
        st.plotly_chart(px.bar(by_date, title="每日告警趋势"), use_container_width=True)
    with c2:
        by_type = df["alert_type"].value_counts()
        st.plotly_chart(px.pie(values=by_type.values, names=by_type.index, title="告警类型占比"), use_container_width=True)

    st.subheader("告警记录")
    st.dataframe(df[["timestamp", "elder_name", "alert_type", "severity", "community"]].head(20), use_container_width=True)

# ------------------------------
# 模块4：情感分析
# ------------------------------
elif module == "😊 情感分析":
    st.title("😊 长者情感与孤独指数分析")
    emo = sim.df_emotion.groupby("date")[["positive","neutral","negative"]].mean()
    st.plotly_chart(px.area(emo, title="社区整体情感趋势"), use_container_width=True)

    lonely = sim.df_emotion.groupby("elder_id")["loneliness_index"].mean().nlargest(10)
    st.plotly_chart(px.bar(lonely, orientation="h", title="孤独指数 TOP10"), use_container_width=True)

# ------------------------------
# 模块5：设备管理
# ------------------------------
elif module == "📱 设备管理":
    st.title("📱 智能设备监控中心")
    devices = sim.df_devices.merge(sim.df_elders[["device_id","name","community"]], on="device_id")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("设备总数", len(devices))
    col2.metric("在线", devices["online"].sum())
    col3.metric("平均电量", f"{devices['battery'].mean():.0f}%")
    col4.metric("离线", len(devices)-devices["online"].sum())

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(devices, names="online", title="在线状态"), use_container_width=True)
    with c2:
        st.plotly_chart(px.histogram(devices, x="battery", title="电量分布"), use_container_width=True)

    st.dataframe(devices, use_container_width=True)

# ------------------------------
# 模块6：社区活动
# ------------------------------
elif module == "🎭 社区活动":
    st.title("🎭 社区文化活动中心")
    act = sim.df_activities
    st.plotly_chart(px.histogram(act, x="activity", y="participants", color="activity"), use_container_width=True)
    sat = act.groupby("activity")["satisfaction"].mean()
    st.plotly_chart(px.bar(sat, title="活动满意度"), use_container_width=True)

# ------------------------------
# 模块7：运营分析
# ------------------------------
elif module == "📊 运营分析":
    st.title("📊 机构运营数据分析")
    finance = sim.df_finance
    finance["total"] = finance["revenue_gov"] + finance["revenue_self"]
    st.plotly_chart(px.bar(finance, x="month", y="total", title="月度营收"), use_container_width=True)

    staff = sim.df_staff.groupby("role")["satisfaction_score"].mean()
    st.plotly_chart(px.bar(staff, title="员工满意度"), use_container_width=True)
