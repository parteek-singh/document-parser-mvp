# dividend_extractor.py
import re
from typing import Optional
from pydantic import BaseModel


class DividendInfo(BaseModel):
    entity_name: Optional[str] = None
    ticker: Optional[str] = None
    security_description: Optional[str] = None
    announcement_date: Optional[str] = None  # dd/mm/yyyy (as in ASX form)
    period_end_date: Optional[str] = None

    currency: Optional[str] = None           # primary currency (e.g. AUD, USD)
    amount_per_security: Optional[float] = None
    aud_equivalent_amount: Optional[float] = None  # for USD with AUD equivalent (BHP style)

    ex_date: Optional[str] = None
    record_date: Optional[str] = None
    payment_date: Optional[str] = None

    franking_percent: Optional[float] = None
    franked_amount_per_security: Optional[float] = None
    unfranked_amount_per_security: Optional[float] = None

    drp_available: Optional[bool] = None
    drp_status: Optional[str] = None
    drp_price: Optional[float] = None
    drp_price_currency: Optional[str] = None


def _find(pattern: str, text: str, flags=0) -> Optional[re.Match]:
    return re.search(pattern, text, flags)


def _find_value(pattern: str, text: str, flags=0) -> Optional[str]:
    m = _find(pattern, text, flags)
    return m.group(1).strip() if m else None


def _find_float(pattern: str, text: str, flags=0) -> Optional[float]:
    m = _find(pattern, text, flags)
    if not m:
        return None
    raw = m.group(1).replace(",", "").strip()
    try:
        return float(raw)
    except ValueError:
        return None


def extract_dividend_info(full_text: str) -> DividendInfo:
    """
    Extract structured dividend info from an ASX Appendix 3A.1 style document.
    Designed using AGL and BHP dividend examples.
    """

    text = full_text

    # --- Entity & security basics ---
    entity_name = _find_value(r"Entity name\s+(.+)", text)
    ticker = _find_value(r"1\.3 ASX issuer code\s+([A-Z0-9]{2,5})", text)
    security_description = _find_value(r"ASX \+Security Description\s+(.+)", text)

    announcement_date = _find_value(r"Date of this announcement\s+(\d{1,2}/\d{1,2}/\d{4})", text)

    # e.g. "2A.3 The dividend/distribution relates to the financial reporting or payment period ending ... 30/6/2024"
    period_end_date = _find_value(
        r"2A\.3 .*?ending(?: ended/ending)? \(date\)?\s+(\d{1,2}/\d{1,2}/\d{4})",
        text,
        flags=re.DOTALL
    )

    # --- Key dates ---
    ex_date = _find_value(r"Ex Date\s+(\d{1,2}/\d{1,2}/\d{4})", text)
    record_date = _find_value(r"(?:\+Record Date|Record Date)\s+(\d{1,2}/\d{1,2}/\d{4})", text)
    payment_date = _find_value(r"Payment Date\s+(\d{1,2}/\d{1,2}/\d{4})", text)

    # --- Currency & amounts ---
    # Currency in which dividend is made (primary currency)
    currency = _find_value(
        r"Currency in which the dividend/distribution is made.*?\n([A-Z]{3})",
        text,
        flags=re.DOTALL
    )

    # Amount per security in primary currency
    # Pattern 1: 2A.9 Total dividend/distribution payment amount per +security...
    amount_per_security = None
    if currency:
        amount_per_security = _find_float(
            rf"Total dividend/distribution payment amount per\s*\+security.*?\n{currency}\s+([\d\.]+)",
            text,
            flags=re.DOTALL
        )

    # Fallback Pattern 2: "Distribution Amount" block near top (AGL style)
    if amount_per_security is None:
        currency2 = _find_value(r"Distribution Amount\s+([A-Z]{3})", text)
        if currency2:
            currency = currency or currency2
            amount_per_security = _find_float(
                rf"Distribution Amount\s+{currency2}\s+([\d\.]+)",
                text
            )

    # AUD equivalent amount if defined (BHP style)
    aud_equivalent_amount = _find_float(
        r"2A\.9a AUD equivalent.*?\nAUD\s+([\d\.]+)",
        text,
        flags=re.DOTALL
    )

    # --- Franking info ---
    franking_percent = _find_float(
        r"Percentage of ordinary dividend/distribution that is\s+franked\s+([\d\.]+)",
        text,
        flags=re.DOTALL
    )

    franked_amount_per_security = None
    if currency:
        franked_amount_per_security = _find_float(
            rf"3A\.4 .*?franked amount per\s*\+security\s+{currency}\s+([\d\.]+)",
            text,
            flags=re.DOTALL
        )

    unfranked_amount_per_security = None
    if currency:
        unfranked_amount_per_security = _find_float(
            rf"3A\.6 .*?unfranked amount.*?\n{currency}\s+([\d\.]+)",
            text,
            flags=re.DOTALL
        )

        # --- DRP info ---
    drp_available = None
    if "Dividend/Distribution Reinvestment Plan (DRP)" in text or "We have a Dividend/Distribution Reinvestment Plan (DRP)" in text:
        drp_available = True
    elif "DRP" in text:
        drp_available = True
    else:
        drp_available = False

    drp_status = None
    m_status = re.search(
        r"DRP Status.*?(Full DRP|Partial DRP|No DRP|Suspended)",
        text,
        flags=re.DOTALL
    )
    if m_status:
        drp_status = m_status.group(1).strip()
    else:
        m_status_any = re.search(r"(Full DRP|Partial DRP|No DRP|Suspended)", text)
        if m_status_any:
            drp_status = m_status_any.group(1).strip()

    drp_price = None
    drp_price_currency = None
    m_price = re.search(
        r"DRP Price.{0,80}?([A-Z]{3})\s*([\d,]+\.\d+)",
        text,
        flags=re.DOTALL
    )
    if m_price:
        drp_price_currency = m_price.group(1).strip()
        try:
            drp_price = float(m_price.group(2).replace(",", ""))
        except ValueError:
            drp_price = None




    return DividendInfo(
        entity_name=entity_name,
        ticker=ticker,
        security_description=security_description,
        announcement_date=announcement_date,
        period_end_date=period_end_date,
        currency=currency,
        amount_per_security=amount_per_security,
        aud_equivalent_amount=aud_equivalent_amount,
        ex_date=ex_date,
        record_date=record_date,
        payment_date=payment_date,
        franking_percent=franking_percent,
        franked_amount_per_security=franked_amount_per_security,
        unfranked_amount_per_security=unfranked_amount_per_security,
        drp_available=drp_available,
        drp_status=drp_status,
        drp_price=drp_price,
        drp_price_currency=drp_price_currency,
    )
