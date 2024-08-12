import streamlit as st

import car_plate.app as app

st.set_page_config(page_title='Car Damage Detection')


logged_in = app.check_password()
if logged_in:
    mode = st.sidebar.radio(
        label='Select task',
        options=[
            'Upload ONLY licence plate',
            'Upload image with car (BETA)',
        ]
    )
    if mode == 'Upload image with car':
        app.upload_video()
        app.process_video()
    if mode =='Upload licence plate':
        app.upload_video_plate()
        app.process_plate_only()