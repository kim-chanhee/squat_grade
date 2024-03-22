import cv2
import requests

# UID = 'chanhee'

# 웹캠에서 프레임을 캡처하여 서버로 전송하고 로컬에 저장하는 함수 정의
def capture_and_send_frame(webcam, save_path, server_url):
    time_num = 0  # 시간 카운터 초기화
    image_num = 0  # 이미지 번호 초기화
    
    # 웹캠이 열려있는 동안 반복
    while webcam.isOpened():
        status, frame = webcam.read()  # 웹캠에서 프레임 읽기
        time_num += 1  # 시간 카운터 증가
        if not status:  # 프레임 읽기 실패 시 반복 중단
            break

        cv2.imshow("Webcam", frame)  # 읽은 프레임을 화면에 표시
        
        # 설정한 시간(여기서는 30 프레임)마다 이미지 파일로 저장
        if time_num == 30:
            image_num += 1  # 이미지 번호 증가
            filename = f"{save_path}img{image_num}.jpg"  # 저장할 파일 경로 및 이름 설정
            cv2.imwrite(filename, frame)  # 이미지 파일로 저장
            time_num = 0  # 시간 카운터 초기화

        _, img_encoded = cv2.imencode('.jpg', frame)  # 프레임을 JPEG 형식으로 인코딩
        img_bytes = img_encoded.tobytes()  # 인코딩된 데이터를 바이트 형태로 변환
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키를 누르면 반복 중단
            break
        
        # 서버로 인코딩된 이미지 데이터 전송
        try:
            response = requests.post(server_url, files={'image': img_bytes}, data={'UID': UID})
            print("Response:", response.text)  # 서버로부터 받은 응답 출력
        except Exception as e:
            print("Error sending frame to server:", e)  # 서버 전송 중 오류 발생 시 오류 메시지 출력
            
# 메인 실행 부분
if __name__ == "__main__":
    save_path = "/home/pi/camImage/"  # 이미지 저장 경로 설정
    server_url = "http://192.168.50.229:5052/upload"  # 서버 URL 설정
    
    webcam = cv2.VideoCapture(0)  # 웹캠 객체 생성
    
    # 웹캠이 정상적으로 열리지 않은 경우 오류 메시지 출력
    if not webcam.isOpened():
        print("Web cam is not running")
    else:
        capture_and_send_frame(webcam, save_path, server_url)  # 웹캠에서 프레임 캡처 및 전송 함수 호출
        
    webcam.release()  # 웹캠 자원 해제
    cv2.destroyAllWindows()  # 생성된 모든 창 닫기