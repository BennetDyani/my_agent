import os
import re
from pathlib import Path
import io

import pandas as pd
import streamlit as st

# Optional LLM imports (try Google Gemini wrapper, then OpenAI)
try:
	from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
	ChatGoogleGenerativeAI = None
try:
	import openai
except Exception:
	openai = None


DATA_PATH = Path(__file__).parents[1] / "blood_analysis.txt"


def parse_blood_report(text: str) -> pd.DataFrame:
	rows = []
	for line in text.splitlines():
		line = line.strip()
		if not line or line.startswith("-") or line.endswith(":"):
			continue
		if ":" not in line:
			continue
		left, right = line.split(":", 1)
		test = left.strip()
		# split off normal range in parentheses
		normal = ""
		m = re.search(r"\(.*?Normal:([^\)]*)\)", right)
		if m:
			normal = m.group(1).strip()
			value_part = right[: m.start()].strip()
		else:
			# also handle cases like "(Normal: <200)" or no parenthesis
			value_part = re.sub(r"\(.*\)", "", right).strip()

		# extract first numeric value
		num_m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", value_part)
		numeric = float(num_m.group(0)) if num_m else None
		# units = rest after the numeric
		units = ""
		if num_m:
			units = value_part[num_m.end():].strip()

		rows.append({
			"Test": test,
			"ValueRaw": value_part,
			"NumericValue": numeric,
			"Units": units,
			"Normal": normal,
		})

	df = pd.DataFrame(rows)
	return df


def interpret_flag(value, normal_text):
	if value is None or not normal_text:
		return ""
	normal_text = normal_text.replace("\u2013", "-")
	try:
		if "<" in normal_text:
			thr = float(re.search(r"<\s*([0-9.]+)", normal_text).group(1))
			return "High" if value >= thr else "Normal"
		if ">" in normal_text:
			thr = float(re.search(r">\s*([0-9.]+)", normal_text).group(1))
			return "Low" if value <= thr else "Normal"
		if "-" in normal_text:
			a, b = re.split(r"-", normal_text)
			low = float(re.findall(r"[0-9.]+", a)[0])
			high = float(re.findall(r"[0-9.]+", b)[0])
			if value < low:
				return "Low"
			if value > high:
				return "High"
			return "Normal"
	except Exception:
		return ""
	return ""


def load_default_report() -> str:
	if DATA_PATH.exists():
		return DATA_PATH.read_text(encoding="utf-8")
	return ""


def call_llm(prompt: str, provider: str = "auto", model: str | None = None) -> str:
	"""Call an available LLM provider and return text response.

	provider: 'google', 'openai', or 'auto'
	"""
	# Prefer explicit providers
	if provider == "google" or (provider == "auto" and ChatGoogleGenerativeAI is not None):
		if ChatGoogleGenerativeAI is None:
			return "Google LLM client not available in this environment."
		model_name = model or "gemini-2.5-flash"
		try:
			llm = ChatGoogleGenerativeAI(model=model_name)
			resp = llm.invoke(prompt)
			return getattr(resp, "text", str(resp))
		except Exception as e:
			return f"Google LLM call failed: {e}"

	if provider == "openai" or (provider == "auto" and openai is not None):
		if openai is None:
			return "OpenAI client not available in this environment."
		key = os.environ.get("OPENAI_API_KEY")
		if not key:
			return "OPENAI_API_KEY not set in environment."
		try:
			openai.api_key = key
			model_name = model or "gpt-4o-mini"
			resp = openai.ChatCompletion.create(
				model=model_name,
				messages=[{"role": "user", "content": prompt}],
				max_tokens=800,
			)
			return resp["choices"][0]["message"]["content"]
		except Exception as e:
			return f"OpenAI call failed: {e}"

	return "No supported LLM provider is available. Set `OPENAI_API_KEY` or install `langchain_google_genai`."


def main():
	st.set_page_config(page_title="Blood Health Analysis", layout="centered")
	st.title("Blood Health Analysis")

	st.markdown("Simple Streamlit viewer for `blood_analysis.txt`.")

	uploaded = st.file_uploader("Upload a blood analysis text file", type=["txt"], help="Upload a report similar to the sample")
	if uploaded is not None:
		text = uploaded.getvalue().decode("utf-8")
	else:
		text = load_default_report()

	if not text:
		st.warning("No report available. Upload a `txt` file or add `blood_analysis.txt` next to this app.")
		return

	st.sidebar.header("Report Preview")
	if st.sidebar.checkbox("Show raw report", value=False):
		st.sidebar.code(text)

	df = parse_blood_report(text)
	df["Flag"] = df.apply(lambda r: interpret_flag(r.NumericValue, r.Normal), axis=1)

	st.subheader("Summary Table")
	st.dataframe(df[ ["Test","ValueRaw","Units","Normal","NumericValue","Flag"] ], height=320)

	numeric_df = df.dropna(subset=["NumericValue"]).set_index("Test")
	if not numeric_df.empty:
		st.subheader("Values Chart")
		st.bar_chart(numeric_df["NumericValue"])

		high = df[df.Flag == "High"]
		low = df[df.Flag == "Low"]
		cols = st.columns(2)
		cols[0].metric("High flags", len(high))
		cols[1].metric("Low flags", len(low))

	# LLM assistant UI
	st.subheader("LLM Assistant")
	st.sidebar.header("LLM Settings")
	provider = st.sidebar.selectbox("LLM Provider", options=["auto", "google", "openai"], index=0)
	model = st.sidebar.text_input("Model (optional)", value="")
	include_raw = st.checkbox("Include raw report in prompt", value=False)
	include_parsed = st.checkbox("Include parsed values (CSV) in prompt", value=False)

	if "llm_prompt" not in st.session_state:
		st.session_state.llm_prompt = "Write a short 3-line health summary and a concise diet plan based on the blood report."

	# sample prompt buttons
	sp1, sp2, sp3 = st.columns(3)
	with sp1:
		if st.button("Summary"):
			st.session_state.llm_prompt = "Write a concise health summary (3 lines) based on the report."
	with sp2:
		if st.button("Extract Values"):
			st.session_state.llm_prompt = "Extract all test names and numeric values from the report and classify each as HIGH/LOW/NORMAL. Output as a CSV list with columns Test,Value,Flag."
	with sp3:
		if st.button("Diet Plan"):
			st.session_state.llm_prompt = "Based on the blood analysis, provide a short South-African-friendly diet plan: Foods to avoid; Foods to eat more often. Keep concise."

	prompt = st.text_area("Prompt to LLM", value=st.session_state.llm_prompt, height=160)

	if st.button("Send to LLM"):
		full_prompt = prompt
		if include_raw:
			full_prompt = f"Report:\n{text}\n\n" + full_prompt
		if include_parsed:
			full_prompt = f"Parsed values (CSV):\n{df.to_csv(index=False)}\n\n" + full_prompt

		with st.spinner("Calling LLM..."):
			resp_text = call_llm(full_prompt, provider=provider, model=(model or None))

		st.success("LLM response received")
		with st.expander("LLM Response", expanded=True):
			st.code(resp_text)
		st.download_button("Download LLM response", data=resp_text.encode("utf-8"), file_name="llm_response.txt", mime="text/plain")

	# CSV download for parsed data
	csv = df.to_csv(index=False).encode("utf-8")
	st.download_button("Download parsed CSV", data=csv, file_name="blood_analysis_parsed.csv", mime="text/csv")


if __name__ == "__main__":
	main()
