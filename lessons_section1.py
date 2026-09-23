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
