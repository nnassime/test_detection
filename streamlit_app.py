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
        st.write('path didnt exist, so creation ! ')
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

    return vname

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
    vname = starter()
        
    if st.button('Heads detection!'):
        prediction(vname)
        st.success("Click again to retry or try a different video by uploading")
        vpath='data/'+vname
        filepath = 'inference/output/'+vpath
        filepath = filepath[:-3]+'txt'
        st.write(filepath)
    if st.button('Display Heads!'):
        extract_heads(filepath) 
    
    return
      
def extract_heads(filepath):
    nbperson = 0
    listhead = []
    if os.path.exists(filepath):
        array_from_file = np.loadtxt(filepath, dtype=int)
        array_from_file = np.delete(array_from_file,np.s_[7:10], axis=1)
        nbperson = np.unique(array[:,1]).shape[0]

        rows = 5
        cols = 10
        nbheads = rows*cols
        
        for a in range(nbheads):
            numh = a
            head = frame[cont[numh][3]:cont[numh][3]+cont[numh][5],cont[numh][2]:cont[numh][2]+cont[numh][4],:]
            listhead.append(head)
            st.write('Len of liste heads : ', len(listhead))
    return nbperson, listhead
    
    
if __name__ == '__main__':
    load_model()
    st.write("bismillah")
    print("bismillah")
    main() 
    
    st.write('out function ', os.listdir('data/'))
    st.write('out function ', os.listdir('yolov5/weights/'))

