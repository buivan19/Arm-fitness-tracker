import streamlit as st

class BicepCurlInstruction:
    
    name = "Bicep Curl"    
    description = "Bicep curl (cuốn tạ tay trước) là bài tập thể hình kinh điển, tập trung phát triển cơ tay trước (biceps), giúp cơ bắp khỏe mạnh, săn chắc và nổi rõ đường nét bằng cách gập khuỷu tay để nâng tạ lên ngang vai."
    setup = [
        "Đặt camera đối diện người tập",
        "Camera ngang tầm ngực",
        "Khoảng cách camera từ 2-4m",
        "Toàn bộ phần thân trên và tay phải năm trên khung hình",
        "Camera đặt cố định, không rung lắc, ánh sáng tốt"
    ]
    
    execution = [
        "Đứng thẳng, 2 tay trước ngực",
        "Khuỷu tay giữ cố định sát thân người.",
        "Tay duỗi đúng khoảng 160-170 độ",
        "Gập tay từ 160-170 độ xuống khoảng 30-40 độ.",
        "Không đung đưa người khi tập.",
        "Hạ tay xuống chậm và có kiểm soát."
    ]


class LateralRaiseInstruction:
    
    name = "Lateral Raise"
    description = "Lateral raise là bài tập thể hình chủ yếu nhắm vào cơ vai giữa, giúp vai rộng hơn, săn chắc và khỏe mạnh hơn"
    
    setup = [
        "Đặt camera đối diện người tập",
        "Camera ngang tầm vai",
        "Hai tay luôn nằm trong khung hình",
        "Tránh che khuất tay khi tập"
    ]
    
    execution = [
        "Đứng thẳng, hai tay thả lỏng bên hông",
        "Nâng hai tay từ từ sang ngang cho đến khi tay song song với mặt đất",
        "Giữ tay khoảng 1 giây rồi từ từ hạ tay xuống",
    ]


class OverheadPressInstruction:
    
    name = "Overhead Press"
    description = "Overhead Press là bài tập compound (phối hợp nhiều nhóm cơ) cốt lõi, giúp tăng sức mạnh thân trên bằng cách nâng vật nặng"
    setup = [
        "Đặt camera thẳng đối diện, phải ngang tầm ngực và vai",
        "Không đặt camera quá thấp hoặc quá cao",
        "Camera phải nhìn rõ được vai và tay"
    ]
    
    execution = [
        "Giữ tay hướng lên ngang vai",
        "Đẩy tay thẳng lên trên đầu",
        "Duỗi tay gần thẳng nhưng không khóa khớp",
        "Hạ tay xuống chậm và có kiểm soát."
    ]


INSTRUCTION_CLASSES = {
    "Bicep Curl": BicepCurlInstruction,
    "Lateral Raise": LateralRaiseInstruction,
    "Overhead Press": OverheadPressInstruction
}


def get_instruction_class(exercise_name):
    return INSTRUCTION_CLASSES.get(exercise_name)


def show_instructions(exercise_name):
    inst = get_instruction_class(exercise_name)
    
    if not inst:
        st.warning("Instructions not available for this exercise.")
        return
    
    st.markdown(f"### {inst.name} Instructions")
    st.info(inst.description)
    
    with st.expander("Hướng dẫn setup camera", expanded=True):
        for step in inst.setup:
            st.markdown(f"• {step}")
    
    with st.expander("Cách thực hiện", expanded=True):
        for i, step in enumerate(inst.execution, 1):
            st.markdown(f"{i}. {step}")