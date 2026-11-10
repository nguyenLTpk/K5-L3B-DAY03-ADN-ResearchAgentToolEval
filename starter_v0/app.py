from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import now_iso, run_model_tool_loop, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
TRANSCRIPTS_DIR = ROOT / "transcripts"
PROVIDERS = ("openrouter", "openai", "anthropic", "gemini", "ollama")

load_lab_env(ROOT)


def start_new_chat(config: tuple[str, str | None, str]) -> None:
    provider_name, model, version = config
    artifact_version = build_artifact_version(version, PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"ui_{provider_name}_{timestamp}"
    st.session_state.active_config = config
    st.session_state.chat_messages = []
    st.session_state.model_messages = []
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model,
        "system_prompt": str(PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": 5,
        "max_tool_rounds": 4,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def show_tool_events(events: list[dict[str, Any]]) -> None:
    if events:
        with st.expander("Chi tiết lời gọi tool"):
            st.json(events)


st.set_page_config(page_title="ADN Research Agent", page_icon="🔎", layout="centered")
st.title("ADN Research Agent")
st.caption("Tra cứu nguồn, đọc URL và định dạng trích dẫn. Phiên chat được lưu thành transcript cục bộ.")

with st.sidebar:
    st.header("Cấu hình")
    provider_name = st.selectbox("Provider", PROVIDERS, index=PROVIDERS.index("ollama"))
    default_model = "qwen2.5:1.5b" if provider_name == "ollama" else ""
    model_value = st.text_input("Model (để trống để dùng mặc định của provider)", value=default_model, key=f"model_{provider_name}")
    version_value = st.text_input("Nhãn version", value="v5")
    st.caption("API key được nạp từ starter_v0/.env hoặc DAY03_ENV_FILE; giá trị key không hiển thị trong UI.")
    new_chat_clicked = st.button("Bắt đầu phiên mới", use_container_width=True)

config = (
    provider_name,
    model_value.strip() or None,
    version_value.strip() or "v5",
)

if "active_config" not in st.session_state:
    start_new_chat(config)
elif new_chat_clicked:
    start_new_chat(config)
elif st.session_state.active_config != config and not st.session_state.chat_messages:
    start_new_chat(config)

config_changed = st.session_state.active_config != config
if config_changed:
    st.warning("Cấu hình đã đổi. Bấm Bắt đầu phiên mới để mở phiên với cấu hình này.")

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        show_tool_events(message.get("tool_events", []))

prompt = st.chat_input("Nhập yêu cầu nghiên cứu…", disabled=config_changed)

if prompt:
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    turn_index = len(st.session_state.transcript["turns"]) + 1
    turn: dict[str, Any] = {
        "turn_index": turn_index,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    try:
        system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
        declarations = load_tool_declarations(TOOLS_PATH)
        tools = to_openai_tools(declarations)
        provider = make_provider(provider_name)
        result = run_model_tool_loop(
            provider=provider,
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.model_messages[-10:],
                {"role": "user", "content": prompt},
            ],
            tools=tools,
            model=config[1],
            max_tool_rounds=4,
        )
        turn.update(result)
        assistant_text = result["assistant_text"] or "Agent chưa trả về nội dung."
        st.session_state.model_messages.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_text},
        ])
    except Exception as exc:
        turn.update({
            "status": "provider_error",
            "error": type(exc).__name__,
        })
        assistant_text = (
            f"Không gọi được provider ({type(exc).__name__}). "
            "Kiểm tra provider, API key và kết nối rồi thử lại."
        )

    turn["assistant_text"] = assistant_text
    turn["ended_at"] = now_iso()
    st.session_state.transcript["turns"].append(turn)
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": assistant_text,
        "tool_events": turn.get("tool_events", []),
    })
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)
    st.rerun()

if st.session_state.transcript["turns"]:
    st.caption(f"Transcript: {st.session_state.transcript_path}")
