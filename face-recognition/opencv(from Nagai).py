import datetime
import shutil
import glob
import cv2
import os

def main():
    f_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
    cap = cv2.VideoCapture(0)
    isSave = False
    dt_limit = datetime.datetime.now()
    stack_folder = 'stack'
    save_folder = 'img'
    if os.path.exists(stack_folder):
        shutil.rmtree(stack_folder)
    os.makedirs(stack_folder, exist_ok=True)
    if os.path.exists(save_folder):
        shutil.rmtree(save_folder)
    os.makedirs(save_folder, exist_ok=True)
    # buf_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    buf_time = datetime.datetime.now() + datetime.timedelta(seconds=2)
    while(datetime.datetime.now() < buf_time):
        ret, origin = cap.read()
        if ret:
            origin = origin[:, 200:80]
            dt_now = datetime.datetime.now()
            f_name = (dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f') + '.jpg')
            cv2.imwrite(os.path.join(stack_folder, f_name), origin)
    while(True):
        try:
            ret, origin = cap.read()
            if ret:
                origin = origin[:, 250:850]
                frame = origin[280:600, 300:450]
                facerect = f_cascade.detectMultiScale(frame, scaleFactor=1.2,
                                                      minNeighbors=1, minSize=(1, 1))
                for rect in facerect:
                    cv2.rectangle(frame, tuple(rect[0:2]),
                                  tuple(rect[0:2] + rect[2:4]),
                                  (255, 255, 255), thickness=2)
                cv2.imshow("Show FLAME Image", frame)
                if len(facerect) != 0:
                    if not isSave:
                        isSave = True
                        files = glob.glob(stack_folder + '/*.jpg')
                        for f in files:
                            shutil.copy(
                                f, os.path.join(save_folder, os.path.basename(f))
                            )
                    dt_limit = (
                        datetime.datetime.now() + datetime.timedelta(minutes=1)
                    )
                    print('detected')
                dt_now = datetime.datetime.now()
                f_name = (dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f') + '.jpg')
                cv2.imwrite(os.path.join(stack_folder, f_name), frame)
                rm_target_file = sorted(
                        glob.glob(os.path.join(stack_folder, '*.jpg'))
                )[0]
                os.remove(rm_target_file)
                if dt_limit > datetime.datetime.now():
                    cv2.imwrite(os.path.join(save_folder, f_name), frame)
                else:
                    isSave = False
                    # shutil.rmtree(stack_folder)
                    # os.mkdir(stack_folder)
                    # k = cv2.waitKey(1)
                if k == ord('q'):
                    break
        except Exception as e:
            print(str(e))
 
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()
