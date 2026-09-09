"""
Example: calling an LLM through the LiteLLM Proxy with structured outputs.

This goes through the LiteLLM Proxy (https://docs.litellm.ai/docs/simple_proxy)
rather than the litellm Python SDK's in-process routing: the proxy is a
standalone OpenAI-compatible server, so this script is just the OpenAI SDK
pointed at it. The proxy config decides which underlying provider/model each
`model` name maps to, so this code never imports `litellm` or picks a
provider itself.

Start a proxy locally (see `litellm_proxy_config.example.yaml` next to this
file) before running this script:
    litellm --config litellm_proxy_config.example.yaml --port 4000

Run from `backend/` (with the venv active):
    python -m examples.litellm_structured_output_example

Env vars:
    LITELLM_PROXY_BASE_URL   default http://localhost:4000
    LITELLM_PROXY_API_KEY    the proxy's master key or a virtual key
"""

import os

from openai import OpenAI
from pydantic import BaseModel


class ExtractedCustomer(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    notes: str


# Name of a `model_list` entry in the proxy config, not a provider model ID -
# the proxy maps this to whichever real provider/model it's configured for.
MODEL = "claude-opus-5"

SAMPLE_TEXT = (
    "Spoke with Priya Sharma today, she wants to update her contact email to "
    "priya.sharma@example.com and mentioned her phone number is 98765 43210. "
    "She's happy with the current plan, no other changes needed."
)

client = OpenAI(
    base_url=os.environ.get("LITELLM_PROXY_BASE_URL", "http://localhost:4000"),
    api_key=os.environ.get("LITELLM_PROXY_API_KEY", "sk-1234"),
)


def extract_customer(raw_text: str) -> ExtractedCustomer:
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the customer details from this note:\n\n"
                    f"{raw_text}"
                ),
            }
        ],
        response_format=ExtractedCustomer,
    )
    return response.choices[0].message.parsed


if __name__ == "__main__":
    customer = extract_customer(SAMPLE_TEXT)
    print(customer.model_dump_json(indent=2))
