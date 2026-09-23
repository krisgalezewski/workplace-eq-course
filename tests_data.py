# -*- coding: utf-8 -*-
"""Final test for Workplace EQ (covers Lessons 1-7).

Each test dict: {id, num, after_section, title, subtitle, part1, part2|None}
Item schema — see gen_test_template.py (mcq / gapfill).
"""


def mcq(prompt, right, wrong):
    return {"type": "mcq", "prompt": prompt,
            "options": [{"label": right, "value": "right", "correct": True},
                        {"label": wrong, "value": "wrong", "correct": False}]}


def gap(before, after, answers, width=110):
    return {"type": "gapfill", "before": before, "after": after, "answers": answers, "width": width}


TESTS = [{
    "id": "weq-test-01",
    "num": 1,
    "after_section": 3,
    "title": "Final Test: Workplace EQ",
    "subtitle": "Covers all seven lessons: presence, communication and career velocity.",
    "part1": {
        "heading": "Part 1 — What would you say?",
        "intro": "Choose the response that would work best in a British workplace.",
        "items": [
            # Lesson 1
            mcq("You're introduced to the CEO, who says \"Hi, I'm Linda.\" You reply…", "\"Nice to meet you, Linda.\"", "\"Nice to meet you, Mrs Linda.\""),
            mcq("You need to leave a conversation at a networking event. You say…", "\"Anyway, I'll let you mingle — lovely to meet you.\"", "\"I have to go now.\""),
            # Lesson 2
            mcq("You need help from a colleague in another team. You say…", "\"I was wondering if you could help me with the forecast.\"", "\"Help me with the forecast, please.\""),
            mcq("Your manager calls your proposal \"an interesting idea\" and changes the subject. She probably…", "has doubts about it", "wants you to start immediately"),
            # Lesson 3
            mcq("A colleague hasn't answered your email for five days. You write…", "\"Just following up on my email below — any news?\"", "\"I am still waiting for your answer.\""),
            mcq("Which sign-off suits a first email to a new client?", "\"Kind regards,\"", "\"Cheers,\""),
            # Lesson 4
            mcq("You want to add a point while someone is speaking. You say…", "\"Sorry to jump in — can I just add something?\"", "\"Wait, I need to say something.\""),
            mcq("The meeting has drifted off topic. You say…", "\"Shall we park that and come back to it at the end?\"", "\"This isn't relevant.\""),
            # Lesson 5
            mcq("You can't take on another project. You say…", "\"I'd love to, but I'm at capacity until June — could we look at it then?\"", "\"No. I'm too busy.\""),
            mcq("You made a mistake in a client report. Your first sentence is…", "\"I'm sorry — that's my mistake, and here's the corrected version.\"", "\"The template we use is confusing.\""),
            # Lesson 6
            mcq("Your director says \"Brilliant presentation!\" You reply…", "\"Thanks — Ola's research made it much stronger.\"", "\"Oh, it was nothing really.\""),
            mcq("You want to ask for a pay rise. You start with…", "\"I'd like to discuss my salary. This year I've taken on…\"", "\"I deserve more money.\""),
            # Lesson 7
            mcq("At a client dinner, the client starts talking about religion. You…", "keep it light and steer to another topic", "share your own views in detail"),
            mcq("Working with a Dutch team, you notice they're very direct. You…", "don't take it personally, and soften a little less yourself", "assume they're angry with you"),
        ],
    },
    "part2": {
        "heading": "Part 2 — Complete the phrase",
        "intro": "Type one word to complete each phrase from the course.",
        "items": [
            gap("Sorry, I didn't quite", "your name.", ["catch", "get"], 90),
            gap("I'm not", "convinced this will work.", ["entirely", "totally", "completely"], 100),
            gap("Would you", "moving the call to Thursday?", ["mind"], 80),
            gap("I look forward to", "from you.", ["hearing"], 100),
            gap("I take your", ", but I'm worried about the cost.", ["point"], 80),
            gap("Just", "of time — shall we move on?", ["conscious", "mindful"], 110),
            gap("Thanks for", "it — I'll fix it today.", ["flagging", "spotting", "mentioning"], 100),
            gap("One thing I'd", "is shortening the intro.", ["suggest"], 100),
            gap("Just a", "-up: the client might call this afternoon.", ["heads"], 90),
            gap("What would you need to", "from me to get there?", ["see"], 80),
        ],
    },
}]
