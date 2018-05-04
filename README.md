# HMM

개발 환경 및 실행 방법
version: python3.6
main file: main.py

> python main.py

파일 구성
- main.py: 메인 실행파일. train(), tag() 함수를 호출
- preprocess.py: train.txt, result.txt를 읽고 파싱하는 함수를 포함
- model.py: HMM class와 Markov chain을 구성하는 Node class 포함

프로그램 순서도
1. train.txt 를 읽어 단어들의 등장 횟수를 카운트 한다.
2. HMM 클래스 내에서 단어 빈도수를 기반으로 observation, transition 확률을 계산한다.
3. result.txt 를 읽어 형태소 분석 결과를 가져온다.
4. forward 알고리즘으로 전체 markov chain의 status 확률을 계산한다.
이 때 다음 노드로 가는 transition 확률 중 가장 큰 값을 저장한다.
또한 smoothing 기법으로 train에서 관측되지 않은 bigram 확률에 대해서는 전체 확률의
최소값의 log scale -1 의 확률을 부여한다.
5. backward 알고리즘으로 이전 단계의 max 값을 찾아 최대 확률을 내는 tag sequence를 구한다.
6. 각 문장의 tagging 결과를 output.txt에 저장한다.


