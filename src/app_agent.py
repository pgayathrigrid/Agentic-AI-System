import streamlit as st
from agent_system import agent, plan

# ✅ Must be first
st.set_page_config(page_title="Agentic AI System", layout="wide")

st.title("🤖 Agentic AI System")
st.write("Ask anything about IFC, stocks, or news")

# =========================
# ✅ MEMORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 💬 CHAT UI FIRST
# =========================

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
query = st.chat_input("Ask something...")

if query:
    # USER
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # AGENT
    tool = plan(query)

    with st.spinner("🤖 Thinking..."):
        result = agent(query)

    # RESPONSE
    response = f"""🧠 **Tool Used:** `{tool.upper()}`

📊 **Answer:**

{result}
"""

    st.chat_message("assistant").markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "tool": tool
    })

# =========================
# 📊 DASHBOARD (AFTER UPDATE)
# =========================

with st.sidebar:
    st.header("📊 Dashboard")

    if st.session_state.messages:
        user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
        assistant_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]

        st.metric("Total Queries", len(user_msgs))
        st.metric("Total Messages", len(st.session_state.messages))

        # Tool usage
        tool_counts = {}
        for msg in assistant_msgs:
            tool = msg.get("tool")
            if tool:
                tool_counts[tool] = tool_counts.get(tool, 0) + 1

        if tool_counts:
            st.subheader("🧠 Tool Usage")
            for t, count in tool_counts.items():
                st.write(f"{t.upper()} → {count}")

        # Last tool info
        if assistant_msgs:
            last_tool = assistant_msgs[-1].get("tool", "N/A")
            st.info(f"Last query used **{last_tool.upper()}** tool")

    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()