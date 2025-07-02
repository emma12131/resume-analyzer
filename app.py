import streamlit as st
import openai

st.set_page_config(page_title="이력서 적합도 분석기", layout="wide")

st.title("📋 이력서 & 모집요강 적합도 분석기")

api_key = st.text_input("🗝 OpenAI API 키를 입력하세요", type="password")

if api_key:
    client = openai.OpenAI(api_key=api_key)

    st.markdown("### 📝 Step 1: 모집요강 입력")
    job_description = st.text_area("모집요강 (지원자격, 우대사항 등)", height=200)

    st.markdown("### 📄 Step 2: 이력서 입력")
    resume_text = st.text_area("이력서 전체 내용", height=300)

    if st.button("🔍 분석하기"):
        with st.spinner("GPT가 분석 중입니다..."):

            prompt = f"""
너는 채용 담당자입니다.

다음은 모집요강입니다:
{job_description}

다음은 지원자의 이력서입니다:
{resume_text}

아래 5가지를 step-by-step으로 정리해줘:
1. 핵심 역량 요약
2. 주요 장점 3가지
3. 단점/보완점 2가지
4. 모집요강과 얼마나 일치하는지 분석
5. 전반적인 적합도 평가 (매우 적합 / 적합 / 애매함 / 부족함 등)
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6
                )
                answer = response.choices[0].message.content
                st.markdown("### ✅ 분석 결과")
                st.write(answer)
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
else:
    st.warning("API 키를 입력해야 GPT 분석이 작동합니다.")
