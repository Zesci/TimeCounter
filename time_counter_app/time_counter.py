import streamlit as st
import time
from datetime import datetime, timedelta

# Initialisieren des Streamlit State, falls noch nicht gesetzt
if 'target_time' not in st.session_state:
    st.session_state['target_time'] = datetime.now()
if 'costs' not in st.session_state:
    st.session_state['costs'] = 0.00
if 'participants' not in st.session_state:
    st.session_state['participants'] = 1
if 'countdown_active' not in st.session_state:
    st.session_state['countdown_active'] = False

COST_PER_SECOND_PER_PARTICIPANT = 0.01389  # Kosten pro Sekunde pro Teilnehmer


def countdown(t, display, costs_display):
    while t and st.session_state['countdown_active']:
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        # Ändern der Textfarbe basierend auf dem Status
        color = st.session_state.get('text_color', '#000000')  # Default Farbe Schwarz
        display.markdown(f"<h1 style='color:{color}; font-size: 60px;'>{timeformat}</h1>", unsafe_allow_html=True)
        # Aktualisieren des Kostenzählers
        st.session_state['costs'] += COST_PER_SECOND_PER_PARTICIPANT * st.session_state['participants']
        costs_display.markdown(
            f"<h1 style='color:{color}; font-size: 60px;'>Kosten: {st.session_state['costs']:.2f}€</h1>",
            unsafe_allow_html=True)
        time.sleep(1)
        t -= 1
        # Setzen der Textfarbe zurück auf Schwarz nach dem Blinken
        if st.session_state.get('blink', False):
            st.session_state['text_color'] = '#000000'
            st.session_state['blink'] = False


def modify_time(seconds, color):
    time_to_modify = timedelta(seconds=seconds)
    st.session_state['target_time'] += time_to_modify
    # Modifizieren der Kosten beim Modifizieren der Zeit
    st.session_state['costs'] += seconds * COST_PER_SECOND_PER_PARTICIPANT * st.session_state['participants']
    # Blinken der Textfarbe beim Modifizieren der Zeit
    st.session_state['text_color'] = color
    st.session_state['blink'] = True


def start_countdown():
    st.session_state['countdown_active'] = True


def set_countdown():
    st.session_state['countdown_initialized'] = False
    minutes = st.number_input('Countdown Dauer in Minuten', min_value=1, value=90)
    st.session_state['target_time'] = datetime.now() + timedelta(minutes=minutes)
    # Setzen der Anfangskosten
    st.session_state['costs'] = 0.00
    # Eingabe der Anzahl der Meetingteilnehmer
    st.session_state['participants'] = st.number_input('Anzahl der Meetingteilnehmer', min_value=1, value=4)
    if st.button('Countdown starten'):
        st.session_state['countdown_initialized'] = True
        start_countdown()


def main():
    # CSS für volle Breite und Schriftgröße
    st.markdown("""
        <style>
            .css-18e3th9 {
                padding: 0px !important;
            }
            .stButton>button {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title('Countdown Timer mit Kostenzähler und Teilnehmeranzahl')

    # Ermöglicht dem Benutzer, die Countdown-Dauer und die Teilnehmeranzahl bei App-Start festzulegen
    if not st.session_state.get('countdown_initialized', False):
        set_countdown()
    else:
        # Platzhalter für den Countdown und Kostenzähler
        countdown_display = st.empty()
        costs_display = st.empty()

        # Buttons zum Modifizieren der Countdown-Zeit
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Zeit reduzieren (-60s)'):
                modify_time(-60, '#7CFC00')  # Grün
        with col2:
            if st.button('Zeit erhöhen (+60s)'):
                modify_time(60, '#FF0000')  # Rot

        # Starten des Countdowns, wenn aktiv
        if st.session_state['countdown_active']:
            remaining_seconds = int((st.session_state['target_time'] - datetime.now()).total_seconds())
            countdown(remaining_seconds, countdown_display, costs_display)


if __name__ == "__main__":
    main()
