import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

def random_forest(data, label):
    # K-fold
    study_train, data_test, study_label, label_test = train_test_split(data, label, random_state=5000, test_size=0.2, train_size=0.8, stratify=label)

    # Random Forest 모델 생성 및 학습 
    R_mode = RandomForestClassifier(n_jobs=-1, n_estimators=100)
    R_mode.fit(study_train, study_label)
    
    # 테스트 데이터에 대해 예측값을 생성합니다.
    predict = R_mode.predict(data_test)

    # 예측값과 실제 값(label_test)를 비교하여 정확도 점수를 계산합니다.
    malware_score = metrics.accuracy_score(label_test, predict)
    
    # 분류 보고서를 작성합니다. 이 보고서에는 각 클래스에 대한 precision(정밀도), recall(재현율), f1-score(F1 점수) 등의 정보가 포함됩니다.
    malware_report = metrics.classification_report(label_test, predict)
    
     # 혼동 행렬(confusion matrix)를 계산합니다. 혼동 행렬은 각 클래스가 어떻게 분류되었는지 나타내는 정보입니다.
    cf_matrix = metrics.confusion_matrix(label_test, predict)

    print("Accuracy Score:", malware_score)
    print("Classification Report:", malware_report)
    print("Confusion Matrix:", cf_matrix)

# CSV 파일 경로로 불러오기
tlsh_csv = pd.read_csv('tlsh_hash_data.csv')

# filename 컬럼 제거 
tlsh_csv = tlsh_csv.drop(columns=['filename'])

# 예측하려는 대상인 'label' 컬럼을 분리 (여기서는 'malware'가 예시입니다.)
label = tlsh_csv['malware']

# 나머지 데이터 
data = tlsh_csv.drop(columns=['malware'])

model = random_forest(data, label)  # 함수 호출하여 모델 학습시키기