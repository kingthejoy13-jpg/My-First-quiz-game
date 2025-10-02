import streamlit as st
import random
import time

st.set_page_config(page_title="⚡ AI 퀴즈 게임 ⚡", page_icon="🎯")

st.title("⚡ AI시대 중딩 퀴즈 게임 ⚡")
st.write("룰: 제한 시간 안에 문제를 풀고, 레벨업하며 가상 코인을 획득하세요! 🪙")
st.write("코인 3개로 '시간 +2초' 아이템 사용 가능!")

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'question' not in st.session_state:
    st.session_state.question = None
if 'answer' not in st.session_state:
    st.session_state.answer = None
if 'coins' not in st.session_state:
    st.session_state.coins = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'extra_time' not in st.session_state:
    st.session_state.extra_time = 0

# 레벨별 배경색
level_colors = {1: "#E0F7FA", 2: "#FFF3E0", 3: "#E8F5E9", 4: "#F3E5F5", 5: "#FFEBEE"}
bg_color = level_colors.get(st.session_state.level, "#FFFFFF")
st.markdown(f"<div style='background-color:{bg_color}; padding:10px'> </div>", unsafe_allow_html=True)

# 새로운 문제 생성 함수
def new_question():
    level = st.session_state.level
    a = random.randint(1, level*10)
    b = random.randint(1, level*10)
    op = random.choice(["+", "-", "*"])
    if op == "+":
        ans = a + b
    elif op == "-":
        ans = a - b
    else:
        ans = a * b
    st.session_state.question = f"{a} {op} {b} = ?"
    st.session_state.answer = ans
    st.session_state.start_time = time.time()
    st.session_state.extra_time = 0  # 아이템 초기화

# 초기 문제
if st.session_state.question is None:
    new_question()

# 게임 UI
st.subheader(f"레벨: {st.session_state.level} | 점수: {st.session_state.score} | 코인: 🪙 {st.session_state.coins}")
st.write("문제:", st.session_state.question)

# 아이템 사용
if st.session_state.coins >= 3:
    if st.button("⏱️ 시간 +2초 사용 (3코인)"):
        st.session_state.extra_time += 2
        st.session_state.coins -= 3
        st.success("시간 +2초 아이템 사용!")

user_input = st.text_input("정답 입력", key="user_input")

if st.button("제출"):
    try:
        user_answer = int(user_input)
        elapsed = time.time() - st.session_state.start_time

        # 시간 제한: 5초 + 아이템 시간
        time_limit = 5 + st.session_state.extra_time

        # 정답 판정
        if user_answer == st.session_state.answer:
            bonus = 5 if elapsed <= 3 else 0
            st.session_state.score += 10 + bonus
            st.session_state.coins += 1
            if bonus > 0:
                st.success(f"⚡ 번개 속도! +5점 보너스!")
            else:
                st.success("정답!")
            # 레벨업 조건
            if st.session_state.score >= st.session_state.level * 30:
                st.session_state.level += 1
                st.balloons()
                st.success(f"🎉 레벨 {st.session_state.level} 달성! 배경색이 바뀌고 보너스 아이템 획득!")
            new_question()
        else:
            st.error(f"땡! 정답은 {st.session_state.answer}")
            st.warning(f"게임 종료! 최종 점수: {st.session_state.score}, 코인: 🪙 {st.session_state.coins}")
            # 초기화
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.coins = 0
            new_question()

        # 시간 초과
        if elapsed > time_limit:
            st.error(f"⏰ 시간 초과! 정답은 {st.session_state.answer}")
            st.warning(f"게임 종료! 최종 점수: {st.session_state.score}, 코인: 🪙 {st.session_state.coins}")
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.coins = 0
            new_question()
    except:
        st.warning("숫자만 입력하세요!")
