"""Scoring anchors shared by the S10 handout and presentation_scoring.md."""
SCORING = {
    "Clarity": ["The finding is not stated.", "The finding appears late or is unclear.",
                "The finding is stated first and is mostly clear.", "The finding is stated first, in one sentence, and everything supports it."],
    "Evidence": ["No numbers or chart.", "Numbers are given but not linked to the finding.",
                 "One chart or number clearly supports the finding.", "The evidence is checked, simple, and answers the question directly."],
    "Recommendation": ["There is none.", "It is vague, like do better.", "A clear action.",
                       "A clear action, with who and why, linked to the evidence."],
    "Delivery": ["Reads the slides, no structure.", "Some structure, but rushed or too long.",
                 "Clear structure and on time.", "Clear structure, on time, calm pace, numbers said simply."],
}
