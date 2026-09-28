from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Student Performance Analytics",page_icon="🎓",layout="wide")
BASE=Path(__file__).parent
st.title("🎓 Student Performance Analytics")
st.caption("Synthetic education dataset for demonstrating descriptive analytics. This is not a validated student-risk or grading system.")
@st.cache_data
def load(): return pd.read_csv(BASE/"data/student_performance.csv")
df=load()
with st.sidebar:
    st.header("Filters")
    programs=st.multiselect("Program",sorted(df.program.unique()),default=sorted(df.program.unique()))
    bands=st.multiselect("Performance band",['At risk','Developing','Proficient','Excellent'],default=['At risk','Developing','Proficient','Excellent'])
    min_att=st.slider("Minimum attendance (%)",0,100,0)
f=df[df.program.isin(programs)&df.performance_band.isin(bands)&(df.attendance_pct>=min_att)]
a,b,c,d=st.columns(4)
a.metric("Students",f"{len(f):,}"); b.metric("Average final score",f"{f.final_score.mean():.1f}" if len(f) else "—"); c.metric("Average attendance",f"{f.attendance_pct.mean():.1f}%" if len(f) else "—"); d.metric("At-risk count",f"{(f.performance_band=='At risk').sum():,}")
left,right=st.columns(2)
left.plotly_chart(px.histogram(f,x="final_score",nbins=20,title="Final score distribution"),use_container_width=True)
right.plotly_chart(px.box(f,x="program",y="final_score",color="program",title="Final score by program"),use_container_width=True)
left,right=st.columns(2)
right.plotly_chart(px.scatter(f,x="attendance_pct",y="final_score",color="performance_band",hover_data=["student_id","program"],title="Attendance vs. final score"),use_container_width=True)
band=f.performance_band.value_counts().reindex(['At risk','Developing','Proficient','Excellent'],fill_value=0).rename_axis('performance_band').reset_index(name='students')
left.plotly_chart(px.bar(band,x="performance_band",y="students",title="Students by performance band"),use_container_width=True)
st.subheader("Program summary")
summary=f.groupby("program",as_index=False).agg(students=("student_id","count"),avg_attendance=("attendance_pct","mean"),avg_assignment=("assignment_avg","mean"),avg_midterm=("midterm_score","mean"),avg_final=("final_score","mean")).round(1)
st.dataframe(summary,use_container_width=True,hide_index=True)
st.subheader("Student-level data")
st.dataframe(f,use_container_width=True,hide_index=True)
st.download_button("Download filtered student data",f.to_csv(index=False).encode(),"student_performance_filtered.csv","text/csv")
st.caption("Use aggregated findings for learning support. Avoid labeling or making consequential decisions about individual students from this synthetic demo.")
