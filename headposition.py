import cv2
from math import atan
import imutils
import copy





def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y

def manInterp(r1, r2):
    a,b = r1
    c,d = r2
    return lambda x: mapFromTo(x, a,b,c,d)

def getFace(holder):
    webcam = cv2.VideoCapture(0)
    faceFinder = cv2.CascadeClassifier()
    faceFinder.load("models/facecascaade.xml")

    while True:
        _, frame = webcam.read()

        # Edit image to detect faces
        frame = cv2.resize(frame, None, fx=.2, fy=.2)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        # faces = faceFinder.detectMultiScale(frame_gray, minNeighbors=4)
        faces = faceFinder.detectMultiScale(frame_gray, minNeighbors=3)

        if len(faces) == 1:
            x, y, w, h = faces[0]
            yoff = frame.shape[0]//2 - (y + h) # use bottom as angle since it's stable
            xoff = x + w//2 - frame.shape[1]//2

            xangle = atan(xoff* 6/(frame.shape[1]*.3)  /12)
            xangle = xangle * 180 / 3.14

            yangle = atan(yoff / (frame.shape[0] * .3) / 12)
            yangle = yangle * 180 / 3.14 + 4

            fsize = w*h

            holder[0] = [xangle, yangle, fsize]






if __name__ == "__main__":
    cv2.namedWindow("webcam", cv2.WND_PROP_FULLSCREEN)
    cv2.namedWindow("model", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("webcam", cv2.WND_PROP_FULLSCREEN,
    #                       cv2.WINDOW_FULLSCREEN)

    # import video into a list
    allFrames = []
    # vid = cv2.VideoCapture('vids/octo.mp4')
    # vid = cv2.VideoCapture('vids/lamp.mp4')

    vid = cv2.VideoCapture('vids/facing1.mp4')
    # vid = cv2.VideoCapture('vids/sliding.mp4')

    while vid.isOpened():
        ret, frame = vid.read()
        allFrames.append(frame)
        if not ret:
            break

    allFrames = allFrames[::-1]

    smoothangle = 0
    faceFinder = cv2.CascadeClassifier()
    faceFinder.load("models/facecascaade.xml")
    webcam = cv2.VideoCapture(0)


    while True:
        _, frame = webcam.read()
        # bigframe = copy.deepcopy(frame)

        # Edit image to detect faces
        frame = cv2.resize(frame, None, fx=.2, fy=.2)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        faces = faceFinder.detectMultiScale(frame_gray, minNeighbors=4)

        if len(faces) == 1:
            x, y, w, h = faces[0]

            yoff = frame.shape[0]//2 - (y + h) # use bottom as angle since it's stable
            # yoff + 30
            xoff = x + w//2 - frame.shape[1]//2
            # print(xoff,yoff)

            xangle = atan(xoff* 6/(frame.shape[1]*.3)  /12)
            xangle = xangle * 180 / 3.14

            yangle = atan(yoff / (frame.shape[0] * .3) / 12)
            yangle = yangle * 180 / 3.14 + 4
            print(yangle, frame.shape)

            fsize = w*h



            smoothangle += (xangle-smoothangle)*.5
            chosen = (30 + smoothangle) * .015 * len(allFrames)
            chosen = max(min(chosen, len(allFrames)), 0)
            chosen = int(round(chosen))
            # chosen = max(min(chosen, allFrames),0)

            try:
                cv2.imshow('model', allFrames[chosen])

                # cv2.imshow('webcam', allFrames[int(round(chosen))])
                # frame = cv2.rectangle(bigframe, (x*5,y*5), ((x+w)*5, (y+h)*5),(255, 0, 0), 2)
                # frame = cv2.putText(frame, str(round(smoothangle,2)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, 200, 5)

                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                frame = cv2.putText(frame, str(round(smoothangle,2)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .6, 3, 2)
                cv2.imshow('webcam', frame)



            except Exception as e:
                print(e)


            # # Outline face
            # center = (x + w // 2, y + h // 2)
            # frame = cv2.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360,
            #                    (255, 0, 255), 4)
        # cv2.imshow('Capture - Face detection', frame)
        if cv2.waitKey(1) == 27:
            break  # esc to quit


