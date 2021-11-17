# Bissmillah
import streamlit as st
import os
from os import listdir
import wget
from PIL import Image
import io
import numpy as np
import cv2



def load_model():
    wpath = 'yolov5/weights/crowdhuman_yolov5m.pt'
    if not os.path.exists(wpath):
        st.write('path didnt exist, so creation ! ')
        #os.system("python pip uninstall opencv-python")
        os.system("python -m pip install numpy torch pandas Pillow opencv-python-headless PyYAML>=5.3.1 torchvision>=0.8.1 matplotlib seaborn>=0.11.0 easydict")
        with st.spinner('Downloading model weights for crowdhuman_yolov5m'):
            #os.system('wget -O yolov5/weights/crowdhuman_yolov5m.pt https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch/releases/download/v.2.0/crowdhuman_yolov5m.pt')
            os.system('wget -nc https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch/releases/download/v.2.0/crowdhuman_yolov5m.pt -O yolov5/weights/crowdhuman_yolov5m.pt')
            #st.write('in function load_model', os.listdir('yolov5/weights/'))

    else:
        st.write('path alredy exist, so no creation ! ')
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
 
    args = { 'HirakAlger' : '112vHirakAlger_09042021_s.mp4' }
    vid_upload  = st.file_uploader(label= 'Upload Video', type = ['mp4', 'avi'])

    vid_open = "data/"+args['HirakAlger'] if vid_upload is None else vid_upload
    vname = args['HirakAlger'] if vid_upload is None else vid_upload.name
  
    video = load_output_video(vid_open)
    
                
    st.video(video) 
    
    st.write('in function : vname  = ', vname)
    st.write('in function ', os.listdir('data/'))
    st.write('in function ', os.listdir('yolov5/weights/'))
    
    vidcap = cv2.VideoCapture( "data/"+vname) 
    #frames = cv.get_frames("data/"+vname)
    success, frame0 = vidcap.read()
    st.write('shape of frame 01 : ', frame0.shape)

    return vname, frame0

@st.cache(allow_output_mutation=True)
def prediction(vname):
    
    vpath='data/'+vname
    wpath = 'yolov5/weights/crowdhuman_yolov5m.pt'
    if os.path.exists(wpath):
        
        os.system("python track.py --yolo_weights yolov5/weights/crowdhuman_yolov5m.pt --img 352 --save-vid --save-txt --classes 1 --conf-thres 0.4 --source " + vpath)
        os.system("ffmpeg -i inference/output/"+vname + " -vcodec libx264 -y inference/output/output_video.mp4")
        path = 'inference/output/output_video.mp4'
        if os.path.exists(path):
            video_file = open(path, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)

def main():
    vname, frame0 = starter()
    filepath = '.'  # Initialisation 
    if st.button('Heads detection!'):
        prediction(vname)
        st.success("Click again to retry or try a different video by uploading")
       
        filepath = 'inference/output/'+vname
        filepath = filepath[:-3]+'txt'
        st.write('filepath : ',filepath)
    st.write(os.listdir('inference/output/'))
    if st.button('Display Heads!'):
        filepath = 'inference/output/'+vname
        filepath = filepath[:-3]+'txt'
        st.write('filepath : ',filepath)
        nbperson, listhead = extract_heads(filepath, frame0) 
        display_heads(nbperson, listhead)
    
    return
      
def extract_heads(filepath, frame0):
    nbperson = 0
    listhead = []
    if os.path.exists(filepath):
        st.write("filepath : ", filepath)
        array_from_file = np.loadtxt(filepath, dtype=int)
        st.write('np of array load : ', array_from_file.shape)
        array_from_file = np.delete(array_from_file,np.s_[7:10], axis=1)
        nbperson = np.unique(array_from_file[:,1]).shape[0]

        rows = 5
        cols = 10
        nbheads = rows*cols
        frame = frame0
        cont = array_from_file
        for a in range(nbheads):
            numh = a
            head = frame[cont[numh][3]:cont[numh][3]+cont[numh][5],cont[numh][2]:cont[numh][2]+cont[numh][4],:]
            listhead.append(head)
        st.write('Len of liste heads : ', len(listhead))
    return nbperson, listhead

def display_heads(nbperson, listhead):
    os.system("streamlit run https://gist.githubusercontent.com/treuille/da70b4888f8b706fca7afc765751cd85/raw/0727bb67defd93774dae65a2bc6917f72e267460/image_paginator.py")
    image_iterator = paginator("Select a sunset page", listhead)
    indices_on_page, images_on_page = map(list, zip(*image_iterator))
    st.image(images_on_page, width=100, caption=indices_on_page)
    return    
    
if __name__ == '__main__':
    load_model()
    st.write("bismillah")
    print("bismillah")
    main() 
    
    st.write('out function ', os.listdir('data/'))
    st.write('out function ', os.listdir('yolov5/weights/'))

