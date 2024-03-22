import cv2
import requests

UID = 'chanhee'

def capture_and_send_frame(webcam, save_path,server_url):
    time_num = 0
    image_num = 0
    
    while webcam.isOpened():
        status,frame = webcam.read()
        time_num += 1
        if not status:
            break

        cv2.imshow("Webcam", frame)
        
        if time_num == 30:
            image_num += 1
            filename = f"{save_path}img{image_num}.jpg"
            cv2.imwrite(filename, frame)
            time_num =0

        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        try:
            response = requests.post(server_url, files={'image' : img_bytes}, data = {'UID' : UID})
            print("Response:", response.text)
        except Exception as e :
            print("Error sending frame to server:", e)
            
     

if __name__ == "__main__":
    save_path = "/home/pi/camImage/"
    server_url = "http://192.168.50.229:5052/upload"
    
    webcam = cv2.VideoCapture(0)
    
    if not webcam.isOpened():
        print("Web cam is not running")
    else:
        capture_and_send_frame(webcam, save_path, server_url)
        
    webcam.release()
    cv2.destroyAllWindows()