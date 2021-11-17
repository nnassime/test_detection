# Bissmillah
import streamlit as st
import os
from os import listdir
import wget
from PIL import Image
import io
import numpy as np

def load_model():
    wpath = 'yolov5/weights/crowdhuman_yolov5m.pt'
    if not os.path.exists(wpath):
        st.writ('path didnt exist, so creation ! ')
        with st.spinner('Downloading model weights for rowdhuman_yolov5m'):
            #os.system('wget -O /app/test/yolov5/weights/crowdhuman_yolov5m.pt https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch/releases/download/v.2.0/crowdhuman_yolov5m.pt')
            os.system('wget -nc https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch/releases/download/v.2.0/crowdhuman_yolov5m.pt -O /app/test/yolov5/weights/crowdhuman_yolov5m.pt')
    else:
        st.writ('path alredy exist, so no creation ! ')
        print("Model is here.")
        
        
# Ft saving uploaded video to directory
def save_uploaded_vid(uploadedfile):
    with open(os.path.join("data", uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Video saved in data dir ")

#@st.cache(ttl=3600, max_entries=10)
def load_output_video(vid):
    if isinstance(vid, str): 
        video = open(vid, 'rb')
    else: 
        video = vid.read()
        vname = vid.name
        save_uploaded_vid(vid)
    return video

def starter():
    st.image('data/LOGOGlob.png', width = 400)
    st.title("Test of Person detection")
    st.text("")
    st.text("")
    st.success("Welcome! Please upload a video!")
 
    args = { 'HirakAlger' : 'data/112vHirakAlger_09042021_s.mp4' }
    vid_upload  = st.file_uploader(label= 'Upload Video', type = ['mp4', 'avi'])

    vid_open = args['HirakAlger'] if vid_upload is None else vid_upload
    vname = args['HirakAlger'] if vid_upload is None else vid_upload.name
    vpath = "/app/test/"+vname if vid_upload is None else "/app/test/data/"+vname
    #vpath = "/app/test/data/"+vname
    
    video = load_output_video(vid_open)
    
    load_model()
                
    st.video(video) 
    
    st.write(vname)
    st.write(vpath)
    st.write('in function ', os.listdir('data/'))
    st.write('in function ', os.listdir('yolov5/weights/'))

    return vname

def main():
    vname = starter()
    return
      
    
if __name__ == '__main__':
    st.write("bismillah")
    print("bismillah")
    main()
    
    st.write('out function ', os.listdir('data/'))
    st.write('out function ', os.listdir('yolov5/weights/'))

