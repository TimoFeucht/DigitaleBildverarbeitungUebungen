import PythonServer_Comms_TCP as TCP
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import PythonLaneLines_student

sock = TCP.TcpComms(tcpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

# Parameters for TCP communication handling
i = 0
frame_number = 0

t1 = time.time()
img_list = []
use_file_output = False         # save every received frame as image file
use_cv_output = True            # convert every received frame as OpenCV image

# Parameters for lane detection
...

while True:
    # increment running var
    i += 1
    
    # read data
    data = sock.ReadReceivedData()    

    # if data is received
    if data != None:            
        # first chunk will include length of received data
        if len(img_list) == 0 and recv_int < 0:
            # first four bytes is length stored as int; but information is stored only in first 2 bytes [0:2]
            recv_int = int.from_bytes(data[0:2], byteorder='little')
            print('Received via int ' + str(recv_int))
            #data = data[4:] # real data starts after byte 4

        if data != None and len(data) > 0:              
            img_list.append(data)                        
            # JPEG starts with ffd8 and ends with ffd9
            t2 = time.time() # get time necessary for receiving
            # convert list of bytes to a joined byte array
            img = b''.join(img_list) # create image from img_list-chunks            
            
            print("Received Length: "  + str(len(img)) + " in " + str((t2-t1) * 1000) + " ms.") 
            print("Last bytes: " + str(img[-10:]))            
            t1 = time.time()

            # initialize coeff for polynomials
            p2 = 0.
            p1 = 0.
            p0 = 0.

            if use_file_output:
                outfile = open('img' + str(frame_number) + '.jpg', 'wb')
                outfile.write(img)
                outfile.close()
            
            # here image is prepared for further processing
            if use_cv_output:
                nparr = np.frombuffer(img, np.byte)                
                img_decoded = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
                if img_decoded is not None:                                        
                    # now work with this frame
                    # analyze image for lane lines
                    # --> TODO: implement your code here
                    result_img, left_line, right_line, radius, ... = PythonLaneLines_student.find_lines(img_decoded, ...)    
                                        
                    p2 = # polynomial for x^2
                    p1 = # polynomial for x^1
                    p0 = # polynomial 
                    
                    #print('Mean Polyn.: ' + str(p2) + ' *x^2 + ' + str(p1) + ' *x + ' + str(p0))                    

                    caption = 'result'
                    
                    cv2.imshow(caption, result_img)                                        
                    cv2.waitKey(1)  

                    # send acknowledgement
                    sock.SendData(str(len(img)) + ';' + str(p0) + ';' + str(p1) + ';' + str(p2) + ';' + str(radius) + ';' + str(pos))

                else:
                    print("Skip frame " + str(i) + " since it was not transferred correctly")                    
                    
                    # send acknowledgement
                    sock.SendData(str(-1) + ';' + str(-1) + ';' + str(-1) + ';' + str(-1) + ';' + str(-1) + ';' + str(-1))

        else:                 
            print("No data received.")
            # send acknowledgement
            sock.SendData(str(-1) + ';' + str(-1) + ';' + str(-1) + ';' + str(-1) + ';' + str(-1) + ';' + str(-1))                                   

        # prepare next frame
        frame_number += 1
        img_list = []    
        recv_int = -1   
    