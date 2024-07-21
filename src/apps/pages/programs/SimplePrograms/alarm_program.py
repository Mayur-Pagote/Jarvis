import streamlit as st
import datetime
import time
# Function to check the alarm and notify
def check_alarm():
    alarm_time = st.session_state.alarm_time
    snooze_time = st.session_state.snooze_time
    alarm_message = st.session_state.alarm_message
    alarm_note = st.session_state.alarm_note
    while True:
        # Get current time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        # Check if the alarm time matches the current time
        if current_time == alarm_time:
            st.session_state.alarm_triggered = True
            st.session_state.alarm_message = alarm_message
            st.session_state.alarm_note = alarm_note
            break
        # Check if snooze time is set and if it's time to trigger snooze
        if st.session_state.snooze_triggered:
            snooze_alarm_time = (datetime.datetime.now() + datetime.timedelta(minutes=snooze_time)).strftime("%H:%M:%S")
            if current_time == snooze_alarm_time:
                st.session_state.alarm_triggered = True
                st.session_state.alarm_message = alarm_message
                st.session_state.alarm_note = alarm_note
                st.session_state.snooze_triggered = False
                break
        # Wait for one second
        time.sleep(1)
# Streamlit app code
def Alarm_App():
    st.title("Alarm Clock")
    # Initialize session state
    if 'alarm_triggered' not in st.session_state:
        st.session_state.alarm_triggered = False
    if 'snooze_triggered' not in st.session_state:
        st.session_state.snooze_triggered = False
    if 'snooze_time' not in st.session_state:
        st.session_state.snooze_time = 0
    # Input for hour, minute, and second
    hour = st.selectbox("Hour", list(range(24)), format_func=lambda x: f"{x:02d}")
    minute = st.selectbox("Minute", list(range(60)), format_func=lambda x: f"{x:02d}")
    second = st.selectbox("Second", list(range(60)), format_func=lambda x: f"{x:02d}")
    # Create alarm time
    alarm_time = f"{hour:02d}:{minute:02d}:{second:02d}"
   # Message options
    message_option = st.radio(
        "Choose Alarm Message Option",
        ("None", "Custom Message", "Predefined Message")
    )
    if message_option == "Custom Message":
        alarm_message = st.text_input("Enter your custom message", "Time's up!")
    elif message_option == "Predefined Message":
        predefined_messages = ["Wake up!", "Meeting time!", "Take a break!"]
        alarm_message = st.selectbox("Choose a predefined message", predefined_messages)
    else:
        alarm_message = "Time's up!"
    # Note/Link options
    note_option = st.radio(
        "Choose Note/Link Option",
        ("None", "Custom Note/Link")
    )
    if note_option == "Custom Note/Link":
        alarm_note = st.text_area("Enter your link or note here", "")
    else:
        alarm_note = "No note or link"
    # Snooze functionality
    snooze_time = st.number_input("Snooze Time (minutes)", min_value=0, max_value=60, value=0)
    # Set alarm button
    if st.button("Set Alarm"):
        st.session_state.alarm_time = alarm_time
        st.session_state.alarm_message = alarm_message
        st.session_state.alarm_note = alarm_note
        st.session_state.snooze_time = snooze_time
        st.session_state.snooze_triggered = False
        st.success(f"Alarm set for {alarm_time} with message: '{alarm_message}' and note: '{alarm_note}'")
        check_alarm()
    # Display alarm notification if triggered
    if st.session_state.alarm_triggered:
        st.balloons()
        st.warning(st.session_state.alarm_message)
        st.info(f"Note/Link: {st.session_state.alarm_note}")
        st.session_state.alarm_triggered = False
