from datetime import datetime
from cv2 import *
import os 
import numpy as np

video = VideoCapture(0)
val,frame = video.read()
last_frame = frame
threshold = 200000

record_buffer_max = 15
record_bufer = 0

fourcc = VideoWriter_fourcc(*'XVID')
numfiles = len(next(os.walk('output_files'))[2])
output = VideoWriter("output_files/"+str(numfiles)+".avi",fourcc,30,(int(video.get(3)),int(video.get(4))))

while True:
    now = datetime.now()
    val, frame = video.read()
    net_difference = 0.0

    gray_curr = cvtColor(frame, COLOR_BGR2GRAY)
    gray_last = cvtColor(last_frame, COLOR_BGR2GRAY)

    diff = subtract(gray_curr, gray_last)
    print("size diff ", diff )
    print("diff\n", diff)
    w = np.size(diff, 0)
    h = np.size(diff, 1)

    for i in range(0,w):
        for j in range(0, h):
            if i%5 == 0 & j%5 == 0:
                #r = diff[i,j]
                #g = diff[i,j]
                #b = diff[i,j]
                x = diff[i, j]

                net_difference += x #(r+g+b)
    
    imshow("Movement", diff)

    if net_difference > threshold:
        record_bufer = record_buffer_max

    putText(frame, now.strftime("%d/%m/%Y %H:%M:%S"), (int(video.get(3)) - 250, int(video.get(4) - 50)), FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255),2)

    if record_bufer<0:
        putText(frame, 'Not moving',(20,20), FONT_HERSHEY_COMPLEX, 0.6, (0,255,0),2)
    else:
        output.write(frame)
        putText(frame, 'Moving',(20,20), FONT_HERSHEY_COMPLEX, 0.6, (0,0,255),2)
        
    
    record_bufer -= 1
    if record_bufer < -100:
        record_bufer = 100

    imshow("Live", frame)
    last_frame = frame

    if waitKey(1) & 0xFF == ord('q'):
        break

video.release()
output.release()
destroyAllWindows()

    

