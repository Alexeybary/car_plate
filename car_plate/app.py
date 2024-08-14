import streamlit as st
import cv2

from car_plate.processors import ocr_recognition
ss = st.session_state

def password_entered():
    st.session_state["pass_correct"] = True if (
            st.session_state["password"] == st.secrets["password"]
    ) else False


def check_password():
    if st.session_state.get("pass_correct", "NONE") == "NONE":
        st.text_input(
            "Password", type="password", on_change=password_entered,
            key="password"
        )
    elif not st.session_state.get("pass_correct"):
        st.text_input(
            "Password", type="password", on_change=password_entered,
            key="password"
        )
        st.error("Password incorrect")
        return False
    else:
        return True


def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())


def upload_video():

    image_data = st.file_uploader("Upload file", ['png', 'jpeg', 'jpg'], key='uploading')

    # func to save BytesIO on a drive

    if image_data:
        temp_file_to_save = f"./temp_file_1.{image_data.type.split('/')[1]}"
        # save uploaded video to disc
        write_bytesio_to_file(temp_file_to_save, image_data)
        ss['file_path'] = temp_file_to_save
def upload_video_plate():

    image_data = st.file_uploader("Upload file", ['png', 'jpeg', 'jpg'], key='uploading2')

    # func to save BytesIO on a drive

    if image_data:
        temp_file_to_save = f"./temp_file_2.{image_data.type.split('/')[1]}"
        # save uploaded video to disc
        write_bytesio_to_file(temp_file_to_save, image_data)
        ss['file_path2'] = temp_file_to_save
def process_video():
    video_path= ss.get('file_path')
    if ss.get('uploading'):
        if st.button('Process image', type='primary'):
            with st.spinner('Processing image'):
                ocr_recognition.upload_video(video_path)
def process_plate_only():
    video_path = ss.get('file_path2')
    if ss.get('uploading2'):
        if st.button('Process plate', type='primary'):
            with st.spinner('Processing plate'):
                ocr_recognition.recognize_plate_only(video_path)
