import streamlit as st
import random
import pandas as pd

def create_seating_chart(students, rows, cols):
    # 학생 목록을 섞습니다
    random.shuffle(students)
    
    # 빈 자리를 포함한 전체 좌석 수를 계산합니다
    total_seats = rows * cols
    
    # 빈 자리를 추가합니다
    seats = students + [''] * (total_seats - len(students))
    
    # 2D 리스트로 변환합니다
    seating_chart = [seats[i:i+cols] for i in range(0, total_seats, cols)]
    
    return seating_chart

st.title('우리 반 자리 배치 앱')

# 사이드바에서 학생 이름 입력 받기
st.sidebar.header('학생 이름 입력')
students_input = st.sidebar.text_area('학생 이름을 줄바꿈으로 구분하여 입력하세요:')
students = [name.strip() for name in students_input.split('\n') if name.strip()]

# 교실 크기 설정
rows = st.sidebar.number_input('교실 행 수:', min_value=1, max_value=10, value=5)
cols = st.sidebar.number_input('교실 열 수:', min_value=1, max_value=10, value=6)

if st.sidebar.button('자리 배치하기'):
    if len(students) > rows * cols:
        st.error(f'학생 수({len(students)})가 좌석 수({rows * cols})보다 많습니다!')
    elif len(students) == 0:
        st.error('학생 이름을 입력해주세요!')
    else:
        seating_chart = create_seating_chart(students, rows, cols)
        
        # 데이터프레임으로 변환하여 표시
        df = pd.DataFrame(seating_chart)
        
        st.subheader('자리 배치 결과')
        st.dataframe(df.style.set_properties(**{'font-size': '20px', 'text-align': 'center'})
                     .set_table_styles([{'selector': 'th', 'props': [('font-size', '20px')]}]), 
                     height=(rows * 50))
        
        # 엑셀 파일로 다운로드 옵션
        st.download_button(
            label="엑셀 파일로 다운로드",
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name="자리배치.csv",
            mime="text/csv",
        )

st.sidebar.markdown('---')
st.sidebar.write('사용 방법:')
st.sidebar.write('1. 왼쪽 사이드바에 학생 이름을 입력하세요.')
st.sidebar.write('2. 교실의 행과 열 수를 설정하세요.')
st.sidebar.write('3. "자리 배치하기" 버튼을 클릭하세요.')
st.sidebar.write('4. 결과를 확인하고 필요하다면 엑셀 파일로 다운로드하세요.')