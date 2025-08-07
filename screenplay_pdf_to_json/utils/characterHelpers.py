import re
from sys import stderr

def isParenthetical(text):
    return bool(re.match(r'^\s*\(.*\)\s*$', text))


def extractCharacter(currentContent):
    text = currentContent["text"]
    split = text.split()
    modifier = text[text.find(
        "(")+1:text.find(")")] if text.find("(") != -1 else None
    character = text.replace(
        "("+modifier+")", "") if modifier is not None else text
    return {
        "character": character,
        "modifier": modifier,
    }


def isCharacter(currentContent):
    text = currentContent["text"]
    characterNameEnum = ["(V.O)", "(O.S)", "CONT'D", "(CONT'D)", "(V.O.)", "(O.S.)",
                         "VOICE OVER", "OFF SCREEN", "VOICEOVER", "OFFSCREEN",
                         "MORE", "(MORE)", "VOICE", "NARRATOR", "NARRATION",
                         "NARRATOR'S VOICE", "NARRATOR'S NARRATION", "NARRATOR'S VOICEOVER",
                         "NARRATOR'S OFFSCREEN", "NARRATOR'S OFFSCREEN VOICE"]

    if isParenthetical(text):
        return False

    for heading in characterNameEnum:
        if heading in text:
            return True

    if not text[0].isalpha() and "\"" not in text[0]:
        return False

    characterName = (text[0: text.index("(")] if "(" in text else text)
    if characterName != characterName.upper():
        return False

    # check if header?
    if any(x in text for x in ["--", "!", "?", "@", "%", "...", "THE END"]):
        return False

    if any(x in text[-1] for x in ["-"]):
        return False

    # Reducing the threshold for the text for the character detection,
    # text might not exactly stay in the center of the page (reduced from 150 to 75)
    if currentContent["x"] < 75:
        return False

    if any(x in text for x in [":"]):
        return False


    return True
