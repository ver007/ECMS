# ECMS
通过environment.yml文件快速安装虚拟环境,其中dlib和pytorch可以选择手动安装,已经上传到网盘;  
在deepface下创建face_database目录;  
在face_database下创建class1,class2,......,classn,具体取决于要管理几个班级或任何想管辖的区域;  
在每个classi下创建img文件夹和faces.csv文件;  
将model_store放在deepface目录下;  
保证参与考勤的人员信息(包括面部特征)已经被录入到系统中;  
在templates/check/faceRecognition.html中,将获取的设备自行切换成能揽盖全局的摄像头,即可实现多人的人脸识别考勤;  
模型太大,传不上去,请自行下载:  
链接: https://pan.baidu.com/s/1VWRaTW-lDfDNGbMhvl0_-Q   
提取码: 44kq 