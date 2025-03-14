import streamlit as st

pages = {
    "Registration": [
        st.Page("route/register.py", title="CGT'25"),
        # st.Page("trial.py", title="Try it out"),
    ],
    # "Thank You For Coming": [
    #     st.Page("route/feedback.py", title="Feedback")
    # ],
    # "Campaign": [
    #     st.Page("route/vote.py", title="Vote your Candidate"),
    #     st.Page("route/stats.py", title="Campaign Statistics"),
    #     st.Page("route/support.py", title="Support your Candidate"),
    # ],
}

pg = st.navigation(pages, expanded=True)
pg.run()

st.logo("assets/favicon.png")