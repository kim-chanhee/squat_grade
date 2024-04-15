# 스쿼트 자세 등급 판별       [squat_grade.pptx](https://github.com/kim-chanhee/squat_grade/files/14739038/squat_grade.pptx)
-----------------------------------------------------
- 주제 : 스쿼트 자세 교정을 통한 지속적인 운동 습관 유지
- 문제 상황 : 개인 지도를 받지 못한 사용자가 잘못된 자세로 스쿼트를 수행하여 부상 위험성 증가. 이에 따른 해결 방안 제시
- 해결방안 : 실시간 이미지 분석을 통하여 스쿼트 자세 등급 판별
------------------
* 작동 원리
  1. 고객 회원가입 및 로그인 -> 라즈베리 파이를 통한 웹캠 연동 실시간 영상 수집
  2. 프레임 단위 이미지 추출 후 자세 분석
     ![image](https://github.com/kim-chanhee/squat_grade/assets/116836230/01de59c6-9152-421e-84b9-c48ad6531731)
  3. 평가 등급 확인 (각 프레임별 이미지 등급분류 기준)
     ![image](https://github.com/kim-chanhee/squat_grade/assets/116836230/a4803c00-497c-4685-9fa7-72b017ebe0c1)

     ![image](https://github.com/kim-chanhee/squat_grade/assets/116836230/a92bcea3-17fd-4b4d-b88a-61c6b38025ac)

------------------
[전체 구조]
![image](https://github.com/kim-chanhee/squat_grade/assets/116836230/8ab72703-511c-477f-a602-4e64bc5b3922)






