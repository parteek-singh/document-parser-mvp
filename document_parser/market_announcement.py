# market_announcement.py
from typing import List, Optional
from pydantic import BaseModel
import re


class MarketAnnouncement(BaseModel):
    company_name: Optional[str] = None
    ticker: Optional[str] = None
    announcement_title: Optional[str] = None
    announcement_type: Optional[str] = None  # e.g. CAPITAL_RAISING, GUIDANCE, M&A, DIVIDEND
    announcement_datetime: Optional[str] = None
    summary: Optional[str] = None
    key_numbers: List[str] = []   # flexible list of human-readable key facts


def guess_ticker(text: str) -> Optional[str]:
    """
    Very naive ticker guess.
    Replace later with proper metadata or mapping.
    """
    # Look for patterns like "ASX: BHP" or "(ASX: BHP)"
    m = re.search(r"ASX:\s*([A-Z]{3,4})", text)
    if m:
        return m.group(1)

    # Fallback: any standalone 3–4 letter uppercase token
    tokens = re.findall(r"\b[A-Z]{3,4}\b", text)
    if tokens:
        return tokens[0]

    return None


def classify_announcement_type(text: str) -> Optional[str]:
    """
    Basic keyword-based classifier for announcement type.
    """
    t = text.lower()

    if any(w in t for w in ["placement", "rights issue", "capital raising", "share purchase plan", "spp"]):
        return "CAPITAL_RAISING"

    if any(w in t for w in ["guidance", "trading update", "earnings outlook"]):
        return "GUIDANCE"

    if any(w in t for w in ["acquisition", "merger", "scheme of arrangement", "takeover", "divestment"]):
        return "M&A"

    if any(w in t for w in ["dividend", "distribution", "franked", "record date", "payment date"]):
        return "DIVIDEND"

    return "OTHER"


def simple_summary(text: str) -> str:
    """
    Super naive summary: first 2–3 sentences.
    Later you can replace with an LLM-based summariser.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(sentences[:3])


def extract_market_announcement(full_text: str, sections: list) -> MarketAnnouncement:
    """
    Template parser for market announcements.
    Uses full_text for classification & summary,
    and the first section heading as a possible title.
    """
    ticker = guess_ticker(full_text)
    announcement_type = classify_announcement_type(full_text)
    summary = simple_summary(full_text)

    # Use the first section heading as title if it looks reasonable
    title = None
    if sections:
        maybe_title = sections[0].get("heading", "").strip()
        if maybe_title and len(maybe_title) < 120:
            title = maybe_title

    return MarketAnnouncement(
        company_name=None,         # later: derive from metadata or header
        ticker=ticker,
        announcement_title=title,
        announcement_type=announcement_type,
        announcement_datetime=None,  # later: parse from header area
        summary=summary,
        key_numbers=[]
    )
