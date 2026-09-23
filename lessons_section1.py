# -*- coding: utf-8 -*-
"""Section 1 — Professional Presence (Lessons 1-2).

Norms taught are British by default; US and international differences
are flagged in the rules panel ("🌍 Elsewhere") and in explanations.
In this course the reading's highlighted spans (gram()) mark KEY
PHRASES rather than grammar forms — each explanation says why the
phrase works and, where useful, what a less skilful speaker might say.
"""
from gen_lesson_template import vocab, gram

SECTION_NAME = "Professional Presence"
THEME = "theme-presence"

LESSONS = []

# ============================================================
# LESSON 1 — First impressions, introductions and small talk
# ============================================================
LESSONS.append({
    "id": "weq-lesson-01-first-impressions",
    "num": 1, "section_name": SECTION_NAME, "theme_class": THEME,
    "title": "First Impressions & Small Talk",
    "subtitle": "Introductions, names, safe topics, and how to leave a conversation without leaving a bad impression.",
    "warmup_intro": "Most first impressions at work are made in under two minutes, and almost none of that time is spent on anything important. That's the point: small talk is how British colleagues decide whether you're easy to work with. Let's see what your instincts say.",
    "warmup": [
        {"prompt": "A British colleague says \"Hi, how are you?\" as you pass in the corridor. The best reply is…",
         "options": [{"label": "\"Good, thanks — you?\"", "value": "right", "correct": True},
                     {"label": "An honest update on how your week is going", "value": "wrong", "correct": False}]},
        {"prompt": "You've been introduced to Helen Price, a senior director, at a London client event. She says \"Hi, I'm Helen.\" You call her…",
         "options": [{"label": "Helen", "value": "right", "correct": True},
                     {"label": "Mrs Helen", "value": "wrong", "correct": False}]},
        {"prompt": "Which topic is the safest opener with someone you've just met at a work event?",
         "options": [{"label": "How they got there, or what brought them to the event", "value": "right", "correct": True},
                     {"label": "What they think of the new government", "value": "wrong", "correct": False}]},
    ],
    "warmup_tip": "In British workplaces, \"How are you?\" is a greeting, not a question. First names are normal almost immediately, even with senior people, once they've offered theirs. The rule of thumb: follow the other person's lead.",
    "diagnostic": [
        {"prompt": "You want to introduce your manager to a client. The most natural line is…",
         "options": [{"label": "\"Sarah, have you met Tom? Tom's our head of sales.\"", "value": "right", "correct": True},
                     {"label": "\"Sarah, I present to you Tom, our head of sales.\"", "value": "wrong", "correct": False}]},
        {"prompt": "You've forgotten the name of someone you met last week. You say…",
         "options": [{"label": "\"I'm so sorry — remind me of your name?\"", "value": "right", "correct": True},
                     {"label": "\"What is your name?\"", "value": "wrong", "correct": False}]},
        {"prompt": "At the end of a first conversation, the natural British phrase is…",
         "options": [{"label": "\"Lovely to meet you.\"", "value": "right", "correct": True},
                     {"label": "\"It was a pleasure to make your acquaintance.\"", "value": "wrong", "correct": False}]},
        {"prompt": "You need to leave a conversation at a networking event. You say…",
         "options": [{"label": "\"I'll let you get back to the party — great talking to you.\"", "value": "right", "correct": True},
                     {"label": "\"OK, I'm going now. Bye.\"", "value": "wrong", "correct": False}]},
    ],
    "widget": {
        "heading": "The three moves of any first conversation",
        "intro": "Every short professional conversation has three moves: you <b>open</b> it (greet, introduce, get names right), you <b>keep it going</b> (safe topics, follow-up questions, small reactions), and you <b>close</b> it gracefully. Browse the phrases for each move, then try the quick check.",
        "tabs": [{"key": "open", "label": "Opening"}, {"key": "keep", "label": "Keeping it going"}, {"key": "close", "label": "Closing gracefully"}, {"key": "quiz", "label": "Quick check"}],
        "categories": {
            "open": [
                {"label": "\"I don't think we've met — I'm Kasia, I look after the Kraków office.\"", "example": "Introducing yourself to a stranger. Name + one useful detail gives the other person something to reply to."},
                {"label": "\"Tom, have you met Sarah? Sarah's just joined us from Deloitte.\"", "example": "Introducing two people. Add a detail they can both talk about, then step back."},
                {"label": "\"Sorry, I didn't quite catch your name.\"", "example": "When you missed it the first time. Much better to ask now than to avoid using their name all evening."},
                {"label": "\"Nice to meet you.\"", "example": "The standard response when you're introduced. \"How do you do?\" still exists but sounds very formal and old-fashioned to most people under 60."},
            ],
            "keep": [
                {"label": "\"How do you know the host?\"", "example": "The perfect event opener: everybody has an answer, and the answer gives you your next question."},
                {"label": "\"Did you have far to come?\"", "example": "The journey is the British small-talk topic after the weather. Safe, neutral, and it works anywhere."},
                {"label": "\"Oh really? How did you end up doing that?\"", "example": "A follow-up question. People remember you as a good talker when you let them do most of the talking."},
                {"label": "\"Awful weather today, isn't it?\"", "example": "A tag question invites agreement, not debate. It isn't really about the weather; it's about showing you're friendly."},
            ],
            "close": [
                {"label": "\"I'll let you get back to it.\"", "example": "Leaving by giving the other person their time back. Polite, and nobody feels abandoned."},
                {"label": "\"I must just go and say hello to someone — lovely to meet you.\"", "example": "A reason to move on. It doesn't have to be dramatic, and nobody will check."},
                {"label": "\"Let's grab a coffee sometime — I'll drop you an email.\"", "example": "Closing with a next step. Only say it if you'll actually send the email."},
                {"label": "\"Great talking to you — enjoy the rest of the evening.\"", "example": "A warm, simple exit. Use their name here if you can; it shows you listened."},
            ],
        },
        "quiz_labels": {"open": "an opening move", "keep": "a keeping-it-going move", "close": "a closing move"},
        "rules_html": '''
          <div class="formula" style="border-left-color:var(--c-present)">✅ <b>Open:</b> name + one detail. "I'm Kasia — I look after the Kraków office." Then use their name once, early, so it sticks.</div>
          <div class="formula" style="border-left-color:var(--c-continuous)">✅ <b>Keep it going:</b> safe topic → open question → follow-up. Journey, the event, the weekend, holidays, work in general. Not salary, politics, religion, age or anyone's weight.</div>
          <div class="formula" style="border-left-color:var(--c-future);margin-bottom:20px">✅ <b>Close:</b> a softener + a reason or a next step + a warm line. "Anyway, I'll let you get back to it — lovely to meet you."</div>
          <div class="warn-box">
            <span>🎯</span>
            <span style="flex:1;min-width:0"><b>The tricky part for Polish speakers:</b> in Polish, <i>Pan Tomasz</i> or <i>Pani Kasia</i> is perfectly polite. In English, a title goes only with a <b>surname</b>, never a first name.<br><br>
            ❌ "Mr Tom", "Mrs Helen" — sounds like a child talking to a teacher, or a hotel receptionist.<br>
            ✅ "Tom" (once he's introduced himself as Tom) or "Mr Clarke" (only in very formal first contact, e.g. an email to someone you've never met).<br><br>
            Also: in British English there is <b>no full stop</b> after Mr, Mrs, Ms or Dr. Use <b>Ms</b> for a woman unless you know she prefers something else.</span>
          </div>
          <div class="tip-box" style="margin-top:12px">🌍 <span style="flex:1;min-width:0"><b>Elsewhere:</b> Americans tend to be warmer and faster ("Great to meet you!", "So what do you do?" in the first minute). In Germany, Austria and much of Asia, titles and surnames last much longer (<i>Frau Dr Weber</i>), so wait to be invited to use a first name. In Japan and Korea, business cards are offered and received with both hands and read before being put away.</span></div>'''
    },
    "compare": {
        "title": "Too blunt, too stiff, or just right?",
        "instruction": "Hover over (or tap) each version to see how a British listener is likely to hear it.",
        "items": [
            {"key": "c1", "label": "Too blunt", "text": "What is your job?", "explain": "Grammatically fine, but it sounds like a form you're filling in. A direct question with no softener, asked in the first minute, can come across as an interrogation."},
            {"key": "c2", "label": "Too stiff", "text": "May I enquire as to your profession?", "explain": "Over-formal. It sounds like a butler in a period drama, and the other person will wonder if you're joking."},
            {"key": "c3", "label": "Just right", "text": "So what brings you here — are you with one of the sponsors?", "explain": "Asks the same thing indirectly, through the event. It also gives them an easy first answer.", "groupEnd": True},
            {"key": "c4", "label": "Too blunt", "text": "I have to go now.", "explain": "True, but it sounds like you're escaping. The other person is left wondering what they said wrong."},
            {"key": "c5", "label": "Too stiff", "text": "I regret that I must now take my leave.", "explain": "Very formal and theatrical. In a conversation it sounds like a parody."},
            {"key": "c6", "label": "Just right", "text": "Anyway, I'll let you mingle — really nice to meet you.", "explain": "\"Anyway\" signals the end is coming, \"I'll let you…\" makes leaving sound like a favour to them, and the warm line finishes on a positive note."},
        ]
    },
    "reading": {
        "heading": "The First Ninety Seconds",
        "passage_paragraphs": [
            f'''When Marta moved from Warsaw to a consultancy in London, her English was better than that of half her new colleagues. Her first week still felt oddly difficult. At her welcome drinks, the managing partner came over, smiled and said, {gram("g1","“Hi, I'm James — I don't think we've met properly.”")} Marta, anxious to be respectful, replied, "Good evening, Mr James." He laughed kindly, but she saw the {vocab("awkward","awkward")} flicker in his eyes and spent the rest of the evening replaying it.''',
            f'''Her mistake was not grammar. It was {vocab("register","register")}: the level of formality a situation expects. British offices tend to hide {vocab("hierarchy","hierarchy")} rather than display it. Senior people introduce themselves by first name, and the expected response is simply {gram("g2","“Nice to meet you, James.”")} Being too formal doesn't come across as respect. It creates distance, and in a culture that prizes being {vocab("approachable","approachable")}, distance can be mistaken for coldness.''',
            f'''Small talk, which many learners dismiss as {vocab("trivial","trivial")}, is where most of this happens. A question like {gram("g3","“Did you have far to come?”")} is not really about the journey. It's a low-risk way of checking that the other person is friendly and easy to talk to. The best conversationalists are rarely the most interesting people in the room; they are the ones who ask {gram("g4","“Oh really? How did you end up doing that?”")} and then actually listen to the answer.''',
            f'''Leaving a conversation matters too. Marta's instinct was to wait until the other person walked away, which meant she often stood {vocab("stranded","stranded")} with one person for an hour. A colleague taught her an exit line: {gram("g5","“Anyway, I'll let you get back to it — lovely to meet you.”")} It sounds considerate, it's {vocab("courteous","courteous")}, and nobody has ever been offended by it. By her third event, Marta was using {gram("g6","“Sorry, I didn't quite catch your name”")} without embarrassment, and a {vocab("rapport","rapport")} with her new team followed soon after. As she put it later, \"Nobody taught me any of this at school, because none of it is written down.\"''',
        ],
        "comprehension": [
            {"prompt": "Why did James react awkwardly to Marta's greeting?", "options": [
                {"label": "Because \"Mr\" + first name was far too formal (and incorrect) for the situation.", "value": "right", "correct": True},
                {"label": "Because she made a grammar mistake with \"Good evening\".", "value": "wrong", "correct": False}]},
            {"prompt": "According to the text, what is a question like \"Did you have far to come?\" really for?", "options": [
                {"label": "A low-risk way of checking the other person is friendly.", "value": "right", "correct": True},
                {"label": "Finding out practical information about travel.", "value": "wrong", "correct": False}]},
            {"prompt": "What problem did the exit line solve for Marta?", "options": [
                {"label": "She no longer got stuck talking to one person all evening.", "value": "right", "correct": True},
                {"label": "She no longer forgot people's names.", "value": "wrong", "correct": False}]},
        ],
        "vocab_data": {
            "awkward": {"word": "awkward", "ipa": "/ˈɔː.kwəd/", "meaning": "causing or feeling embarrassment; uncomfortable", "example": "There was an awkward silence after his joke."},
            "register": {"word": "register", "ipa": "/ˈredʒ.ɪ.stə/", "meaning": "the level of formality of language used in a particular situation", "example": "An email to your team needs a different register from a letter to a client."},
            "hierarchy": {"word": "hierarchy", "ipa": "/ˈhaɪə.rɑː.ki/", "meaning": "a system in which people are ranked by status or authority", "example": "The company has a very flat hierarchy."},
            "approachable": {"word": "approachable", "ipa": "/əˈprəʊ.tʃə.bəl/", "meaning": "friendly and easy to talk to", "example": "Our new director is surprisingly approachable."},
            "trivial": {"word": "trivial", "ipa": "/ˈtrɪv.i.əl/", "meaning": "of little importance or value", "example": "It may seem trivial, but remembering names matters."},
            "stranded": {"word": "stranded", "ipa": "/ˈstræn.dɪd/", "meaning": "stuck in a place or situation with no easy way out", "example": "I was stranded by the buffet with the one person I didn't want to talk to."},
            "courteous": {"word": "courteous", "ipa": "/ˈkɜː.ti.əs/", "meaning": "polite and showing respect for others", "example": "She sent a courteous reply to every applicant."},
            "rapport": {"word": "rapport", "ipa": "/ræˈpɔː/", "meaning": "a friendly relationship in which people understand each other well", "example": "He quickly built a rapport with the client."},
        },
        "gram_explanations": {
            "g1": "Name + a softened opener. \"I don't think we've met\" is the classic British way to start: it's friendly, and it takes the blame for not having met off the other person. \"Properly\" adds warmth: we've seen each other, but never really talked.",
            "g2": "The standard, safe response. Match their register: he used his first name, so you use it back. Using the name once also helps you remember it.",
            "g3": "A classic safe opener. Everybody has an answer, it's never controversial, and the answer (\"Only from Richmond\", \"I flew in from Oslo\") gives you your next question.",
            "g4": "\"Oh really?\" shows interest; \"How did you end up…?\" is an open question that invites a story. Compare \"What is your job?\", which gets a one-word answer and sounds like a form.",
            "g5": "\"Anyway\" is the signal that the conversation is closing. \"I'll let you get back to it\" frames leaving as a favour to them, and \"lovely to meet you\" finishes on a warm note.",
            "g6": "The polite repair when you missed a name. \"Didn't quite catch\" puts the problem on the noise, not on them or your memory. Far better than avoiding their name for the rest of the evening.",
        },
    },
    "vocab_check": {
        "match": [
            {"prompt": "If a person is \"approachable\", they are…", "options": [{"label": "friendly and easy to talk to", "value": "right", "correct": True}, {"label": "very senior in the company", "value": "wrong", "correct": False}, {"label": "physically close to you", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Register\" in communication means…", "options": [{"label": "the level of formality you choose", "value": "right", "correct": True}, {"label": "a list of attendees at an event", "value": "wrong", "correct": False}, {"label": "your accent", "value": "wrong2", "correct": False}]},
            {"prompt": "A \"hierarchy\" is…", "options": [{"label": "a system that ranks people by status or authority", "value": "right", "correct": True}, {"label": "a type of formal greeting", "value": "wrong", "correct": False}, {"label": "a social event for new employees", "value": "wrong2", "correct": False}]},
            {"prompt": "If you have \"rapport\" with someone, you…", "options": [{"label": "understand each other well and get on", "value": "right", "correct": True}, {"label": "have to report to them", "value": "wrong", "correct": False}, {"label": "disagree with them politely", "value": "wrong2", "correct": False}]},
            {"prompt": "Something \"trivial\" is…", "options": [{"label": "unimportant", "value": "right", "correct": True}, {"label": "difficult", "value": "wrong", "correct": False}, {"label": "rude", "value": "wrong2", "correct": False}]},
        ],
        "gapfill": [
            {"before": "There was an", "after": "silence when he called her \"Mrs Anna\".", "answers": ["awkward"], "width": 110},
            {"before": "Nobody rescued me, so I was", "after": "by the coffee machine for forty minutes.", "answers": ["stranded"], "width": 110},
            {"before": "It's", "after": "to reply to every invitation, even if you can't go.", "answers": ["courteous", "polite"], "width": 110},
            {"before": "Small talk may look", "after": ", but it builds trust.", "answers": ["trivial"], "width": 100},
        ],
    },
    "practice": {
        "gapfill_focus": "complete the phrase (one word per gap)",
        "gapfill": [
            {"before": "I don't think we've", "after": "— I'm Olek, I'm on the data team.", "answers": ["met"], "width": 90},
            {"before": "Sorry, I didn't quite", "after": "your name.", "answers": ["catch", "get"], "width": 90},
            {"before": "Tom, have you", "after": "Sarah? She's just joined from Deloitte.", "answers": ["met"], "width": 90},
            {"before": "Did you have", "after": "to come today?", "answers": ["far"], "width": 80},
            {"before": "Anyway, I'll let you get", "after": "to it — lovely to meet you.", "answers": ["back"], "width": 90},
            {"before": "Oh really? How did you", "after": "up working in insurance?", "answers": ["end"], "width": 90},
        ],
        "second": {
            "type": "errorspot", "title": "Spot the faux pas",
            "instruction": "Each line is grammatically fine but socially wrong for a British workplace. Tap the word that causes the problem, then check the explanation.",
            "items": [
                {"words": ["Nice", "to", "meet", "you,", "Mr", "David."], "error_indices": [4], "explanation": "\"Mr\" + a first name doesn't work in English. Say \"Nice to meet you, David.\" (or \"Mr Jones\" in very formal contexts)."},
                {"words": ["So", "how", "much", "do", "you", "earn", "there?"], "error_indices": [5], "explanation": "Salary is off-limits in British small talk. Try \"So how long have you been there?\" instead."},
                {"words": ["Great", "to", "meet", "you!", "How", "old", "are", "you,", "by", "the", "way?"], "error_indices": [5], "explanation": "Age is off-limits with people you've just met (and often with colleagues you know well). Ask about their role, the event or their journey instead."},
            ],
        },
        "builders": [
            {"words": ["I", "don't", "think", "we've", "met", "—", "I'm", "Kasia."]},
            {"words": ["Sorry,", "I", "didn't", "quite", "catch", "your", "name."]},
            {"words": ["I'll", "let", "you", "get", "back", "to", "the", "party."]},
        ],
    },
    "speaking": {
        "solo_text": "Record a 60-second \"elevator introduction\" for a networking event in London: your name, one useful detail about what you do, and one question you'd ask the other person. Then add a graceful exit line at the end.",
        "group_questions": [
            "Role-play: one of you is the host of a work event and introduces the other two to each other. Keep the conversation going for one minute, then everyone leaves it gracefully.",
            "What are the \"safe\" and \"unsafe\" small-talk topics in your country? Which British ones surprise you?",
            "Tell your group about a first impression (yours or someone else's) that went badly. What would you say differently now?",
        ],
    },
    "listening": {
        "intro": "Tomasz has just started at the London office. Anna asks how his first networking event went.",
        "dialogue": [
            {"speaker": "Anna", "line": "So, how was the drinks thing last night? Did you survive?"},
            {"speaker": "Tomasz", "line": "Just about. I think I called the finance director \"Mr Richard\" — twice."},
            {"speaker": "Anna", "line": "Oh no. Honestly, he'll have found it charming. Everyone's Richard here, even to the interns."},
            {"speaker": "Tomasz", "line": "Then I got stuck with a man from procurement for about an hour. I didn't know how to get away."},
            {"speaker": "Anna", "line": "You just say something like, \"Anyway, I'll let you get back to it — lovely to meet you,\" and off you go."},
            {"speaker": "Tomasz", "line": "That's it? Nobody thinks it's rude?"},
            {"speaker": "Anna", "line": "Not at all. It's rude to trap someone. Leaving nicely is doing them a favour."},
            {"speaker": "Tomasz", "line": "Right. Next time: first names, ask how they got there, and leave before the hour's up."},
        ],
        "comprehension": [
            {"prompt": "What mistake did Tomasz make with the finance director?", "options": [{"label": "He used \"Mr\" with his first name.", "value": "right", "correct": True}, {"label": "He forgot the director's name.", "value": "wrong", "correct": False}]},
            {"prompt": "What does Anna say about leaving a conversation?", "options": [{"label": "Leaving politely is actually a favour to the other person.", "value": "right", "correct": True}, {"label": "You should wait for the other person to leave first.", "value": "wrong", "correct": False}]},
            {"prompt": "Which small-talk opener does Tomasz plan to use next time?", "options": [{"label": "Asking how people got to the event.", "value": "right", "correct": True}, {"label": "Asking what people earn.", "value": "wrong", "correct": False}]},
        ],
    },
    "exit": [
        {"prompt": "Your new manager introduces herself as \"Jo\". You call her…", "options": [{"label": "Jo", "value": "right", "correct": True}, {"label": "Mrs Jo", "value": "wrong", "correct": False}]},
        {"prompt": "The best opener at a conference coffee break is…", "options": [{"label": "\"Have you been to one of these before?\"", "value": "right", "correct": True}, {"label": "\"Which party did you vote for?\"", "value": "wrong", "correct": False}]},
        {"prompt": "You missed someone's name. You say…", "options": [{"label": "\"Sorry, I didn't quite catch your name.\"", "value": "right", "correct": True}, {"label": "\"Repeat your name.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Which exit line sounds most natural?", "options": [{"label": "\"Anyway, I'll let you mingle — great to meet you.\"", "value": "right", "correct": True}, {"label": "\"I will leave this conversation now.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A colleague says \"How are you?\" in the lift. The best answer is…", "options": [{"label": "\"Not bad, thanks — you?\"", "value": "right", "correct": True}, {"label": "A detailed account of your weekend", "value": "wrong", "correct": False}]},
    ],
})

# ============================================================
# LESSON 2 — Politeness, register and British understatement
# ============================================================
LESSONS.append({
    "id": "weq-lesson-02-politeness-register",
    "num": 2, "section_name": SECTION_NAME, "theme_class": THEME,
    "title": "Politeness & Register",
    "subtitle": "Softening requests, disagreeing without offending, and decoding what British colleagues really mean.",
    "warmup_intro": "Polish is a precise, fairly direct language, and \"please\" does a lot of the polite work. British English does the politeness in the whole sentence instead: past tenses, modal verbs, little words like \"just\" and \"slightly\". Leave them out and a perfectly correct sentence can sound like an order.",
    "warmup": [
        {"prompt": "You need a colleague's slides. Which sounds more natural in a British office?",
         "options": [{"label": "\"Could you send me the slides when you get a chance?\"", "value": "right", "correct": True},
                     {"label": "\"Please send me the slides.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Your British manager says your proposal is \"an interesting idea\". Most likely she means…",
         "options": [{"label": "She has doubts and probably won't go ahead with it.", "value": "right", "correct": True},
                     {"label": "She's excited and wants to discuss it further.", "value": "wrong", "correct": False}]},
        {"prompt": "\"I was wondering if you could help me\" uses the past tense because…",
         "options": [{"label": "it makes the request softer and less direct", "value": "right", "correct": True},
                     {"label": "the wondering happened yesterday", "value": "wrong", "correct": False}]},
    ],
    "warmup_tip": "Politeness in English is mostly built from distance: past tense (\"I wanted to ask\"), modals (\"could\", \"would\", \"might\"), softeners (\"just\", \"a bit\", \"slightly\") and questions instead of statements. \"Please\" on its own doesn't turn an order into a request.",
    "diagnostic": [
        {"prompt": "You disagree with a colleague's figures in a meeting. You say…",
         "options": [{"label": "\"I'm not sure those figures are quite right.\"", "value": "right", "correct": True},
                     {"label": "\"Your figures are wrong.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Which request is softest?",
         "options": [{"label": "\"Would you mind moving the meeting to Thursday?\"", "value": "right", "correct": True},
                     {"label": "\"Move the meeting to Thursday, please.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A British client says: \"With the greatest respect, I think we need to look at this again.\" They are…",
         "options": [{"label": "fairly annoyed and strongly disagreeing", "value": "right", "correct": True},
                     {"label": "showing great respect for your work", "value": "wrong", "correct": False}]},
        {"prompt": "\"It's not bad\" from a British colleague usually means…",
         "options": [{"label": "it's quite good, maybe even good", "value": "right", "correct": True},
                     {"label": "it's bad, but they're being kind", "value": "wrong", "correct": False}]},
    ],
    "widget": {
        "heading": "Three kinds of softening",
        "intro": "British politeness does three jobs: it <b>softens requests</b> so they don't sound like orders, it <b>softens disagreement</b> so people don't lose face, and it uses <b>understatement</b>, saying less than you mean, which listeners are expected to decode. Browse each, then try the quick check.",
        "tabs": [{"key": "req", "label": "Softening requests"}, {"key": "dis", "label": "Softening disagreement"}, {"key": "under", "label": "Understatement"}, {"key": "quiz", "label": "Quick check"}],
        "categories": {
            "req": [
                {"label": "\"I was wondering if you could take a look at this.\"", "example": "Past continuous + \"if\" = maximum distance. Good for asking a favour of someone senior or someone you don't know well."},
                {"label": "\"Would you mind sending me the latest version?\"", "example": "\"Would you mind + -ing\" is polite and very common. The expected answer is \"Not at all\" or \"No problem\"."},
                {"label": "\"Could you just check the dates for me?\"", "example": "\"Just\" makes the task sound small and quick, which makes it easier to say yes to."},
                {"label": "\"Is there any chance you could get it to me by Friday?\"", "example": "Frames a deadline as a possibility, not a demand, while still making the deadline clear."},
            ],
            "dis": [
                {"label": "\"I'm not sure that's quite right.\"", "example": "Means \"I think that's wrong.\" \"Not sure\" + \"quite\" gives the other person room to check without being embarrassed."},
                {"label": "\"I see what you mean, but I wonder if…\"", "example": "Acknowledge first, then disagree. \"I wonder if\" turns your objection into a suggestion."},
                {"label": "\"I'm not entirely convinced.\"", "example": "A polite but firm \"no\". \"Not entirely\" sounds gentle, yet everybody understands it as a real objection."},
                {"label": "\"Wouldn't it be better to wait until the data's in?\"", "example": "A negative question presents your opinion as something the other person probably agrees with already."},
            ],
            "under": [
                {"label": "\"That's an interesting idea.\"", "example": "Often means \"I don't think that will work.\" Watch the tone and whether any follow-up is suggested."},
                {"label": "\"It's not bad at all.\"", "example": "Means \"It's good.\" British praise is often expressed through negatives."},
                {"label": "\"There are just a few minor issues.\"", "example": "Can mean \"This needs serious work.\" In feedback, \"minor\" is sometimes not minor at all."},
                {"label": "\"With the greatest respect…\"", "example": "Means \"I think you're wrong, and I'm getting irritated.\" The more respect is mentioned, the less there is."},
            ],
        },
        "quiz_labels": {"req": "a softened request", "dis": "softened disagreement", "under": "understatement"},
        "rules_html": '''
          <div class="formula" style="border-left-color:var(--c-present)">✅ <b>Distance with tense:</b> "I wanted to ask…", "I was wondering if…", "I was hoping you could…". The past tense means "now", but it sounds less pushy.</div>
          <div class="formula" style="border-left-color:var(--c-continuous)">✅ <b>Distance with modals and questions:</b> could / would / might, "Would you mind + -ing?", "Is there any chance…?", "Wouldn't it be better to…?"</div>
          <div class="formula" style="border-left-color:var(--c-future);margin-bottom:20px">✅ <b>Softeners:</b> just, a bit, slightly, quite, perhaps, not entirely, I'm not sure. They shrink the size of the request or the criticism.</div>
          <div class="warn-box">
            <span>🎯</span>
            <span style="flex:1;min-width:0"><b>The tricky part for Polish speakers:</b> translating directly from Polish produces sentences that are correct but sound like orders: "I want…", "Give me…", "You must…", "Send it to me, please." In Polish, <i>proszę</i> does the polite work. In English, "please" + an imperative is still an instruction.<br><br>
            ❌ "Please send me the report today." (to a colleague) — sounds like a manager giving an order.<br>
            ✅ "Could you send me the report today, if possible?"<br><br>
            The opposite mistake exists too: stacking every softener ("I was just wondering if you could possibly perhaps…") sounds nervous or sarcastic. One or two softeners per sentence is enough.</span>
          </div>
          <div class="tip-box" style="margin-top:12px">🌍 <span style="flex:1;min-width:0"><b>Elsewhere:</b> Americans are usually more direct in requests but more enthusiastic in praise ("This is awesome!"), so British "not bad" can sound cold to them, and American "quite good" means <i>very</i> good, while British "quite good" means only fairly good. Dutch, German and Israeli colleagues are often more direct than the British and may find heavy softening confusing. In Japan and much of East Asia, disagreement is even more indirect than in the UK.</span></div>'''
    },
    "compare": {
        "title": "Too blunt, too stiff, or just right?",
        "instruction": "Hover over (or tap) each version to see how a British listener is likely to hear it.",
        "items": [
            {"key": "c1", "label": "Too blunt", "text": "Send me the report by Friday.", "explain": "An order. From a peer it sounds rude; even from a manager it sounds cold."},
            {"key": "c2", "label": "Too stiff", "text": "Would you be so kind as to furnish me with the report at your earliest convenience?", "explain": "So formal it sounds sarcastic, and \"at your earliest convenience\" hides the actual deadline."},
            {"key": "c3", "label": "Just right", "text": "Could you send me the report by Friday, if that works for you?", "explain": "A clear request with a clear deadline, softened with a modal and a small \"if\" clause.", "groupEnd": True},
            {"key": "c4", "label": "Too blunt", "text": "That's wrong.", "explain": "Direct disagreement in front of others makes people defensive. In a British meeting it can feel like an attack."},
            {"key": "c5", "label": "Too stiff", "text": "I must humbly and respectfully register my profound disagreement.", "explain": "So elaborate that it sounds either sarcastic or like a courtroom."},
            {"key": "c6", "label": "Just right", "text": "I'm not sure that's quite right — could we look at the figures again?", "explain": "The disagreement is clear, but it's framed as uncertainty plus a practical next step, so nobody loses face."},
        ]
    },
    "reading": {
        "heading": "What They Say, What They Mean",
        "passage_paragraphs": [
            f'''Piotr had been in the Manchester office for three months when he realised he had been misunderstanding his manager all along. Whenever he suggested an idea, Claire would smile and say, {gram("g1","“That's an interesting idea, Piotr.”")} He went away pleased and started working on it. It took an {vocab("awkward","awkward")} conversation with a colleague to learn that, in Claire's mouth, \"interesting\" usually meant \"no\".''',
            f'''Piotr's problem was the reverse of the one many British people have abroad. He came from a culture where being {vocab("candid","candid")} is a sign of respect: if you disagree, you say so, and nobody takes it personally. British professional culture relies far more on {vocab("understatement","understatement")}. Criticism arrives wrapped in softeners, like {gram("g2","“I'm not entirely convinced”")} or {gram("g3","“There are just a few minor points”")}, and the listener is expected to hear the real message underneath.''',
            f'''The same system works in the other direction. When Piotr emailed Claire, \"I want to take Friday off,\" he meant nothing rude; it was simply a clear statement. To Claire, it sounded {vocab("blunt","blunt")}, almost like a demand. A more {vocab("tactful","tactful")} version would have been {gram("g4","“I was wondering if I could take Friday off?”")} The past tense and the question form do the polite work that \"proszę\" does in Polish.''',
            f'''None of this means the British are dishonest. Understatement is a shared code, and it is full of {vocab("nuance","nuance")}: {gram("g5","“With the greatest respect”")} signals strong disagreement, while \"not bad at all\" is genuine praise. The skill is to be {vocab("diplomatic","diplomatic")} without being vague. Piotr's colleague summed it up: \"Say what you mean, but put a cushion around it. {gram("g6","“Could we look at the numbers again?”")} gets you further than \"Your numbers are wrong,\" even when the numbers are wrong.\" Once Piotr stopped taking every phrase literally, he stopped being {vocab("misread","misread")} too.''',
        ],
        "comprehension": [
            {"prompt": "What did Piotr eventually learn about Claire's phrase \"That's an interesting idea\"?", "options": [
                {"label": "It usually meant she wasn't going to accept the idea.", "value": "right", "correct": True},
                {"label": "It meant she wanted him to develop the idea immediately.", "value": "wrong", "correct": False}]},
            {"prompt": "Why did Piotr's email about Friday cause a problem?", "options": [
                {"label": "\"I want…\" sounded like a demand to a British reader.", "value": "right", "correct": True},
                {"label": "He asked for the wrong day off.", "value": "wrong", "correct": False}]},
            {"prompt": "What is the main message of the final paragraph?", "options": [
                {"label": "Be clear about what you mean, but soften how you say it.", "value": "right", "correct": True},
                {"label": "Avoid disagreeing with British colleagues at all.", "value": "wrong", "correct": False}]},
        ],
        "vocab_data": {
            "awkward": {"word": "awkward", "ipa": "/ˈɔː.kwəd/", "meaning": "causing embarrassment or discomfort", "example": "It was an awkward conversation, but a useful one."},
            "candid": {"word": "candid", "ipa": "/ˈkæn.dɪd/", "meaning": "honest and direct, even when the truth is unwelcome", "example": "She gave me a candid opinion of my presentation."},
            "understatement": {"word": "understatement", "ipa": "/ˈʌn.dəˌsteɪt.mənt/", "meaning": "saying that something is less important, serious or good than it really is", "example": "\"A bit of a problem\" was an understatement: the server was down for two days."},
            "blunt": {"word": "blunt", "ipa": "/blʌnt/", "meaning": "saying what you think directly, without trying to be polite", "example": "His feedback was accurate but very blunt."},
            "tactful": {"word": "tactful", "ipa": "/ˈtækt.fəl/", "meaning": "careful not to upset or embarrass people", "example": "There's no tactful way to tell him the project's cancelled."},
            "nuance": {"word": "nuance", "ipa": "/ˈnjuː.ɑːns/", "meaning": "a very small difference in meaning, tone or feeling", "example": "Learners often miss the nuance in \"quite good\"."},
            "diplomatic": {"word": "diplomatic", "ipa": "/ˌdɪp.ləˈmæt.ɪk/", "meaning": "able to deal with people politely and without causing bad feeling", "example": "She gave a diplomatic answer that didn't upset either side."},
            "misread": {"word": "misread", "ipa": "/ˌmɪsˈriːd/", "meaning": "to understand someone or something wrongly", "example": "I completely misread the situation."},
        },
        "gram_explanations": {
            "g1": "Classic British understatement. Said warmly with no follow-up question, \"interesting\" often means \"I'm not keen.\" If she'd said \"Interesting — can you put some numbers on it?\", that would be real interest.",
            "g2": "A polite but firm objection. \"Not entirely\" sounds gentle, yet it's understood as \"I disagree.\"",
            "g3": "\"Just\" and \"minor\" shrink the criticism. In feedback this can hide quite significant problems, so always ask which points matter most.",
            "g4": "Past continuous + \"if\" + a question: three layers of distance that turn a demand into a request. Compare \"I want to take Friday off.\"",
            "g5": "Formal respect language used as a warning. The speaker strongly disagrees and wants you to notice.",
            "g6": "A disagreement turned into a shared next step (\"could we…\"). Nobody is accused, and the problem still gets fixed.",
        },
    },
    "vocab_check": {
        "match": [
            {"prompt": "A \"tactful\" person is someone who…", "options": [{"label": "is careful not to upset or embarrass people", "value": "right", "correct": True}, {"label": "always says exactly what they think", "value": "wrong", "correct": False}, {"label": "is very good at planning", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Understatement\" means…", "options": [{"label": "presenting something as less serious or good than it is", "value": "right", "correct": True}, {"label": "a written summary of a meeting", "value": "wrong", "correct": False}, {"label": "exaggerating to make a point", "value": "wrong2", "correct": False}]},
            {"prompt": "If feedback is \"blunt\", it is…", "options": [{"label": "direct, with no attempt to soften it", "value": "right", "correct": True}, {"label": "vague and hard to understand", "value": "wrong", "correct": False}, {"label": "very positive", "value": "wrong2", "correct": False}]},
            {"prompt": "A \"nuance\" is…", "options": [{"label": "a small but important difference in meaning or tone", "value": "right", "correct": True}, {"label": "a rude remark", "value": "wrong", "correct": False}, {"label": "a new rule", "value": "wrong2", "correct": False}]},
            {"prompt": "If you \"misread\" a situation, you…", "options": [{"label": "understand it wrongly", "value": "right", "correct": True}, {"label": "handle it perfectly", "value": "wrong", "correct": False}, {"label": "read about it too late", "value": "wrong2", "correct": False}]},
        ],
        "gapfill": [
            {"before": "She's refreshingly", "after": ": she tells you exactly what she thinks of your work.", "answers": ["candid", "blunt"], "width": 110},
            {"before": "A good manager stays", "after": "even when two team members are arguing.", "answers": ["diplomatic", "tactful"], "width": 120},
            {"before": "\"A slight delay\" was an", "after": ": the launch was three months late.", "answers": ["understatement"], "width": 150},
            {"before": "It was an", "after": "moment when she realised he'd been joking.", "answers": ["awkward"], "width": 100},
        ],
    },
    "practice": {
        "gapfill_focus": "softening phrases (one word per gap)",
        "gapfill": [
            {"before": "I was", "after": "if you could help me with the budget.", "answers": ["wondering"], "width": 110},
            {"before": "Would you", "after": "sending me the latest version?", "answers": ["mind"], "width": 90},
            {"before": "I'm not", "after": "convinced this is the right approach.", "answers": ["entirely", "totally", "completely"], "width": 100},
            {"before": "Could you", "after": "check these dates for me?", "answers": ["just", "quickly"], "width": 90},
            {"before": "Is there any", "after": "you could get it to me by Friday?", "answers": ["chance", "way"], "width": 100},
            {"before": "I see what you", "after": ", but I wonder if we should wait.", "answers": ["mean"], "width": 90},
        ],
        "second": {
            "type": "errorspot", "title": "Spot the faux pas",
            "instruction": "Each sentence is grammatically correct but too direct for a British workplace. Tap the word that makes it sound rude.",
            "items": [
                {"words": ["You", "must", "send", "me", "the", "figures", "today."], "error_indices": [1], "explanation": "\"Must\" sounds like an order from above. Try \"Could you send me the figures today, if possible?\""},
                {"words": ["I", "want", "a", "copy", "of", "the", "slides."], "error_indices": [1], "explanation": "\"I want\" sounds demanding. \"Could I get a copy of the slides?\" or \"Would you mind sharing the slides?\" is the natural request."},
                {"words": ["Honestly,", "your", "plan", "is", "wrong."], "error_indices": [4], "explanation": "A flat verdict on someone's work causes loss of face. \"I'm not sure the plan quite works — can we talk it through?\""},
            ],
        },
        "builders": [
            {"words": ["Would", "you", "mind", "sending", "me", "the", "figures?"]},
            {"words": ["I", "was", "wondering", "if", "you", "could", "help."]},
            {"words": ["I'm", "not", "sure", "that's", "quite", "right."]},
        ],
    },
    "speaking": {
        "solo_text": "Take three direct sentences you might say at work (e.g. \"Send me the file.\", \"That's wrong.\", \"I want Friday off.\") and say a softened British version of each. Then explain which technique you used each time: past tense, a modal, a softener or a question.",
        "group_questions": [
            "Is your first language more direct or more indirect than British English? Give an example of a phrase that doesn't translate well.",
            "Have you ever misread someone's politeness (or had your directness misread)? What happened?",
            "Role-play: one person asks for something difficult (a deadline extension, a day off). The other says no using only understatement. Can the group decode the real answer?",
        ],
    },
    "listening": {
        "intro": "Tomasz shows Anna an email he's about to send to their manager, Claire.",
        "dialogue": [
            {"speaker": "Tomasz", "line": "Can you look at this before I send it? \"Claire, I want to take Friday off. Please confirm.\""},
            {"speaker": "Anna", "line": "Hmm. It's clear, I'll give you that. But she'll read it as an order."},
            {"speaker": "Tomasz", "line": "Really? I said please."},
            {"speaker": "Anna", "line": "Please doesn't do much on its own. Try \"I was wondering if I could take Friday off — would that be OK?\""},
            {"speaker": "Tomasz", "line": "That's so much longer to say the same thing."},
            {"speaker": "Anna", "line": "It isn't the same thing, though. Yours tells her. Mine asks her. By the way, what did she say about your dashboard idea?"},
            {"speaker": "Tomasz", "line": "She said it was an interesting idea. So I've started building it."},
            {"speaker": "Anna", "line": "Ah. I might hold off on that until she mentions it again."},
        ],
        "comprehension": [
            {"prompt": "What's wrong with Tomasz's original email, according to Anna?", "options": [{"label": "It sounds like he's telling Claire rather than asking her.", "value": "right", "correct": True}, {"label": "It doesn't say which Friday he means.", "value": "wrong", "correct": False}]},
            {"prompt": "What does Anna say about the word \"please\"?", "options": [{"label": "On its own it doesn't make a sentence polite.", "value": "right", "correct": True}, {"label": "It should always go at the start of a request.", "value": "wrong", "correct": False}]},
            {"prompt": "Why does Anna suggest waiting before building the dashboard?", "options": [{"label": "\"Interesting idea\" probably didn't mean yes.", "value": "right", "correct": True}, {"label": "Claire said the budget isn't ready yet.", "value": "wrong", "correct": False}]},
        ],
    },
    "exit": [
        {"prompt": "The most natural way to ask a colleague for help is…", "options": [{"label": "\"Could you give me a hand with this?\"", "value": "right", "correct": True}, {"label": "\"Help me with this, please.\"", "value": "wrong", "correct": False}]},
        {"prompt": "\"I'm not entirely convinced\" means…", "options": [{"label": "I disagree, politely.", "value": "right", "correct": True}, {"label": "I agree, but I need more time.", "value": "wrong", "correct": False}]},
        {"prompt": "\"With the greatest respect…\" usually signals…", "options": [{"label": "strong disagreement", "value": "right", "correct": True}, {"label": "admiration", "value": "wrong", "correct": False}]},
        {"prompt": "Which is a softened disagreement?", "options": [{"label": "\"I see what you mean, but I wonder if…\"", "value": "right", "correct": True}, {"label": "\"No, that's not true.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A British colleague calls your report \"not bad at all\". That's…", "options": [{"label": "a genuine compliment", "value": "right", "correct": True}, {"label": "a polite complaint", "value": "wrong", "correct": False}]},
    ],
})
