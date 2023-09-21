import csv
import os
import tlsh

csvfile = 'tlsh_hash_data.csv'

with open(csvfile, 'w', newline='') as fp:
    writer = csv.writer(fp)

# 헤더 리스트 생성하고 "filename" 추가하기
header = list()
header.append("filename")

# 헤더에 "f1"부터 "f70"까지 추가하기
for i in range(1, 73):
    header.append("f"+str(i))

with open(csvfile, 'w',newline='')as fp:
    writer = csv.writer(fp)
# 헤더를 CSV 파일에 작성하기
    writer.writerow(header)
##-----------------------------------------------------------------------------------------------------------------------------------------------------
    # 상대 경로를 사용하는 경우:
    # files = os.listdir('testdir') 
    # 절대 경로를 사용하는 경우:
    # full_path = '/home/user/testdir'  # 실제 경로로 변경해야 합니다.
    # files = os.listdir(full_path)
    #  ------------------------------------------------------------------------------------------------------------------------------------------------------
    # 경로에서 파일 목록 가져오기 (경로는 실제 사용하는 경로로 바꿔주세요)
    path = r'C:\Users\yeop\Desktop\악성코드'
    files = os.listdir(path)

 # 각각의 파일에 대해서 반복 처리하기 
    for filename in files:
        datalist = list()
        datalist.append(filename)

        file_path = os.path.join(path,filename)

        with open (path + '/' + filename, mode='rb') as fp2:
            binary = fp2.read()  # 해당 파일을 바이너리 모드로 읽기

        tlsh_value = tlsh.hash(binary)  # TLSH 해시값 계산

        idx = 0

        while(idx < len(tlsh_value)):  # TLSH 값을 한 글자씩 처리하기 위한 반복문 
            str_tlsh = tlsh_value[idx:idx+1]  # TLSH 값을 한 글자씩 추출하여 문자열 형태로 변환 
            datalist.append(ord(str_tlsh))   # 해당 문자열의 ASCII 코드 값을 데이터 리스트에 추가 
            idx += 1

        writer.writerow(datalist)   # 완성된 데이터 리스트를 CSV 파일에 작성 
binary = None