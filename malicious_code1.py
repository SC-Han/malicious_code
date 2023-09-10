import os
import hashlib
import pyodbc
from tkinter import *

#tk객체 생성
Search = Tk()
Search.title("악성코드 찾기 프로그램")
Search.geometry("900x600")

#label 생성
label = Label(Search,text='악성코드 찾을려면 아래 버튼을 눌러주세요.')
#label을 화면에 배치
label.pack()

def calculate_sha256(file_path):
    # SHA-256 해시 객체를 생성합니다.
    sha256_hash = hashlib.sha256()
    try:
        # file 을 binary mode로 open
        with open(file_path, "rb") as f:    #파일을 4096 byte씩 읽어와서 해시를 값을 염
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()  #해시값을 16진수 형태를 반환합니다.

    except FileNotFoundError as notfound:
        print(f"파일을 찾을 수 없습니다: {file_path}, {notfound}")

    except PermissionError as notPermission:
        print(f"파일을 읽을 권한이 없습니다.: {file_path}, {notPermission}")

    except Exception as error:
        print(f"파일 열기 오류: {file_path}, {error}")

    return None

# 악성코드 검색 버튼 함수
def find_malicious_code():
    malicious_files = []
    file_count = 0

    # MSSQL 서버 연결 정보 설정
    server = '서버이름 적으세용'
    database = 'MaliciousCode'
    username = '유저이름 수정'
    password = '패스워드 수정'

    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conn.cursor()

        # 쿼리 실행
        cursor.execute('SELECT HashValue256 FROM MaliciousCode')

        # 쿼리 결과를 malicious_sha256_hashes 리스트에 추가
        malicious_sha256_hashes = [row[0] for row in cursor.fetchall()]

    except pyodbc.Error as e:
        print(f"MSSQL 서버 연결 오류: {e}")
        exit(1)

    # 최상위 디렉토리와 검사하고 싶은 확장자 목록을 지정합니다.

    root_directory = 'C:\\'  # 검색할 디렉토리를 변경하세요.
   
    extensions = ['.txt', '.docx', '.pdf']  # 검사하고 싶은 파일 확장자를 추가하세요.

    # root_directory에서 하위 디렉토리까지 탐색
    for root, dirs, files in os.walk(root_directory):
        print("현재 : 디렉토리 ", root)

        #window로 시작하는 디렉토리는 무시
        if os.path.join('Windows') in root:   
            continue

        for file in files:    #파일확인
            #파일 확장자가 지정된 확장자로 끝나는지 확인
            if any(file.endswith(ext) for ext in extensions):
                #파일 전체 경로를 생성
                file_path = os.path.join(root, file)

                # 파일의 SHA-256 해시값 계산
                sha256_hash = calculate_sha256(file_path)

                #만약 해시값이 존재하고 악성 해시 목록이 있다면 해시 값을 리스트에 추가
                if sha256_hash and sha256_hash in malicious_sha256_hashes:
                    malicious_files.append(file_path)

                    file_count+=1

    if malicious_files:
        print("악성 코드가 발견된 파일:")
        for file_path in malicious_files:
            print(file_path)
    else:
        print("악성 코드가 발견되지 않았습니다.")

    # DB 연결 종료
    conn.close()

# 악성코드 검색 버튼
Search_button = Button(Search,width=10, text="악성 코드 검색",overrelief="solid",command=find_malicious_code)
Search_button.pack()

Search.mainloop()