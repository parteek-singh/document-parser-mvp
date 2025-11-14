# # kpi_extractor.py
# from typing import List, Dict, Any, Optional
# from pydantic import BaseModel
# import json
# import os
# import openai  # or your preferred LLM client


# class KpiDefinition(BaseModel):
#     name: str
#     description: str
#     type: str = "number"   # "number", "string", etc.
#     unit: Optional[str] = None


# class KpiValue(BaseModel):
#     name: str
#     value: Any
#     unit: Optional[str] = None
#     confidence: Optional[float] = None
#     source_snippet: Optional[str] = None


# # Configure OpenAI client (set env var OPENAI_API_KEY)
# openai.api_key = os.getenv("OPENAI_API_KEY")


# def build_kpi_prompt(text: str, kpis: List[KpiDefinition]) -> str:
#     kpi_desc = "\n".join(
#         f"- {k.name} ({k.type}, unit={k.unit}): {k.description}"
#         for k in kpis
#     )

#     # Truncate text if needed to avoid massive prompts
#     max_chars = 15000
#     if len(text) > max_chars:
#         text = text[:max_chars]

#     prompt = f"""
# You are a precise information extraction assistant.

# Text:
# \"\"\"{text}\"\"\"

# We need to extract the following KPIs from this text:

# {kpi_desc}

# Return a JSON object with this exact structure:

# {{
#   "kpis": [
#     {{
#       "name": "<kpi_name>",
#       "value": <value or null>,
#       "unit": "<unit or null>",
#       "confidence": <0.0-1.0 or null>,
#       "source_snippet": "<short quote from the text or null>"
#     }}
#   ]
# }}

# If a KPI is not present, set value to null and confidence to 0.0.
# Do not add extra fields.
# """
#     return prompt


# def extract_kpis_with_llm(text: str, kpis: List[KpiDefinition]) -> List[KpiValue]:
#     """
#     Use an LLM to extract KPI values according to the provided KPI definitions.
#     """
#     if not openai.api_key:
#         raise RuntimeError("OPENAI_API_KEY environment variable is not set")

#     prompt = build_kpi_prompt(text, kpis)

#     # Example using ChatCompletion. Adjust model name to what you have access to.
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",  # or "gpt-4o", "gpt-4.1", etc.
#         messages=[
#             {"role": "system", "content": "You are a helpful data extraction assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.0
#     )

#     content = response.choices[0].message["content"]
#     data = json.loads(content)

#     values = [KpiValue(**item) for item in data.get("kpis", [])]
#     return values
