"""
ai — generate a Linux command with Gemini and pre-type it in the shell (no execution).

Example
  ai "make me a command to go into /root"
"""

import os
import sys
import json
import subprocess
import readline
import textwrap
import requests

from dotenv import load_dotenv

from sysinfo import get_sysinfo
from dangcmds import is_dangerous

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_MODEL_TEMPERATURE = os.getenv("GEMINI_MODEL_TEMPERATURE", 0.2)
GEMINI_SYSTEM_PROMPT = os.getenv("GEMINI_SYSTEM_PROMPT", "")

INCLUDE_SYSINFO = os.getenv("INCLUDE_SYSINFO", "true").lower() == "true"

CACHE = os.getenv("CACHE", "false").lower() == "true"

ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key="
)

SYSTEM_PROMPT = textwrap.dedent(f"""
    {GEMINI_SYSTEM_PROMPT}
""").strip()

if INCLUDE_SYSINFO:
    SYSTEM_PROMPT += str(get_sysinfo())


def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def get_command(description: str) -> str:
    if not GEMINI_API_KEY:
        fail("GEMINI_API_KEY not set")
    headers = {"Content-Type": "application/json"}
    payload = {
    "system_instruction": {
        "parts": [
            {"text": SYSTEM_PROMPT}
        ]
    },
    "contents": [
        {   # user message
            "role": "user",
            "parts": [
                {"text": description}
            ]
        }
    ],
    "generationConfig": {
        "temperature": GEMINI_MODEL_TEMPERATURE
    }
}
    r = requests.post(ENDPOINT + GEMINI_API_KEY, headers=headers, data=json.dumps(payload))
    if r.status_code != 200:
        fail(f"Gemini API error: {r.status_code} – {r.text}")
    try:
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError, TypeError) as e:
        fail(f"Unexpected response shape: {e}\nFull response:\n{r.text}")
    return text

def input_with_prefill(prompt: str, text: str) -> str:
    """Prefill the input with default command so user can edit inline"""
    if sys.stdin.isatty() and readline:
        def hook():
            readline.insert_text(text)
        readline.set_startup_hook(hook)
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook(None)

def main() -> None:
    if len(sys.argv) < 2:
        fail("Usage: ai \"your description here\"")

    command = get_command(" ".join(sys.argv[1:]).strip())
    try:
        cmd = input_with_prefill("> ", command).strip()
    except KeyboardInterrupt:
        print("\nAborted.")
        return

    is_dang, category = is_dangerous(cmd)
    if is_dang:
        print(f"⚠️ Warning: Command potentially dangerous. Reason : {category}")
        if input("Are you sure to execute ? [y/N] ").lower() not in ["y", "yes"]:
            print("Aborted.")
            return

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as err:
        print(err)
        sys.exit(err.returncode)


if __name__ == "__main__":
    main()
