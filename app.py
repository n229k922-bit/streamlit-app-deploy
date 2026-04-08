import csv
from datetime import date, datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="合宿参加意向調査", page_icon="🏕️")
st.title("🏕️ 合宿参加の意向調査フォーム")
st.write("以下の項目にご回答ください。")

CSV_PATH = Path("responses.csv")
FIELDS = [
    "timestamp",
    "name",
    "grade",
    "participation",
    "reason",
    "allergy",
    "emergency_contact",
    "response_date",
]


def append_response(record: dict) -> None:
    file_exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)


with st.form("camp_survey_form"):
    name = st.text_input("氏名 *")
    grade = st.selectbox("学年", ["1年", "2年", "3年", "4年", "その他"])
    participation = st.radio(
        "合宿への参加意向 *",
        ["参加する", "検討中", "参加しない"],
        horizontal=True,
    )
    reason = st.text_area("理由・補足（任意）")
    allergy = st.text_area("アレルギー・持病（任意）")
    emergency_contact = st.text_input("緊急連絡先（任意）")

    submitted = st.form_submit_button("送信")

if submitted:
    if not name.strip():
        st.error("必須項目（氏名）を入力してください。")
    else:
        response = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "name": name.strip(),
            "grade": grade,
            "participation": participation,
            "reason": reason.strip(),
            "allergy": allergy.strip(),
            "emergency_contact": emergency_contact.strip(),
            "response_date": str(date.today()),
        }

        append_response(response)

        st.success("回答を受け付けました。ありがとうございます！")
        st.write("### 入力内容確認")
        st.json(response)

st.divider()
st.caption("回答は `responses.csv` に保存されます。")
