import re

def numeric_consistency_check(llm_draft: str, tool_results: list) -> str:
    numbers_in_draft = re.findall(r"\b\d+(?:\.\d+)?\b", llm_draft)
    tool_text = " ".join([str(res) for res in tool_results])
    
    for num in numbers_in_draft:
        # ignore trivial numbers
        if num in ["1", "2", "3", "0", "0.0"]:
            continue
        if num not in tool_text:
            return "Based on the latest data, I cannot safely confirm those numbers. Please check the dashboard directly."
            
    return llm_draft
    
def enforce_trust_gate(llm_draft: str, tool_results: list) -> str:
    tool_text = " ".join([str(res) for res in tool_results])
    if "INSUFFICIENT_DATA" in tool_text or "Trust score is Insufficient" in tool_text:
        return "I do not have enough reliable recent data to make a strong recommendation. Please refer to local traders or wait for data to refresh."
    return llm_draft
