# -*- coding: utf-8 -*-
"""Section 3 — Career Velocity (Lessons 6-7).

Lesson 6 covers visibility and self-advocacy; Lesson 7 is the capstone
scenario that recycles language from all six earlier lessons.
"""
from gen_lesson_template import vocab, gram

SECTION_NAME = "Career Velocity"
THEME = "theme-velocity"

LESSONS = []

# ============================================================
# LESSON 6 — Visibility and self-advocacy
# ============================================================
LESSONS.append({
    "id": "weq-lesson-06-visibility-self-advocacy",
    "num": 6, "section_name": SECTION_NAME, "theme_class": THEME,
    "title": "Visibility & Self-Advocacy",
    "subtitle": "Making your work visible without bragging, managing up, and asking for the raise, the project or the promotion.",
    "warmup_intro": "Good work doesn't speak for itself; people speak for it. In British workplaces the challenge is doing that without sounding boastful, because modesty is valued and open self-promotion can seem un-British. The trick is to talk about results, share credit, and ask clearly.",
    "warmup": [
        {"prompt": "Your manager says \"Great job on the launch!\" The best British response is…",
         "options": [{"label": "\"Thanks! It was a real team effort — Sam did brilliant work on the testing.\"", "value": "right", "correct": True},
                     {"label": "\"Oh, it was nothing, really.\"", "value": "wrong", "correct": False}]},
        {"prompt": "You want to be considered for a promotion. You say to your manager…",
         "options": [{"label": "\"I'd like to talk about my next step here. What would you need to see from me?\"", "value": "right", "correct": True},
                     {"label": "\"I deserve a promotion. Everyone knows I'm the best on the team.\"", "value": "wrong", "correct": False}]},
        {"prompt": "\"Managing up\" means…",
         "options": [{"label": "making your manager's job easier and keeping them informed", "value": "right", "correct": True},
                     {"label": "trying to replace your manager", "value": "wrong", "correct": False}]},
    ],
    "warmup_tip": "Take a compliment with \"Thanks\" plus a mention of the team, not a denial. Talk about results and numbers rather than personal qualities. Ask for what you want in terms of what the business needs.",
    "diagnostic": [
        {"prompt": "In a weekly update, the best way to mention your success is…",
         "options": [{"label": "\"Quick win: the new process cut invoice errors by 40% this month.\"", "value": "right", "correct": True},
                     {"label": "\"I did an amazing job with the invoices.\"", "value": "wrong", "correct": False}]},
        {"prompt": "You want a pay rise. The strongest opening is…",
         "options": [{"label": "\"I'd like to discuss my salary. Over the last year I've taken on X and Y.\"", "value": "right", "correct": True},
                     {"label": "\"My rent has gone up, so I need more money.\"", "value": "wrong", "correct": False}]},
        {"prompt": "You met someone useful at a conference. The best follow-up is…",
         "options": [{"label": "\"Great to meet you on Thursday — here's the article I mentioned.\"", "value": "right", "correct": True},
                     {"label": "Adding them on LinkedIn with no message", "value": "wrong", "correct": False}]},
        {"prompt": "Your manager is about to meet the board. You…",
         "options": [{"label": "send a three-line summary of the key figures they might need", "value": "right", "correct": True},
                     {"label": "wait for them to ask", "value": "wrong", "correct": False}]},
    ],
    "widget": {
        "heading": "Three career-velocity skills",
        "intro": "Careers move faster for people who do three things well: <b>show their work</b> without bragging, <b>manage up</b> by making their manager's life easier, and <b>ask for what they want</b> clearly. Browse the phrases for each, then try the quick check.",
        "tabs": [{"key": "show", "label": "Showing your work"}, {"key": "up", "label": "Managing up"}, {"key": "ask", "label": "Asking for what you want"}, {"key": "quiz", "label": "Quick check"}],
        "categories": {
            "show": [
                {"label": "\"Quick win from this week: …\"", "example": "A light way to share a success in an update or stand-up. \"Quick\" keeps it modest."},
                {"label": "\"Thanks — it was a team effort, and Sam's testing made a big difference.\"", "example": "Accept the compliment and share credit. You look generous and confident at the same time."},
                {"label": "\"We managed to cut the turnaround time from five days to two.\"", "example": "Numbers speak for you. \"We managed to\" sounds modest, but the result is clear."},
                {"label": "\"I'd be happy to share what worked with the other teams.\"", "example": "Offering to help others spreads your name and sounds collaborative, not boastful."},
            ],
            "up": [
                {"label": "\"Just a heads-up: the supplier might be late.\"", "example": "Warn your manager early. Nobody likes surprises, especially bad ones."},
                {"label": "\"Here's a three-line summary for your meeting with the board.\"", "example": "Anticipate what your manager needs. It makes them look good, and they'll remember who helped."},
                {"label": "\"How would you like me to keep you updated?\"", "example": "Ask about their preferences: weekly email, quick chat, only when there's a problem."},
                {"label": "\"I've got two options — which would you prefer?\"", "example": "Bring solutions, not just problems. Your manager makes a quick decision; you look capable."},
            ],
            "ask": [
                {"label": "\"I'd like to talk about my next step here.\"", "example": "Opens a career conversation without demanding anything yet."},
                {"label": "\"What would you need to see from me to get there?\"", "example": "Makes your manager name the criteria. Now you both know the target."},
                {"label": "\"Over the past year I've taken on…\"", "example": "The evidence part of a pay or promotion request: specific responsibilities and results."},
                {"label": "\"I'd love the chance to lead the next project.\"", "example": "Asking for a stretch opportunity. Clear, positive, easy to say yes to."},
            ],
        },
        "quiz_labels": {"show": "showing your work", "up": "managing up", "ask": "asking for what you want"},
        "rules_html": '''
          <div class="formula" style="border-left-color:var(--c-present)">✅ <b>Show your work:</b> results + numbers + "we", in regular small doses (updates, stand-ups, a line in an email). Accept compliments with "Thanks" + credit to others.</div>
          <div class="formula" style="border-left-color:var(--c-continuous)">✅ <b>Manage up:</b> no surprises (a heads-up early), bring options not just problems, and learn how your manager likes to be updated.</div>
          <div class="formula" style="border-left-color:var(--c-future);margin-bottom:20px">✅ <b>Ask:</b> ask for the conversation first → evidence (what you've done) → the ask (specific) → their criteria ("What would you need to see?"). Base it on value to the business, not personal need.</div>
          <div class="warn-box">
            <span>🎯</span>
            <span style="flex:1;min-width:0"><b>The tricky part for Polish speakers:</b> two opposite traps.<br><br>
            <b>Too modest:</b> "It was nothing", "I just did my job", or never mentioning your results. British colleagues may simply believe you. → "Thanks — I'm really pleased with how it went."<br>
            <b>Too direct:</b> "I deserve a raise" or "I am the best specialist here" sounds arrogant in British English, even if it's true. → "I'd like to discuss my salary. Here's what I've delivered this year."<br><br>
            And don't base a pay request on personal costs ("My rent went up"). Base it on your value and the market.</span>
          </div>
          <div class="tip-box" style="margin-top:12px">🌍 <span style="flex:1;min-width:0"><b>Elsewhere:</b> Americans are usually more comfortable with open self-promotion ("I drove a 30% increase") and may expect you to advocate for yourself loudly. In Scandinavia, the \"Jante law\" makes self-promotion even less acceptable than in the UK. In more hierarchical cultures (much of Asia, parts of Southern Europe), asking your manager directly for a promotion may be unusual, and career moves happen through mentors and relationships.</span></div>'''
    },
    "compare": {
        "title": "Too blunt, too modest, or just right?",
        "instruction": "Hover over (or tap) each version to see how a British manager is likely to hear it.",
        "items": [
            {"key": "c1", "label": "Too blunt", "text": "I deserve a raise.", "explain": "Sounds entitled. It invites the question \"Why?\" and puts your manager on the defensive."},
            {"key": "c2", "label": "Too modest", "text": "I was just wondering, if it's not too much trouble, whether maybe my salary could possibly be looked at sometime?", "explain": "So hesitant that it's easy to ignore. It also suggests you don't believe in your own case."},
            {"key": "c3", "label": "Just right", "text": "I'd like to discuss my salary. This year I've taken on the Leeds account and cut reporting time by half.", "explain": "Clear request, specific evidence, no apology. Confident without being arrogant.", "groupEnd": True},
            {"key": "c4", "label": "Too blunt", "text": "The launch was a success because of me.", "explain": "Takes all the credit. Colleagues will remember it, and not kindly."},
            {"key": "c5", "label": "Too modest", "text": "Oh, I didn't really do anything.", "explain": "British people may take you at your word. Your contribution quietly disappears."},
            {"key": "c6", "label": "Just right", "text": "Thanks — I'm really pleased with how it went. Sam's testing made a huge difference.", "explain": "Accepts the praise, shows pride, shares credit. Everyone comes out looking good, including you."},
        ]
    },
    "reading": {
        "heading": "The Invisible Expert",
        "passage_paragraphs": [
            f'''For three years, Marek was the person everyone in his London team went to with difficult data problems. He fixed them quietly and moved on. When a senior analyst role came up, it went to a colleague who was, by most accounts, less skilled but far more {vocab("visible","visible")}. Marek's manager was surprised he was disappointed. \"I didn't know you wanted it,\" she said. \"And honestly, I didn't know how much you were doing.\"''',
            f'''Marek had assumed that good work would be noticed. In reality, managers are busy, and they notice what they hear about. A mentor suggested a small habit: a weekly update of three lines, one of them starting {gram("g1","“Quick win from this week:”")} followed by a result with a number in it. It felt uncomfortable at first, close to bragging. But because it described outcomes, not personal qualities, nobody saw it as boastful. It was just information.''',
            f'''He also learnt to {vocab("manage up","manage up")}. Before his manager's quarterly meeting with the directors, he sent her {gram("g2","“a three-line summary of the figures you might need”")}. When a supplier looked likely to miss a deadline, he gave her {gram("g3","“a heads-up”")} a week early, with two {vocab("options","options")} for dealing with it. His manager began to see him as someone who made her job easier, which is one of the most valuable {vocab("reputations","reputations")} anyone can have.''',
            f'''Six months later, Marek asked for the conversation he had avoided for years. He didn't say he deserved a promotion. He said {gram("g4","“I'd like to talk about my next step here,”")} listed three projects and their results, and finished with {gram("g5","“What would you need to see from me to get there?”")} His manager gave him two clear {vocab("criteria","criteria")}, and he met both by the spring. When colleagues congratulated him on the new role, he said {gram("g6","“Thanks — a lot of it was a team effort”")}, and meant it. {vocab("Self-advocacy","Self-advocacy")}, he realised, isn't about talking yourself up. It's about making sure the right people have the right information, and then asking.''',
        ],
        "comprehension": [
            {"prompt": "Why didn't Marek get the senior analyst role the first time?", "options": [
                {"label": "His manager didn't know he wanted it or how much he was doing.", "value": "right", "correct": True},
                {"label": "His technical skills weren't strong enough.", "value": "wrong", "correct": False}]},
            {"prompt": "Why wasn't the weekly update seen as bragging?", "options": [
                {"label": "It described results, not personal qualities.", "value": "right", "correct": True},
                {"label": "He only sent it to his closest colleagues.", "value": "wrong", "correct": False}]},
            {"prompt": "How did Marek finish his career conversation?", "options": [
                {"label": "By asking what his manager would need to see from him.", "value": "right", "correct": True},
                {"label": "By saying he would leave if he wasn't promoted.", "value": "wrong", "correct": False}]},
        ],
        "vocab_data": {
            "visible": {"word": "visible", "ipa": "/ˈvɪz.ə.bəl/", "meaning": "noticed and known about by others, especially people with influence", "example": "Presenting at the all-hands meeting made her work much more visible."},
            "manage up": {"word": "manage up", "ipa": "/ˈmæn.ɪdʒ ʌp/", "meaning": "to work effectively with your manager by anticipating their needs and keeping them informed", "example": "Learning to manage up is one of the fastest ways to build trust."},
            "options": {"word": "options", "ipa": "/ˈɒp.ʃənz/", "meaning": "possible choices", "example": "Don't just bring problems; bring options."},
            "reputations": {"word": "reputation", "ipa": "/ˌrep.jəˈteɪ.ʃən/", "meaning": "the opinion that people generally have of someone", "example": "She has a reputation for being reliable."},
            "criteria": {"word": "criteria", "ipa": "/kraɪˈtɪə.ri.ə/", "meaning": "the standards used to judge or decide something (singular: criterion)", "example": "What are the criteria for promotion?"},
            "Self-advocacy": {"word": "self-advocacy", "ipa": "/ˌself ˈæd.və.kə.si/", "meaning": "speaking up for your own interests and needs", "example": "Self-advocacy isn't the same as arrogance."},
        },
        "gram_explanations": {
            "g1": "A light, modest frame for a success. \"Quick\" makes it feel small and routine, while the result speaks for itself.",
            "g2": "Managing up: anticipating what your manager will need before they ask.",
            "g3": "\"A heads-up\" = an early warning. Managers value it enormously, because nobody likes surprises in front of their own boss.",
            "g4": "Asks for the conversation, not the promotion. It's low-pressure and hard to refuse.",
            "g5": "Makes the manager name the criteria. Now you have a clear target, and they've committed to it.",
            "g6": "Accepting praise the British way: thanks + shared credit. Confident and generous at once.",
        },
    },
    "vocab_check": {
        "match": [
            {"prompt": "If your work is \"visible\", it is…", "options": [{"label": "noticed by people who matter", "value": "right", "correct": True}, {"label": "finished on time", "value": "wrong", "correct": False}, {"label": "shared online", "value": "wrong2", "correct": False}]},
            {"prompt": "To \"manage up\" means to…", "options": [{"label": "work well with your manager by anticipating their needs", "value": "right", "correct": True}, {"label": "get promoted above your manager", "value": "wrong", "correct": False}, {"label": "complain to your manager's boss", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Criteria\" are…", "options": [{"label": "standards used to judge or decide something", "value": "right", "correct": True}, {"label": "criticisms", "value": "wrong", "correct": False}, {"label": "people who make decisions", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Self-advocacy\" means…", "options": [{"label": "speaking up for your own interests", "value": "right", "correct": True}, {"label": "working alone", "value": "wrong", "correct": False}, {"label": "being your own lawyer", "value": "wrong2", "correct": False}]},
            {"prompt": "A \"heads-up\" is…", "options": [{"label": "an early warning", "value": "right", "correct": True}, {"label": "a promotion", "value": "wrong", "correct": False}, {"label": "a type of meeting", "value": "wrong2", "correct": False}]},
        ],
        "gapfill": [
            {"before": "She has a", "after": "for always delivering on time.", "answers": ["reputation"], "width": 120},
            {"before": "What are the", "after": "for promotion to senior level?", "answers": ["criteria"], "width": 100},
            {"before": "Don't just bring your manager problems — bring", "after": ".", "answers": ["options", "solutions"], "width": 100},
            {"before": "Presenting at the conference made her work far more", "after": ".", "answers": ["visible"], "width": 100},
        ],
    },
    "practice": {
        "gapfill_focus": "self-advocacy phrases (one word per gap)",
        "gapfill": [
            {"before": "Quick", "after": "from this week: we closed the Leeds deal.", "answers": ["win"], "width": 80},
            {"before": "Just a", "after": "-up: the supplier might be late.", "answers": ["heads"], "width": 90},
            {"before": "It was a real team", "after": ".", "answers": ["effort"], "width": 90},
            {"before": "I'd like to talk about my next", "after": "here.", "answers": ["step", "move"], "width": 80},
            {"before": "What would you need to", "after": "from me to get there?", "answers": ["see"], "width": 80},
            {"before": "Over the past year I've taken", "after": "the Leeds account.", "answers": ["on", "over"], "width": 70},
        ],
        "second": {
            "type": "errorspot", "title": "Spot the faux pas",
            "instruction": "Each line hurts the speaker's career, by being too blunt or too modest. Tap the word that causes the problem.",
            "items": [
                {"words": ["I", "deserve", "a", "promotion", "this", "year."], "error_indices": [1], "explanation": "\"Deserve\" sounds entitled. Ask for the conversation and bring evidence: \"I'd like to talk about my next step here.\""},
                {"words": ["Oh,", "it", "was", "nothing,", "really."], "error_indices": [3], "explanation": "British listeners may believe you, and your contribution disappears. \"Thanks — I'm really pleased with how it went\" is modest enough."},
                {"words": ["I", "need", "a", "raise", "because", "my", "rent", "went", "up."], "error_indices": [6], "explanation": "Personal costs aren't a business reason. Base the request on value: \"This year I've taken on X and delivered Y.\""},
            ],
        },
        "builders": [
            {"words": ["I'd", "like", "to", "talk", "about", "my", "next", "step."]},
            {"words": ["What", "would", "you", "need", "to", "see", "from", "me?"]},
            {"words": ["Thanks", "—", "it", "was", "a", "real", "team", "effort."]},
        ],
    },
    "speaking": {
        "solo_text": "Prepare a 60-second pitch to your manager asking for a stretch opportunity (leading a project, a training course, or a new responsibility). Open by asking for the conversation, give two pieces of evidence with numbers if possible, make the specific ask, and end by asking what they'd need to see from you.",
        "group_questions": [
            "In your culture, is self-promotion admired, tolerated or disliked? How does that compare with British and American attitudes?",
            "Role-play: A compliments B's recent work. B responds the British way (thanks + shared credit). Then swap and try the American way. What feels different?",
            "What's one thing your manager could know about your work that they probably don't? How could you make it visible this week?",
        ],
    },
    "listening": {
        "intro": "Tomasz has his first annual review next week. He asks Anna for advice.",
        "dialogue": [
            {"speaker": "Tomasz", "line": "My review's on Tuesday. I was going to say I've worked very hard and I deserve a raise."},
            {"speaker": "Anna", "line": "Hmm. Everyone thinks they've worked hard. What have you actually delivered?"},
            {"speaker": "Tomasz", "line": "Well, I rebuilt the client dashboard. Reporting takes one day now instead of three."},
            {"speaker": "Anna", "line": "That's your opening line, then. Numbers, not adjectives."},
            {"speaker": "Tomasz", "line": "And if Claire says it's not the right time?"},
            {"speaker": "Anna", "line": "Ask her what she'd need to see from you, and when you can talk about it again. Then write it down."},
            {"speaker": "Tomasz", "line": "Should I mention that Ola helped with the testing?"},
            {"speaker": "Anna", "line": "Definitely. Sharing credit makes you look more senior, not less."},
        ],
        "comprehension": [
            {"prompt": "What does Anna think of \"I've worked very hard\"?", "options": [{"label": "It's weak, because everyone says it.", "value": "right", "correct": True}, {"label": "It's the best way to start a review.", "value": "wrong", "correct": False}]},
            {"prompt": "What should Tomasz do if Claire says it isn't the right time?", "options": [{"label": "Ask what she'd need to see and when they can talk again.", "value": "right", "correct": True}, {"label": "Tell her he'll look for another job.", "value": "wrong", "correct": False}]},
            {"prompt": "Why does Anna say Tomasz should mention Ola?", "options": [{"label": "Sharing credit makes him look more senior.", "value": "right", "correct": True}, {"label": "Ola asked him to mention her.", "value": "wrong", "correct": False}]},
        ],
    },
    "exit": [
        {"prompt": "The best response to \"Great job on the report!\" is…", "options": [{"label": "\"Thanks — Ola's analysis really helped.\"", "value": "right", "correct": True}, {"label": "\"It was nothing.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A strong case for a pay rise is based on…", "options": [{"label": "what you've delivered for the business", "value": "right", "correct": True}, {"label": "your personal expenses", "value": "wrong", "correct": False}]},
        {"prompt": "\"Just a heads-up\" introduces…", "options": [{"label": "an early warning", "value": "right", "correct": True}, {"label": "a compliment", "value": "wrong", "correct": False}]},
        {"prompt": "Managing up includes…", "options": [{"label": "bringing options, not just problems", "value": "right", "correct": True}, {"label": "doing your manager's job for them", "value": "wrong", "correct": False}]},
        {"prompt": "The best way to start a promotion conversation is…", "options": [{"label": "\"I'd like to talk about my next step here.\"", "value": "right", "correct": True}, {"label": "\"I want to be promoted now.\"", "value": "wrong", "correct": False}]},
    ],
})

# ============================================================
# LESSON 7 — Capstone: A Week in London
# ============================================================
LESSONS.append({
    "id": "weq-lesson-07-capstone-week-in-london",
    "num": 7, "section_name": SECTION_NAME, "theme_class": THEME,
    "title": "Capstone: A Week in London",
    "subtitle": "One working week, from Monday's first handshake to Friday's follow-up email, using everything from the course.",
    "warmup_intro": "This lesson follows one person through a busy week at a London company: a new team, a client dinner, a tense meeting, a mistake and a big opportunity. Each situation brings back language from Lessons 1–6. Let's start with a quick warm-up across the whole course.",
    "warmup": [
        {"prompt": "Monday. Your new team lead introduces himself as \"Rob\". You say…",
         "options": [{"label": "\"Nice to meet you, Rob.\"", "value": "right", "correct": True},
                     {"label": "\"Nice to meet you, Mr Rob.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Tuesday. You need a report from a colleague in another team. You write…",
         "options": [{"label": "\"Hi Jess — could you send me the Q3 report when you get a chance?\"", "value": "right", "correct": True},
                     {"label": "\"Jess, send me the Q3 report.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Wednesday. At the client dinner, the client asks what you think of the new prime minister. You…",
         "options": [{"label": "keep it light and steer to a safer topic", "value": "right", "correct": True},
                     {"label": "give your full political opinion", "value": "wrong", "correct": False}]},
    ],
    "warmup_tip": "The capstone doesn't add many new phrases. It asks you to choose the right one quickly, in context, under a bit of pressure, which is what real workplaces demand.",
    "diagnostic": [
        {"prompt": "Thursday's meeting: the director proposes a plan you think is risky. You say…",
         "options": [{"label": "\"I take your point, but I'm a bit worried about the budget.\"", "value": "right", "correct": True},
                     {"label": "\"That plan is too risky.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Thursday afternoon: you realise you sent the client the wrong file. You write…",
         "options": [{"label": "\"Apologies — I attached the wrong version. The correct one is here.\"", "value": "right", "correct": True},
                     {"label": "\"The system attached the wrong file.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Friday: Rob says you did a great job this week. You reply…",
         "options": [{"label": "\"Thanks — Jess's report made the client meeting much easier.\"", "value": "right", "correct": True},
                     {"label": "\"Yes, I know.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Friday: you'd like to lead the next client project. You say…",
         "options": [{"label": "\"I'd love the chance to lead the next one — what would you need to see from me?\"", "value": "right", "correct": True},
                     {"label": "\"I should lead the next project.\"", "value": "wrong", "correct": False}]},
    ],
    "widget": {
        "heading": "The whole course in three moves",
        "intro": "Every phrase in this course does one of three things. It builds your <b>presence</b> (how people see you), it helps your <b>communication</b> land (so people understand and act), or it adds to your <b>career velocity</b> (so your work and ambitions are noticed). Browse the best phrase from each lesson, then sort them in the quick check.",
        "tabs": [{"key": "pres", "label": "Presence"}, {"key": "comm", "label": "Communication"}, {"key": "vel", "label": "Career velocity"}, {"key": "quiz", "label": "Quick check"}],
        "categories": {
            "pres": [
                {"label": "\"I don't think we've met — I'm Kasia.\"", "example": "Lesson 1: open with your name and one useful detail."},
                {"label": "\"Anyway, I'll let you get back to it.\"", "example": "Lesson 1: leave a conversation gracefully."},
                {"label": "\"I was wondering if you could…\"", "example": "Lesson 2: soften a request with distance."},
                {"label": "\"I'm not entirely convinced.\"", "example": "Lesson 2: polite but clear disagreement."},
            ],
            "comm": [
                {"label": "\"Just following up on my email below.\"", "example": "Lesson 3: chase without nagging."},
                {"label": "\"Sorry to jump in — can I just add something?\"", "example": "Lesson 4: get the floor in a meeting."},
                {"label": "\"Shall we park that and come back to it?\"", "example": "Lesson 4: keep a meeting on track."},
                {"label": "\"I'd love to, but I'm at capacity until Friday.\"", "example": "Lesson 5: say no with a reason."},
            ],
            "vel": [
                {"label": "\"Quick win from this week: …\"", "example": "Lesson 6: make results visible without bragging."},
                {"label": "\"Just a heads-up: …\"", "example": "Lesson 6: manage up by warning early."},
                {"label": "\"I'd like to talk about my next step here.\"", "example": "Lesson 6: open a career conversation."},
                {"label": "\"Thanks — it was a real team effort.\"", "example": "Lesson 6: accept praise and share credit."},
            ],
        },
        "quiz_labels": {"pres": "presence", "comm": "communication", "vel": "career velocity"},
        "rules_html": '''
          <div class="formula" style="border-left-color:var(--c-present)">✅ <b>Presence:</b> follow the other person's lead on names and formality; soften requests and disagreements; decode understatement.</div>
          <div class="formula" style="border-left-color:var(--c-continuous)">✅ <b>Communication:</b> put the point first; chase lightly; get the floor with a short apology; disagree with acknowledge → concern → suggestion; say no with a reason and an alternative; apologise by owning it first.</div>
          <div class="formula" style="border-left-color:var(--c-future);margin-bottom:20px">✅ <b>Career velocity:</b> results and numbers, "we" and shared credit, no surprises for your manager, and ask for the conversation before you ask for the thing.</div>
          <div class="warn-box">
            <span>🎯</span>
            <span style="flex:1;min-width:0"><b>The one rule behind all of it:</b> be <b>clear about the message</b> and <b>generous about the person</b>. Blunt speakers forget the second half; over-polite speakers forget the first. Every "just right" example in this course does both.<br><br>
            If you're ever unsure, three questions help: <i>Would they know exactly what I want? Would they feel respected? Would I say this to someone senior?</i></span>
          </div>
          <div class="tip-box" style="margin-top:12px">🌍 <span style="flex:1;min-width:0"><b>Taking it abroad:</b> in the US, turn up the warmth and the self-promotion a notch. In Germany or the Netherlands, turn the softening down. In Japan or much of East Asia, turn the indirectness and the formality up. The British default is a good middle setting: easy to adjust in either direction.</span></div>'''
    },
    "compare": {
        "title": "Too blunt, too stiff, or just right? (mixed situations)",
        "instruction": "One example from each part of the week. Hover over (or tap) to see how each version lands.",
        "items": [
            {"key": "c1", "label": "Too blunt", "text": "What do you do and how much do you earn?", "explain": "Wednesday's client dinner: two questions too direct for a first meeting, and one of them is off-limits."},
            {"key": "c2", "label": "Too stiff", "text": "Might I enquire as to the nature of your professional responsibilities?", "explain": "So formal that the client will think you're joking."},
            {"key": "c3", "label": "Just right", "text": "So how long have you been with Harris? It sounds like a busy time for you.", "explain": "Friendly, open, and easy to answer. It keeps the conversation going.", "groupEnd": True},
            {"key": "c4", "label": "Too blunt", "text": "Your figures are wrong. Fix them.", "explain": "Thursday's meeting: an accusation plus an order, in front of everyone."},
            {"key": "c5", "label": "Too stiff", "text": "I would humbly suggest that the figures may perhaps contain some small inaccuracies.", "explain": "So softened that nobody knows how serious the problem is."},
            {"key": "c6", "label": "Just right", "text": "I'm not sure those figures are quite right — could we check them together after the meeting?", "explain": "Clear about the problem, generous to the person, and a private next step."},
        ]
    },
    "reading": {
        "heading": "Monday to Friday",
        "passage_paragraphs": [
            f'''<b>Monday.</b> Zofia's first day at a London fintech began with a round of introductions. When the head of product said \"Hi, I'm Rob,\" she answered {gram("g1","“Nice to meet you, Rob”")}, no title, no surname, and asked him how long he'd been with the company. By lunchtime she had a {vocab("rapport","rapport")} with half the team, mostly because she'd asked questions and listened to the answers.''',
            f'''<b>Tuesday and Wednesday.</b> She needed data from a team she'd never worked with, so she wrote {gram("g2","“I was wondering if you could send me the Q3 figures when you get a chance?”")} They arrived within the hour. On Wednesday evening she joined Rob at a client dinner. When the client raised politics over dessert, Zofia smiled, said it had been quite a year, and asked about his holiday plans instead. Her {vocab("discretion","discretion")} did not go unnoticed.''',
            f'''<b>Thursday.</b> In the strategy meeting, the director proposed doubling the marketing budget. Zofia thought the numbers didn't support it. She waited for a natural pause, then said {gram("g3","“Sorry to jump in — I take the point, but I'm a bit worried about the return on the last campaign.”")} The room paused, then agreed to look at the data again. That afternoon she discovered she had sent the client an old version of a proposal. Her email began {gram("g4","“Apologies — I attached the wrong version, and that's my mistake.”")} It was three lines long. The client replied with a smiley face.''',
            f'''<b>Friday.</b> Rob stopped by her desk. \"Great first week,\" he said. \"The client loved you.\" Zofia said {gram("g5","“Thanks — Jess's figures made the dinner conversation much easier”")}, and then, because the moment felt right, added {gram("g6","“I'd love the chance to lead the next client project. What would you need to see from me?”")} Rob looked {vocab("taken aback","taken aback")} for a second, then smiled and gave her two things to work on. She sent him a short {vocab("follow-up","follow-up")} email that afternoon summarising them. None of it was {vocab("rocket science","rocket science")}. It was simply the unwritten rules, followed consistently, for five days in a row.''',
        ],
        "comprehension": [
            {"prompt": "How did Zofia handle politics at the client dinner?", "options": [
                {"label": "She kept it light and moved to a safer topic.", "value": "right", "correct": True},
                {"label": "She shared her opinion honestly.", "value": "wrong", "correct": False}]},
            {"prompt": "What happened after Zofia disagreed in Thursday's meeting?", "options": [
                {"label": "The group agreed to look at the data again.", "value": "right", "correct": True},
                {"label": "The director asked her to leave the meeting.", "value": "wrong", "correct": False}]},
            {"prompt": "What did Zofia do after Rob praised her on Friday?", "options": [
                {"label": "Shared credit, asked to lead a project, and followed up in writing.", "value": "right", "correct": True},
                {"label": "Asked for an immediate pay rise.", "value": "wrong", "correct": False}]},
        ],
        "vocab_data": {
            "rapport": {"word": "rapport", "ipa": "/ræˈpɔː/", "meaning": "a friendly relationship in which people understand each other well", "example": "She built a quick rapport with the new team."},
            "discretion": {"word": "discretion", "ipa": "/dɪˈskreʃ.ən/", "meaning": "the ability to behave without causing embarrassment or revealing private information", "example": "The job requires tact and discretion."},
            "taken aback": {"word": "taken aback", "ipa": "/ˈteɪ.kən əˈbæk/", "meaning": "surprised, especially by something unexpected", "example": "I was taken aback by how direct she was."},
            "follow-up": {"word": "follow-up", "ipa": "/ˈfɒl.əʊ.ʌp/", "meaning": "a message or action that continues something done earlier", "example": "Send a short follow-up after every important meeting."},
            "rocket science": {"word": "rocket science", "ipa": "/ˈrɒk.ɪt ˌsaɪ.əns/", "meaning": "(informal, usually negative) something very complicated", "example": "Writing a good email isn't rocket science."},
        },
        "gram_explanations": {
            "g1": "Lesson 1: follow the other person's lead. He used his first name, so she did too.",
            "g2": "Lesson 2: a softened request with distance (\"I was wondering if…\") and a friendly time frame.",
            "g3": "Lessons 4 and 2: a polite interruption plus acknowledge → concern. Clear disagreement, no attack.",
            "g4": "Lesson 5: own the mistake in the first sentence. Short, accountable, fixed.",
            "g5": "Lesson 6: accept praise and share credit, naming the colleague.",
            "g6": "Lesson 6: ask for the opportunity, then ask for the criteria.",
        },
    },
    "vocab_check": {
        "match": [
            {"prompt": "\"Discretion\" is…", "options": [{"label": "the ability to behave tactfully and keep things private", "value": "right", "correct": True}, {"label": "a discount for clients", "value": "wrong", "correct": False}, {"label": "a strong opinion", "value": "wrong2", "correct": False}]},
            {"prompt": "If you're \"taken aback\", you are…", "options": [{"label": "surprised", "value": "right", "correct": True}, {"label": "promoted", "value": "wrong", "correct": False}, {"label": "angry", "value": "wrong2", "correct": False}]},
            {"prompt": "A \"follow-up\" email…", "options": [{"label": "continues something that started earlier", "value": "right", "correct": True}, {"label": "is sent to everyone in the company", "value": "wrong", "correct": False}, {"label": "is always a complaint", "value": "wrong2", "correct": False}]},
            {"prompt": "\"It isn't rocket science\" means…", "options": [{"label": "It isn't complicated.", "value": "right", "correct": True}, {"label": "It isn't interesting.", "value": "wrong", "correct": False}, {"label": "It isn't allowed.", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Rapport\" is…", "options": [{"label": "a good understanding between people", "value": "right", "correct": True}, {"label": "a written report", "value": "wrong", "correct": False}, {"label": "a formal complaint", "value": "wrong2", "correct": False}]},
        ],
        "gapfill": [
            {"before": "HR matters need to be handled with complete", "after": ".", "answers": ["discretion"], "width": 120},
            {"before": "I was a bit taken", "after": "by his reaction.", "answers": ["aback"], "width": 90},
            {"before": "I'll send a quick", "after": "email with the action points.", "answers": ["follow-up", "followup"], "width": 110},
            {"before": "Good small talk isn't rocket", "after": "— just ask and listen.", "answers": ["science"], "width": 100},
        ],
    },
    "practice": {
        "gapfill_focus": "mixed phrases from the whole course (one word per gap)",
        "gapfill": [
            {"before": "I don't think we've", "after": "— I'm Zofia, I've just joined the product team.", "answers": ["met"], "width": 80},
            {"before": "Would you", "after": "sending me the Q3 figures?", "answers": ["mind"], "width": 80},
            {"before": "Just following", "after": "on my email from Monday.", "answers": ["up"], "width": 70},
            {"before": "Sorry to jump", "after": ", but can I add something?", "answers": ["in"], "width": 70},
            {"before": "I'm afraid I'm at", "after": "until Friday.", "answers": ["capacity"], "width": 100},
            {"before": "Just a", "after": "-up: the client may call you this afternoon.", "answers": ["heads"], "width": 90},
        ],
        "second": {
            "type": "errorspot", "title": "Spot the faux pas: the whole week",
            "instruction": "One line from each part of Zofia's week, as a less skilful colleague might have said it. Tap the word that causes the problem.",
            "items": [
                {"words": ["Good", "morning,", "Mrs", "Jess,", "send", "me", "the", "figures."], "error_indices": [2], "explanation": "Two problems, one tap: \"Mrs\" + a first name is wrong, and the request is an order. \"Hi Jess — could you send me the figures?\""},
                {"words": ["Unfortunately", "the", "system", "attached", "the", "wrong", "file."], "error_indices": [2], "explanation": "Blaming the system sounds like an excuse. Own it: \"Apologies — I attached the wrong file.\""},
                {"words": ["I", "deserve", "to", "lead", "the", "next", "project."], "error_indices": [1], "explanation": "Sounds entitled. \"I'd love the chance to lead the next project — what would you need to see from me?\""},
            ],
        },
        "builders": [
            {"words": ["I'd", "love", "the", "chance", "to", "lead", "the", "next", "one."]},
            {"words": ["Apologies", "—", "I", "attached", "the", "wrong", "version."]},
            {"words": ["I", "was", "wondering", "if", "you", "could", "send", "the", "figures."]},
        ],
    },
    "speaking": {
        "solo_text": "Record a 90-second \"week in review\" as if you were Zofia talking to a friend on Friday evening. Describe one moment from each day and quote the exact phrase she used, then say which one you'd find hardest in real life and why.",
        "group_questions": [
            "Full role-play (5 minutes): new employee, team lead and client. Cover an introduction, a request, a disagreement, an apology and a career ask. The group gives feedback using \"What worked really well was…\" and \"One thing I'd suggest is…\".",
            "Which lesson in this course changed the way you'll speak at work the most? Give one example of something you'll say differently.",
            "Think of a real situation coming up at your work in the next month. Which phrases from this course will you use, and how?",
        ],
    },
    "listening": {
        "intro": "It's Friday evening. Anna and Tomasz look back on his first few months in London.",
        "dialogue": [
            {"speaker": "Anna", "line": "So, three months in. What's the biggest thing you've learnt?"},
            {"speaker": "Tomasz", "line": "That my English was never the problem. It was the rules nobody writes down."},
            {"speaker": "Anna", "line": "Like \"Mr Richard\"?"},
            {"speaker": "Tomasz", "line": "Please don't. But yes, names, softening, chasing, all of it. I actually jumped in at the meeting today."},
            {"speaker": "Anna", "line": "I noticed. \"I take your point, but I'm a bit worried about the timeline.\" Textbook."},
            {"speaker": "Tomasz", "line": "And Claire said my dashboard was \"not bad at all\". I've learnt that's a compliment."},
            {"speaker": "Anna", "line": "A big one. Have you asked her about leading the next phase?"},
            {"speaker": "Tomasz", "line": "Monday morning. I've booked twenty minutes, and I know my first line: \"I'd like to talk about my next step here.\""},
        ],
        "comprehension": [
            {"prompt": "What does Tomasz say was his real challenge?", "options": [{"label": "The unwritten rules, not his English.", "value": "right", "correct": True}, {"label": "His pronunciation.", "value": "wrong", "correct": False}]},
            {"prompt": "How does Tomasz now understand \"not bad at all\"?", "options": [{"label": "As a genuine compliment.", "value": "right", "correct": True}, {"label": "As hidden criticism.", "value": "wrong", "correct": False}]},
            {"prompt": "What is Tomasz planning for Monday?", "options": [{"label": "A conversation with Claire about his next step.", "value": "right", "correct": True}, {"label": "A client dinner with Anna.", "value": "wrong", "correct": False}]},
        ],
    },
    "exit": [
        {"prompt": "The rule behind the whole course is…", "options": [{"label": "be clear about the message and generous about the person", "value": "right", "correct": True}, {"label": "always be as formal as possible", "value": "wrong", "correct": False}]},
        {"prompt": "At a client dinner, politics comes up. You…", "options": [{"label": "keep it light and change the subject", "value": "right", "correct": True}, {"label": "debate it in detail", "value": "wrong", "correct": False}]},
        {"prompt": "You sent the wrong file. Your first sentence is…", "options": [{"label": "\"Apologies — I attached the wrong version.\"", "value": "right", "correct": True}, {"label": "\"The software didn't work properly.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Your manager praises you. You reply…", "options": [{"label": "\"Thanks — the team made a big difference.\"", "value": "right", "correct": True}, {"label": "\"I know, I worked very hard.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Working with Dutch or German colleagues, you might…", "options": [{"label": "use a bit less softening than with British colleagues", "value": "right", "correct": True}, {"label": "add even more understatement", "value": "wrong", "correct": False}]},
    ],
})
