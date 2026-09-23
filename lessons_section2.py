# -*- coding: utf-8 -*-
"""Section 2 — Communication That Lands (Lessons 3-5).

British norms by default; US/international notes in each rules panel.
Reading highlights (gram()) mark key phrases, not grammar forms.
"""
from gen_lesson_template import vocab, gram

SECTION_NAME = "Communication That Lands"
THEME = "theme-communication"

LESSONS = []

# ============================================================
# LESSON 3 — Emails and messaging
# ============================================================
LESSONS.append({
    "id": "weq-lesson-03-emails-messaging",
    "num": 3, "section_name": SECTION_NAME, "theme_class": THEME,
    "title": "Emails & Messaging",
    "subtitle": "Openings and closings, chasing without nagging, apologising for delays, and the unwritten rules of Slack and Teams.",
    "warmup_intro": "Written messages lose your smile, your tone of voice and your chance to explain. Every word has to do that work instead. A British reader forms an opinion of you from the first line and the sign-off, often before reading the middle.",
    "warmup": [
        {"prompt": "You're emailing Helen Clarke, a client you've never met. The best opening is…",
         "options": [{"label": "\"Dear Ms Clarke,\"", "value": "right", "correct": True},
                     {"label": "\"Respected Mrs Helen,\"", "value": "wrong", "correct": False}]},
        {"prompt": "A colleague hasn't replied for a week. Your follow-up starts…",
         "options": [{"label": "\"Just following up on my email below…\"", "value": "right", "correct": True},
                     {"label": "\"I am still waiting for your answer.\"", "value": "wrong", "correct": False}]},
        {"prompt": "On Slack or Teams, you need a quick answer from someone. You send…",
         "options": [{"label": "\"Hi Mark — quick one: is the Q3 deck final, or still in progress?\"", "value": "right", "correct": True},
                     {"label": "\"Hi\" … and wait for them to reply before asking", "value": "wrong", "correct": False}]},
    ],
    "warmup_tip": "Match the formality of the person you're writing to, and move one step less formal once they do. Chase with \"just following up\", never \"I'm still waiting\". In chat, put the greeting and the question in the same message.",
    "diagnostic": [
        {"prompt": "Which sign-off is right for a first email to a client?",
         "options": [{"label": "\"Kind regards,\"", "value": "right", "correct": True},
                     {"label": "\"Cheers,\"", "value": "wrong", "correct": False}]},
        {"prompt": "You replied to an email three days late. You start with…",
         "options": [{"label": "\"Apologies for the slow reply — it's been a hectic week.\"", "value": "right", "correct": True},
                     {"label": "\"I didn't have time to answer before.\"", "value": "wrong", "correct": False}]},
        {"prompt": "The most natural British way to end a request email is…",
         "options": [{"label": "\"Thanks in advance — let me know if you have any questions.\"", "value": "right", "correct": True},
                     {"label": "\"Waiting for your quick reply.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A client emails 30 people about a change. You have a question just for her. You…",
         "options": [{"label": "reply only to her", "value": "right", "correct": True},
                     {"label": "reply all, so everyone can see your question", "value": "wrong", "correct": False}]},
    ],
    "widget": {
        "heading": "The three jobs of a work message",
        "intro": "Most work messages do one of three jobs: they <b>open and close</b> at the right level of formality, they <b>ask or chase</b> without sounding pushy, or they <b>apologise and clarify</b> when something has gone wrong. Browse each, then try the quick check.",
        "tabs": [{"key": "frame", "label": "Opening & closing"}, {"key": "ask", "label": "Asking & chasing"}, {"key": "fix", "label": "Apologising & clarifying"}, {"key": "quiz", "label": "Quick check"}],
        "categories": {
            "frame": [
                {"label": "\"Dear Ms Clarke,\" … \"Kind regards,\"", "example": "First contact, especially with clients or someone senior you don't know. Surname + title, no full stop after Ms."},
                {"label": "\"Hi Helen,\" … \"Best wishes,\"", "example": "The default for most British work email once you've been in contact. Friendly but professional."},
                {"label": "\"I hope you're well.\"", "example": "A light opener before getting to the point. One line is enough; don't write a paragraph of pleasantries."},
                {"label": "\"Thanks, Tom\" / \"Cheers, Tom\"", "example": "Internal and informal. \"Cheers\" is common in the UK between colleagues, but it's too casual for a first client email."},
            ],
            "ask": [
                {"label": "\"Could you let me know by Thursday whether…?\"", "example": "A clear request with a clear deadline. Soft phrasing, specific content."},
                {"label": "\"Just following up on my email below.\"", "example": "The standard polite chase. It assumes they're busy, not ignoring you."},
                {"label": "\"Just bumping this to the top of your inbox.\"", "example": "A lighter, more informal second chase. Good with colleagues, a bit casual for clients."},
                {"label": "\"No rush, but it'd be great to have this by Friday.\"", "example": "Friendly urgency. \"No rush\" softens it; the deadline is still there."},
            ],
            "fix": [
                {"label": "\"Apologies for the slow reply.\"", "example": "Short and professional. No need for long excuses; one reason at most."},
                {"label": "\"Sorry, I should have been clearer.\"", "example": "Takes the blame for a misunderstanding, even when it's partly theirs. Very British and very effective."},
                {"label": "\"Just to clarify — did you mean the March figures or the April ones?\"", "example": "Checking meaning without suggesting the other person wrote badly."},
                {"label": "\"Please ignore my previous email — wrong attachment!\"", "example": "Quick correction. Admit it lightly and move on; everyone has done it."},
            ],
        },
        "quiz_labels": {"frame": "opening or closing", "ask": "asking or chasing", "fix": "apologising or clarifying"},
        "rules_html": '''
          <div class="formula" style="border-left-color:var(--c-present)">✅ <b>The formality ladder:</b> Dear Ms Clarke → Dear Helen → Hi Helen → Helen → (no greeting, in a thread). Start one step more formal than you think you need, then copy the other person.</div>
          <div class="formula" style="border-left-color:var(--c-continuous)">✅ <b>Structure:</b> greeting → one-line opener → the point (in the first two lines) → the request + deadline → a warm close. Busy people read the top and skim the rest.</div>
          <div class="formula" style="border-left-color:var(--c-future);margin-bottom:20px">✅ <b>Chat (Slack/Teams):</b> greeting + question in one message; use threads; don't message someone's private chat for something a channel should see; respect status ("Away", "Focusing").</div>
          <div class="warn-box">
            <span>🎯</span>
            <span style="flex:1;min-width:0"><b>The tricky part for Polish speakers:</b> some very natural Polish email formulas sound strange or pushy when translated.<br><br>
            ❌ "Respected Mr Kowalski" (<i>Szanowny Panie</i>) → ✅ "Dear Mr Kowalski"<br>
            ❌ "I am waiting for your answer" (<i>Czekam na odpowiedź</i>) → ✅ "I look forward to hearing from you"<br>
            ❌ "Greetings" (<i>Pozdrawiam</i>) as a sign-off → ✅ "Best wishes" / "Kind regards"<br>
            ❌ "ASAP" to a client → ✅ "as soon as you can" or, better, a real date.<br><br>
            And avoid "Dear Sir or Madam" if you know (or can find) the person's name.</span>
          </div>
          <div class="tip-box" style="margin-top:12px">🌍 <span style="flex:1;min-width:0"><b>Elsewhere:</b> American emails tend to be shorter and more upbeat ("Hi Helen, / Best,"), and "Cheers" is rarely used. German and many Central European companies keep "Dear Mr/Ms + surname" much longer. In many Asian cultures, a longer relationship-building opening is expected before the request. Response-time expectations differ too: in the UK, replying within one working day is normal courtesy.</span></div>'''
    },
    "compare": {
        "title": "Too blunt, too stiff, or just right?",
        "instruction": "Hover over (or tap) each version to see how a British reader is likely to hear it.",
        "items": [
            {"key": "c1", "label": "Too blunt", "text": "Why haven't you answered my email?", "explain": "An accusation. The reader will feel defensive and may reply even more slowly."},
            {"key": "c2", "label": "Too stiff", "text": "I humbly take the liberty of reminding you of my previous correspondence.", "explain": "Sounds like a 19th-century letter, or like passive-aggressive sarcasm."},
            {"key": "c3", "label": "Just right", "text": "Just following up on my email below — any update on the figures?", "explain": "Assumes they're busy, restates the one thing you need, and is easy to answer.", "groupEnd": True},
            {"key": "c4", "label": "Too blunt", "text": "I didn't have time to answer before.", "explain": "True, maybe, but it sounds like they weren't a priority."},
            {"key": "c5", "label": "Too stiff", "text": "Please accept my most profound apologies for this unforgivable delay.", "explain": "Over-apologising makes a small delay sound like a disaster, and it sounds insincere."},
            {"key": "c6", "label": "Just right", "text": "Apologies for the slow reply — it's been a busy week.", "explain": "Short, sincere, one light reason, then straight on to the answer."},
        ]
    },
    "reading": {
        "heading": "The Email That Waited",
        "passage_paragraphs": [
            f'''Agnieszka, a project manager in a Birmingham engineering firm, had a supplier who never answered her emails on time. After two weeks of silence she wrote, \"I am still waiting for your answer. Please reply ASAP.\" The reply came within an hour, and it was noticeably cold. What she had meant as {vocab("persistence","persistence")} had come across as a reprimand.''',
            f'''Her British colleague Dan showed her his own version of a chaser: {gram("g1","“Just following up on my email below — any news on the delivery date?”")} It says the same thing, but it quietly assumes that the other person is busy, not lazy. For a second reminder he might write {gram("g2","“Just bumping this to the top of your inbox”")}, a slightly playful line that makes a {vocab("nudge","nudge")} feel friendly rather than {vocab("passive-aggressive","passive-aggressive")}.''',
            f'''Dan's other rule was about tone at the edges of an email. People {vocab("skim","skim")} the middle, he said, but they notice the greeting and the sign-off. He opened new client emails with \"Dear\" and closed them with {gram("g3","“Kind regards”")}, then relaxed to \"Hi\" and \"Best wishes\" once the client did. When he was late replying, he didn't write a paragraph of excuses. He wrote {gram("g4","“Apologies for the slow reply”")} and answered the question in the next line.''',
            f'''Chat tools have their own {vocab("etiquette","etiquette")}. On the team's Slack, Agnieszka used to send \"Hi\" and wait for a response before asking her question, which left colleagues feeling {vocab("put on the spot","put on the spot")}. Now she writes {gram("g5","“Hi Mark — quick one: is the deck final?”")} in a single message. And when a 40-person email arrived asking for comments, she resisted the urge to reply all. Her one-line \"Thanks, looks good\" went only to the sender, which saved 39 people a {vocab("notification","notification")} and made her look quietly professional.''',
        ],
        "comprehension": [
            {"prompt": "Why did the supplier reply coldly to Agnieszka's first chaser?", "options": [
                {"label": "It sounded like a telling-off rather than a reminder.", "value": "right", "correct": True},
                {"label": "It was sent to the wrong person.", "value": "wrong", "correct": False}]},
            {"prompt": "According to Dan, which parts of an email do people really notice?", "options": [
                {"label": "The greeting and the sign-off.", "value": "right", "correct": True},
                {"label": "The subject line only.", "value": "wrong", "correct": False}]},
            {"prompt": "What did Agnieszka change about how she uses Slack?", "options": [
                {"label": "She puts the greeting and the question in one message.", "value": "right", "correct": True},
                {"label": "She stopped using greetings altogether.", "value": "wrong", "correct": False}]},
        ],
        "vocab_data": {
            "persistence": {"word": "persistence", "ipa": "/pəˈsɪs.təns/", "meaning": "continuing to try to do something even when it's difficult", "example": "Her persistence finally got the supplier to reply."},
            "nudge": {"word": "nudge", "ipa": "/nʌdʒ/", "meaning": "a gentle reminder or push to get someone to do something", "example": "I'll give him a nudge if he hasn't replied by Friday."},
            "passive-aggressive": {"word": "passive-aggressive", "ipa": "/ˌpæs.ɪv.əˈɡres.ɪv/", "meaning": "showing annoyance indirectly instead of saying it openly", "example": "\"As per my last email\" can sound very passive-aggressive."},
            "skim": {"word": "skim", "ipa": "/skɪm/", "meaning": "to read something quickly to get the main idea", "example": "Most people skim long emails on their phones."},
            "etiquette": {"word": "etiquette", "ipa": "/ˈet.ɪ.ket/", "meaning": "the accepted rules of polite behaviour in a particular group or situation", "example": "Every team has its own email etiquette."},
            "put on the spot": {"word": "put on the spot", "ipa": "/pʊt ɒn ðə spɒt/", "meaning": "to put someone in a difficult position where they have to respond immediately", "example": "Don't put new colleagues on the spot in big meetings."},
            "notification": {"word": "notification", "ipa": "/ˌnəʊ.tɪ.fɪˈkeɪ.ʃən/", "meaning": "an alert that tells you a new message or event has arrived", "example": "I turn off notifications when I need to focus."},
        },
        "gram_explanations": {
            "g1": "The standard polite chaser. \"Just\" makes it light, \"below\" points to the original, and the question is specific and easy to answer.",
            "g2": "An informal second chase. The mild humour keeps it friendly. Best with colleagues or clients you know well.",
            "g3": "The safest professional sign-off in British English. Neutral, polite, never wrong in a first email.",
            "g4": "A short apology, then straight on to the answer. More professional than long explanations of why you were late.",
            "g5": "Greeting + context + question in one message. The reader can answer immediately, whenever they see it.",
        },
    },
    "vocab_check": {
        "match": [
            {"prompt": "A \"nudge\" in an email is…", "options": [{"label": "a gentle reminder", "value": "right", "correct": True}, {"label": "a formal complaint", "value": "wrong", "correct": False}, {"label": "an attachment", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Passive-aggressive\" behaviour means…", "options": [{"label": "showing annoyance indirectly", "value": "right", "correct": True}, {"label": "being openly angry", "value": "wrong", "correct": False}, {"label": "being too shy to reply", "value": "wrong2", "correct": False}]},
            {"prompt": "If you \"skim\" an email, you…", "options": [{"label": "read it quickly for the main idea", "value": "right", "correct": True}, {"label": "delete it without reading", "value": "wrong", "correct": False}, {"label": "forward it to someone else", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Etiquette\" is…", "options": [{"label": "the accepted rules of polite behaviour", "value": "right", "correct": True}, {"label": "a type of email label", "value": "wrong", "correct": False}, {"label": "a company's legal policy", "value": "wrong2", "correct": False}]},
            {"prompt": "If someone \"puts you on the spot\", they…", "options": [{"label": "force you to respond immediately, in an awkward position", "value": "right", "correct": True}, {"label": "give you a promotion", "value": "wrong", "correct": False}, {"label": "invite you to a meeting", "value": "wrong2", "correct": False}]},
        ],
        "gapfill": [
            {"before": "Her", "after": "paid off: after five emails, the invoice was finally paid.", "answers": ["persistence"], "width": 120},
            {"before": "I turned off my email", "after": "so I could concentrate.", "answers": ["notifications"], "width": 130},
            {"before": "Most people only", "after": "long emails on their phones.", "answers": ["skim"], "width": 90},
            {"before": "I'll give him a gentle", "after": "if he doesn't reply by Friday.", "answers": ["nudge", "reminder"], "width": 100},
        ],
    },
    "practice": {
        "gapfill_focus": "email and chat phrases (one word per gap)",
        "gapfill": [
            {"before": "Just", "after": "up on my email below — any news?", "answers": ["following"], "width": 110},
            {"before": "Apologies for the slow", "after": "— it's been a busy week.", "answers": ["reply", "response"], "width": 100},
            {"before": "I look forward to", "after": "from you.", "answers": ["hearing"], "width": 100},
            {"before": "Please", "after": "attached the updated contract.", "answers": ["find"], "width": 80},
            {"before": "Just to", "after": "— did you mean March or April?", "answers": ["clarify", "check", "confirm"], "width": 100},
            {"before": "No", "after": ", but it'd be great to have this by Friday.", "answers": ["rush", "pressure"], "width": 90},
        ],
        "second": {
            "type": "errorspot", "title": "Spot the faux pas",
            "instruction": "Each line from an email is grammatically correct but wrong for a British reader. Tap the word that causes the problem.",
            "items": [
                {"words": ["Respected", "Mr", "Jones,", "I", "am", "writing", "about", "the", "invoice."], "error_indices": [0], "explanation": "\"Respected\" is a calque of Polish \"Szanowny\". In English, write \"Dear Mr Jones,\"."},
                {"words": ["I", "am", "still", "waiting", "for", "your", "answer."], "error_indices": [2], "explanation": "\"Still waiting\" sounds like a complaint. Use \"Just following up on my email below\" or \"I look forward to hearing from you.\""},
                {"words": ["Please", "send", "the", "contract", "ASAP."], "error_indices": [4], "explanation": "\"ASAP\" reads as impatient, especially to clients. Give a real date: \"Could you send the contract by Thursday?\""},
            ],
        },
        "builders": [
            {"words": ["Just", "following", "up", "on", "my", "email", "below."]},
            {"words": ["Apologies", "for", "the", "slow", "reply."]},
            {"words": ["I", "look", "forward", "to", "hearing", "from", "you."]},
        ],
    },
    "speaking": {
        "solo_text": "Talk through (out loud) how you'd write three short emails: a first contact with a client you've never met, a polite chaser to a colleague who hasn't replied for a week, and an apology for sending the wrong attachment. Say the greeting, the key line and the sign-off for each.",
        "group_questions": [
            "What's the most annoying email or chat habit you've come across at work? What would you ask people to do instead?",
            "Compare email style in your country with the British style in this lesson. What's different about greetings, sign-offs and chasing?",
            "Role-play on \"Slack\": one person sends messages out loud; the others judge whether each one would get a quick, friendly reply.",
        ],
    },
    "listening": {
        "intro": "Anna catches Tomasz just before he hits send on a reply to a company-wide email.",
        "dialogue": [
            {"speaker": "Anna", "line": "Wait, wait — are you replying all to the office move email?"},
            {"speaker": "Tomasz", "line": "Yes, I just want to ask if I can keep my monitor."},
            {"speaker": "Anna", "line": "That's going to two hundred people. Just reply to Sarah in facilities."},
            {"speaker": "Tomasz", "line": "Good point. Also, the supplier still hasn't answered me. I was going to write \"I am still waiting for your answer.\""},
            {"speaker": "Anna", "line": "Softer. \"Just following up on my email below — any news on the delivery date?\""},
            {"speaker": "Tomasz", "line": "And if they ignore that one too?"},
            {"speaker": "Anna", "line": "Then you pick up the phone. Two emails, then a call. That's my rule."},
            {"speaker": "Tomasz", "line": "Two emails, then a call. Got it."},
        ],
        "comprehension": [
            {"prompt": "Why does Anna stop Tomasz replying all?", "options": [{"label": "His question is only for one person, but the email went to 200.", "value": "right", "correct": True}, {"label": "The office move has been cancelled.", "value": "wrong", "correct": False}]},
            {"prompt": "What chaser does Anna suggest?", "options": [{"label": "\"Just following up on my email below — any news on the delivery date?\"", "value": "right", "correct": True}, {"label": "\"Please reply as soon as possible.\"", "value": "wrong", "correct": False}]},
            {"prompt": "What is Anna's rule for unanswered emails?", "options": [{"label": "Two emails, then a phone call.", "value": "right", "correct": True}, {"label": "Keep emailing every day until they reply.", "value": "wrong", "correct": False}]},
        ],
    },
    "exit": [
        {"prompt": "A first email to a new client should open with…", "options": [{"label": "\"Dear Ms Novak,\"", "value": "right", "correct": True}, {"label": "\"Hey there!\"", "value": "wrong", "correct": False}]},
        {"prompt": "The most natural polite chaser is…", "options": [{"label": "\"Just following up on this.\"", "value": "right", "correct": True}, {"label": "\"Why no answer?\"", "value": "wrong", "correct": False}]},
        {"prompt": "\"Czekam na odpowiedź\" is best translated as…", "options": [{"label": "\"I look forward to hearing from you.\"", "value": "right", "correct": True}, {"label": "\"I am waiting for your answer.\"", "value": "wrong", "correct": False}]},
        {"prompt": "In a team chat, the best first message is…", "options": [{"label": "\"Hi Ola — quick question: are we still on for 3pm?\"", "value": "right", "correct": True}, {"label": "\"Hi\"", "value": "wrong", "correct": False}]},
        {"prompt": "\"Cheers\" as a sign-off is best for…", "options": [{"label": "colleagues you know well", "value": "right", "correct": True}, {"label": "a first email to a senior client", "value": "wrong", "correct": False}]},
    ],
})

# ============================================================
# LESSON 4 — Meetings and calls
# ============================================================
LESSONS.append({
    "id": "weq-lesson-04-meetings-calls",
    "num": 4, "section_name": SECTION_NAME, "theme_class": THEME,
    "title": "Meetings & Calls",
    "subtitle": "Getting a word in, disagreeing without damage, keeping things on track — in the room and on video.",
    "warmup_intro": "In British meetings, what you say matters, but so does how you get the floor and how you disagree. People who are silent can seem uninterested, and people who interrupt bluntly can seem aggressive. The space in between is a set of fairly simple phrases.",
    "warmup": [
        {"prompt": "You want to add a point while a colleague is still speaking. You say…",
         "options": [{"label": "\"Sorry to jump in — can I just add something?\"", "value": "right", "correct": True},
                     {"label": "\"Stop, I want to say something.\"", "value": "wrong", "correct": False}]},
        {"prompt": "At the end of a meeting, someone says \"Let's take that away and think about it.\" This often means…",
         "options": [{"label": "No decision today, and possibly not ever", "value": "right", "correct": True},
                     {"label": "The idea has been approved", "value": "wrong", "correct": False}]},
        {"prompt": "On a video call, the host has been talking for 10 seconds without sound. You say…",
         "options": [{"label": "\"Sorry, Mark — I think you're on mute.\"", "value": "right", "correct": True},
                     {"label": "Nothing. It would be rude to interrupt.", "value": "wrong", "correct": False}]},
    ],
    "warmup_tip": "Apologise briefly to get the floor (\"Sorry to jump in\"), acknowledge before disagreeing (\"I take your point, but…\"), and use \"we\" to steer (\"Shall we come back to that?\"). Silence in a British meeting is rarely read as agreement; it's more often read as having nothing to say.",
    "diagnostic": [
        {"prompt": "You disagree with your manager's plan in a meeting. The best way in is…",
         "options": [{"label": "\"I take your point, but I'm a bit worried about the timeline.\"", "value": "right", "correct": True},
                     {"label": "\"This plan won't work.\"", "value": "wrong", "correct": False}]},
        {"prompt": "The discussion has drifted off topic. As chair, you say…",
         "options": [{"label": "\"Good point — shall we park that and come back to it at the end?\"", "value": "right", "correct": True},
                     {"label": "\"That's not relevant. Next.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Someone interrupts you before you've finished. You say…",
         "options": [{"label": "\"If I could just finish the point…\"", "value": "right", "correct": True},
                     {"label": "\"Don't interrupt me.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A quiet colleague hasn't said anything. To include her, you say…",
         "options": [{"label": "\"Ola, you worked on this last year — what's your take?\"", "value": "right", "correct": True},
                     {"label": "\"Ola, why aren't you saying anything?\"", "value": "wrong", "correct": False}]},
    ],
    "widget": {
        "heading": "Three meeting skills",
        "intro": "Three skills make you effective in a meeting: <b>getting the floor</b> (and keeping it), <b>disagreeing diplomatically</b>, and <b>keeping things on track</b>, which isn't only the chair's job. Browse each, then try the quick check.",
        "tabs": [{"key": "floor", "label": "Getting the floor"}, {"key": "dis", "label": "Disagreeing"}, {"key": "track", "label": "Keeping on track"}, {"key": "quiz", "label": "Quick check"}],
        "categories": {
            "floor": [
                {"label": "\"Sorry to jump in, but…\"", "example": "The standard polite interruption. A quick apology buys you the right to speak."},
                {"label": "\"Can I just come in here?\"", "example": "Asks for the floor at a natural pause. \"Just\" makes it brief."},
                {"label": "\"If I could just finish the point…\"", "example": "Politely keeping the floor when someone interrupts you."},
                {"label": "\"Building on what Sam said…\"", "example": "Joining the conversation by connecting to someone else's point. It sounds collaborative, not competitive."},
            ],
            "dis": [
                {"label": "\"I take your point, but…\"", "example": "Acknowledge first, then disagree. The \"but\" still carries the message."},
                {"label": "\"I'm a bit worried about…\"", "example": "Presents your disagreement as a concern about the plan, not an attack on the person."},
                {"label": "\"Could I play devil's advocate for a moment?\"", "example": "Lets you raise objections while signalling it isn't personal."},
                {"label": "\"I see it slightly differently.\"", "example": "\"Slightly\" softens a disagreement that may be quite big."},
            ],
            "track": [
                {"label": "\"Shall we park that and come back to it at the end?\"", "example": "Politely postpones an off-topic discussion. \"Park\" is very common in British meetings."},
                {"label": "\"Just conscious of time — shall we move on?\"", "example": "\"Conscious of time\" is the polite British way to say \"we're running late\"."},
                {"label": "\"So, just to recap: …\"", "example": "Summarises decisions. Whoever recaps usually shapes what people remember."},
                {"label": "\"Who's going to pick that up?\"", "example": "Turns discussion into action by asking for an owner."},
            ],
        },
        "quiz_labels": {"floor": "getting the floor", "dis": "disagreeing", "track": "keeping on track"},
        "rules_html": '''
          <div class="formula" style="border-left-color:var(--c-present)">✅ <b>Get the floor:</b> short apology + "just" + your point. "Sorry to jump in — just a quick one on the budget." Then keep it short.</div>
          <div class="formula" style="border-left-color:var(--c-continuous)">✅ <b>Disagree:</b> acknowledge → concern → suggestion. "I take your point. I'm a bit worried about the timeline. Could we look at a phased launch?"</div>
          <div class="formula" style="border-left-color:var(--c-future);margin-bottom:20px">✅ <b>Keep on track:</b> park it, be conscious of time, recap, and name an owner. Use "we" and "shall we" so steering sounds shared.</div>
          <div class="warn-box">
            <span>🎯</span>
            <span style="flex:1;min-width:0"><b>The tricky part for Polish speakers:</b> two opposite risks.<br><br>
            <b>Too direct:</b> "No, it's not true" / "You are wrong" (<i>To nieprawda</i>) sounds hostile in a British meeting. → "I'm not sure that's quite the case."<br>
            <b>Too quiet:</b> waiting to be asked, or waiting until you've formed a perfect sentence. British meetings reward people who come in early with a short point. "Can I just add something?" is enough to start.<br><br>
            Also decode the British "maybe": "Let's take that away", "We'll bear that in mind" and "That's worth thinking about" often mean no decision, or no.</span>
          </div>
          <div class="tip-box" style="margin-top:12px">🌍 <span style="flex:1;min-width:0"><b>Elsewhere:</b> in American meetings people often interrupt more freely and speak more confidently about half-formed ideas. In Japan, Finland and parts of Asia, silence and pauses are comfortable and interrupting is rare. Dutch and Israeli colleagues may disagree very directly and see it as honesty. <b>On video:</b> camera on for external calls unless told otherwise; mute when not speaking; say "You're on mute" early and kindly; use the chat or a raised hand to get the floor in big calls.</span></div>'''
    },
    "compare": {
        "title": "Too blunt, too stiff, or just right?",
        "instruction": "Hover over (or tap) each version to see how it lands in a British meeting.",
        "items": [
            {"key": "c1", "label": "Too blunt", "text": "Wait. I want to say something.", "explain": "Sounds like you're overruling the speaker. People will remember the interruption, not your point."},
            {"key": "c2", "label": "Too stiff", "text": "Might I be permitted to offer a brief contribution at this juncture?", "explain": "So formal it sounds like a joke. It also takes longer than just making the point."},
            {"key": "c3", "label": "Just right", "text": "Sorry to jump in — can I just add something on the budget?", "explain": "A short apology, a clear signal, and it tells everyone what your point is about.", "groupEnd": True},
            {"key": "c4", "label": "Too blunt", "text": "This plan won't work.", "explain": "A verdict with no reason and no alternative. It shuts the discussion down."},
            {"key": "c5", "label": "Too stiff", "text": "I would respectfully submit that the proposal may be somewhat suboptimal.", "explain": "So softened and formal that people aren't sure what you actually think."},
            {"key": "c6", "label": "Just right", "text": "I take your point, but I'm a bit worried about the timeline — could we phase it?", "explain": "Acknowledgement, a specific concern and a suggestion. Clear, but nobody loses face."},
        ]
    },
    "reading": {
        "heading": "Why Nobody Heard Ola",
        "passage_paragraphs": [
            f'''Ola was the best analyst on her team in Leeds, and almost nobody in senior management knew it. In the weekly meeting she waited politely for a gap in the conversation, but in a room full of fluent speakers the gap never came. By the time she had put her point into a perfect sentence, the discussion had moved on. Her manager assumed she had nothing to add, and her silence was read as a lack of {vocab("initiative","initiative")}.''',
            f'''A mentor gave her two phrases. The first was {gram("g1","“Sorry to jump in — can I just add something?”")} It felt rude at first, but nobody in the room even noticed. In British meetings a short apology is the normal price of entry. The second was {gram("g2","“Building on what Sam said…”")}, which let her join a discussion by connecting to someone else's idea, so her contribution sounded {vocab("collaborative","collaborative")} rather than competitive.''',
            f'''Disagreeing was harder. Ola's instinct was either to stay silent or to say what she really thought: \"That won't work.\" Her mentor suggested a three-step pattern: acknowledge, raise a concern, offer an alternative. {gram("g3","“I take your point, but I'm a bit worried about the timeline”")} turned a {vocab("confrontation","confrontation")} into a problem the whole group could solve. Within a month, two of her suggestions had been adopted.''',
            f'''She also learnt to {vocab("read the room","read the room")}. When the director said {gram("g4","“Let's take that away and think about it”")}, it usually meant the idea would quietly {vocab("stall","stall")}. And when discussions began to {vocab("drift","drift")}, the person who said {gram("g5","“Shall we park that and come back to it at the end?”")} was usually the one people saw as a future leader. A year later, Ola was chairing the meeting herself. Her final {vocab("recap","recap")} at the end of each one, {gram("g6","“So, just to recap…”")}, became the part everyone waited for.''',
        ],
        "comprehension": [
            {"prompt": "Why was Ola's silence a problem?", "options": [
                {"label": "Her manager thought she had nothing to contribute.", "value": "right", "correct": True},
                {"label": "It made the meetings too long.", "value": "wrong", "correct": False}]},
            {"prompt": "What three-step pattern did her mentor suggest for disagreeing?", "options": [
                {"label": "Acknowledge, raise a concern, offer an alternative.", "value": "right", "correct": True},
                {"label": "Wait, write it down, email it later.", "value": "wrong", "correct": False}]},
            {"prompt": "What did \"Let's take that away and think about it\" usually mean?", "options": [
                {"label": "The idea would probably not go any further.", "value": "right", "correct": True},
                {"label": "The idea was approved and would start soon.", "value": "wrong", "correct": False}]},
        ],
        "vocab_data": {
            "initiative": {"word": "initiative", "ipa": "/ɪˈnɪʃ.ə.tɪv/", "meaning": "the ability to act and make decisions without being told what to do", "example": "She showed real initiative by fixing the problem herself."},
            "collaborative": {"word": "collaborative", "ipa": "/kəˈlæb.ər.ə.tɪv/", "meaning": "involving people working together", "example": "It was a very collaborative project."},
            "confrontation": {"word": "confrontation", "ipa": "/ˌkɒn.frʌnˈteɪ.ʃən/", "meaning": "an angry disagreement or argument", "example": "He avoids confrontation at all costs."},
            "read the room": {"word": "read the room", "ipa": "/riːd ðə ruːm/", "meaning": "to understand the mood and attitudes of the people around you", "example": "He didn't read the room and told a joke at the wrong moment."},
            "stall": {"word": "stall", "ipa": "/stɔːl/", "meaning": "to stop making progress", "example": "The project stalled when the budget was cut."},
            "drift": {"word": "drift", "ipa": "/drɪft/", "meaning": "to move slowly away from the main subject or purpose", "example": "The conversation drifted to last night's football."},
            "recap": {"word": "recap", "ipa": "/ˈriː.kæp/", "meaning": "a short summary of the main points", "example": "Can you give us a quick recap of the decisions?"},
        },
        "gram_explanations": {
            "g1": "The polite interruption: short apology + \"just\" + a question. It takes two seconds and nobody minds.",
            "g2": "Joining by connecting. It shows you were listening and makes your point sound like teamwork.",
            "g3": "Acknowledge (\"I take your point\") + concern (\"I'm a bit worried\"). The disagreement is clear but it's about the plan, not the person.",
            "g4": "British meeting code. Often means \"not now, maybe not ever\". If you care about the idea, ask for a date to revisit it.",
            "g5": "Steering with \"shall we\" and \"park\". It postpones the topic without dismissing the person who raised it.",
            "g6": "The recap. Whoever summarises the meeting shapes what everyone remembers and does next.",
        },
    },
    "vocab_check": {
        "match": [
            {"prompt": "If a project \"stalls\", it…", "options": [{"label": "stops making progress", "value": "right", "correct": True}, {"label": "is finished early", "value": "wrong", "correct": False}, {"label": "gets more funding", "value": "wrong2", "correct": False}]},
            {"prompt": "A \"recap\" is…", "options": [{"label": "a short summary of the main points", "value": "right", "correct": True}, {"label": "a second meeting", "value": "wrong", "correct": False}, {"label": "a formal apology", "value": "wrong2", "correct": False}]},
            {"prompt": "To \"read the room\" means to…", "options": [{"label": "understand the mood of the people around you", "value": "right", "correct": True}, {"label": "read the meeting agenda aloud", "value": "wrong", "correct": False}, {"label": "book a meeting room", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Initiative\" is…", "options": [{"label": "the ability to act without being told", "value": "right", "correct": True}, {"label": "a meeting at the start of a project", "value": "wrong", "correct": False}, {"label": "a type of disagreement", "value": "wrong2", "correct": False}]},
            {"prompt": "A \"confrontation\" is…", "options": [{"label": "an angry disagreement", "value": "right", "correct": True}, {"label": "a friendly discussion", "value": "wrong", "correct": False}, {"label": "a confirmation email", "value": "wrong2", "correct": False}]},
        ],
        "gapfill": [
            {"before": "The conversation began to", "after": "towards holiday plans.", "answers": ["drift"], "width": 90},
            {"before": "It was a genuinely", "after": "effort — everyone contributed.", "answers": ["collaborative"], "width": 140},
            {"before": "He hates", "after": ", so he agrees with everyone.", "answers": ["confrontation", "conflict"], "width": 140},
            {"before": "Could you give us a quick", "after": "of what we decided?", "answers": ["recap", "summary"], "width": 100},
        ],
    },
    "practice": {
        "gapfill_focus": "meeting phrases (one word per gap)",
        "gapfill": [
            {"before": "Sorry to", "after": "in, but can I add something?", "answers": ["jump", "butt", "cut"], "width": 90},
            {"before": "I take your", "after": ", but I'm worried about the cost.", "answers": ["point"], "width": 90},
            {"before": "Shall we", "after": "that and come back to it later?", "answers": ["park"], "width": 90},
            {"before": "Just", "after": "of time — shall we move on?", "answers": ["conscious", "mindful"], "width": 110},
            {"before": "If I could just", "after": "the point…", "answers": ["finish"], "width": 90},
            {"before": "So, just to", "after": ": Anna owns the budget, and we meet again on Friday.", "answers": ["recap", "summarise", "summarize"], "width": 100},
        ],
        "second": {
            "type": "errorspot", "title": "Spot the faux pas",
            "instruction": "Each line would sound wrong in a British meeting. Tap the word that causes the problem.",
            "items": [
                {"words": ["No,", "that's", "not", "true,", "the", "numbers", "are", "different."], "error_indices": [3], "explanation": "\"Not true\" sounds like you're calling the speaker a liar. Try \"I'm not sure that's quite right — my numbers are slightly different.\""},
                {"words": ["Ola,", "why", "are", "you", "so", "quiet", "today?"], "error_indices": [5], "explanation": "Commenting on someone's silence puts them on the spot. Invite them in instead: \"Ola, what's your take on this?\""},
                {"words": ["Stop,", "this", "is", "off", "topic."], "error_indices": [0], "explanation": "Too commanding. \"Good point — shall we park that and come back to it?\" steers without dismissing anyone."},
            ],
        },
        "builders": [
            {"words": ["Sorry", "to", "jump", "in,", "but", "can", "I", "add", "something?"]},
            {"words": ["Shall", "we", "park", "that", "for", "now?"]},
            {"words": ["I", "take", "your", "point,", "but", "I'm", "a", "bit", "worried."]},
        ],
    },
    "speaking": {
        "solo_text": "Imagine your manager proposes moving a big launch forward by a month. In 60 seconds, disagree diplomatically: acknowledge the idea, raise one or two concerns, and suggest an alternative. Then close with a short recap sentence.",
        "group_questions": [
            "Role-play a 3-minute meeting about planning the team's Christmas party. One person chairs; the others must interrupt politely at least once, disagree once, and one person keeps drifting off topic.",
            "In your culture, is interrupting rude, normal, or a sign of engagement? How about silence?",
            "What makes a video call go well or badly? Share one rule you'd like everyone at work to follow.",
        ],
    },
    "listening": {
        "intro": "After a project meeting, Anna gives Tomasz some feedback on how it went.",
        "dialogue": [
            {"speaker": "Anna", "line": "You were very quiet in there. You had views on the timeline, didn't you?"},
            {"speaker": "Tomasz", "line": "I did, but everyone was talking at once. I was waiting for a pause."},
            {"speaker": "Anna", "line": "There's never a pause. You just say \"Sorry to jump in\" and go."},
            {"speaker": "Tomasz", "line": "And when Mark said the launch date was fixed, I wanted to say \"That's not realistic.\""},
            {"speaker": "Anna", "line": "Try \"I take your point, but I'm a bit worried about the testing time.\" Same message, less smoke."},
            {"speaker": "Tomasz", "line": "Less smoke. I like that. And what did Mark mean by \"let's take that away\"?"},
            {"speaker": "Anna", "line": "Usually it means \"not today\". If you care about it, email him tomorrow and suggest a date to revisit it."},
            {"speaker": "Tomasz", "line": "OK. Next meeting, I'm jumping in at least once."},
        ],
        "comprehension": [
            {"prompt": "Why didn't Tomasz speak in the meeting?", "options": [{"label": "He was waiting for a pause that never came.", "value": "right", "correct": True}, {"label": "He didn't have an opinion on the timeline.", "value": "wrong", "correct": False}]},
            {"prompt": "What does Anna suggest instead of \"That's not realistic\"?", "options": [{"label": "\"I take your point, but I'm a bit worried about the testing time.\"", "value": "right", "correct": True}, {"label": "Saying nothing and emailing Mark later.", "value": "wrong", "correct": False}]},
            {"prompt": "What does Anna advise about \"let's take that away\"?", "options": [{"label": "Follow up and suggest a date to revisit it.", "value": "right", "correct": True}, {"label": "Assume the idea has been approved.", "value": "wrong", "correct": False}]},
        ],
    },
    "exit": [
        {"prompt": "The politest way to interrupt is…", "options": [{"label": "\"Sorry to jump in — can I just add something?\"", "value": "right", "correct": True}, {"label": "\"Wait, listen to me.\"", "value": "wrong", "correct": False}]},
        {"prompt": "\"Shall we park that?\" means…", "options": [{"label": "Let's discuss it later.", "value": "right", "correct": True}, {"label": "Let's go outside.", "value": "wrong", "correct": False}]},
        {"prompt": "Which is a diplomatic disagreement?", "options": [{"label": "\"I see it slightly differently.\"", "value": "right", "correct": True}, {"label": "\"You're wrong about this.\"", "value": "wrong", "correct": False}]},
        {"prompt": "\"Just conscious of time\" signals that…", "options": [{"label": "the meeting is running late", "value": "right", "correct": True}, {"label": "someone has arrived late", "value": "wrong", "correct": False}]},
        {"prompt": "On a video call, someone has been talking on mute. You…", "options": [{"label": "tell them kindly and quickly", "value": "right", "correct": True}, {"label": "wait until they notice", "value": "wrong", "correct": False}]},
    ],
})

# ============================================================
# LESSON 5 — Difficult conversations
# ============================================================
LESSONS.append({
    "id": "weq-lesson-05-difficult-conversations",
    "num": 5, "section_name": SECTION_NAME, "theme_class": THEME,
    "title": "Difficult Conversations",
    "subtitle": "Saying no, apologising properly, and giving (and receiving) feedback without damaging the relationship.",
    "warmup_intro": "Everyone avoids the same conversations: saying no to a request, admitting a mistake, telling a colleague their work isn't good enough. The British way of handling them is to be clear about the message and generous about the person. Let's see where your instincts are.",
    "warmup": [
        {"prompt": "Your manager asks you to take on another project, but you're overloaded. You say…",
         "options": [{"label": "\"I'd love to help, but I'm at capacity until the audit's done. Could we look at it in May?\"", "value": "right", "correct": True},
                     {"label": "\"No, I can't. I have too much work.\"", "value": "wrong", "correct": False}]},
        {"prompt": "You sent a client the wrong figures. The best first line is…",
         "options": [{"label": "\"I'm sorry — I sent you the wrong figures. The correct ones are attached.\"", "value": "right", "correct": True},
                     {"label": "\"There was a problem with the system, so the figures were wrong.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A British colleague says your report has \"a few small things to tweak\". You should…",
         "options": [{"label": "ask which points matter most, as they may be bigger than they sound", "value": "right", "correct": True},
                     {"label": "assume it's basically finished", "value": "wrong", "correct": False}]},
    ],
    "warmup_tip": "A good \"no\" includes a reason and an alternative. A good apology owns the mistake before it explains it. Good feedback is specific, and British feedback is often more serious than it sounds.",
    "diagnostic": [
        {"prompt": "Which is the most constructive feedback?",
         "options": [{"label": "\"The analysis is strong. The summary could be shorter — maybe one page?\"", "value": "right", "correct": True},
                     {"label": "\"The summary is bad.\"", "value": "wrong", "correct": False}]},
        {"prompt": "Someone gives you critical feedback. The best first response is…",
         "options": [{"label": "\"Thanks, that's really useful. Can you give me an example?\"", "value": "right", "correct": True},
                     {"label": "\"That's not fair — I didn't have enough time.\"", "value": "wrong", "correct": False}]},
        {"prompt": "You need to tell a client their deadline can't be met. You start with…",
         "options": [{"label": "\"I'm afraid we won't be able to deliver by the 10th.\"", "value": "right", "correct": True},
                     {"label": "\"Unfortunately it is impossible.\"", "value": "wrong", "correct": False}]},
        {"prompt": "A colleague apologises to you for a small delay. You say…",
         "options": [{"label": "\"No worries at all.\"", "value": "right", "correct": True},
                     {"label": "\"OK, but don't do it again.\"", "value": "wrong", "correct": False}]},
    ],
    "widget": {
        "heading": "Three difficult conversations",
        "intro": "Three conversations cause most of the tension at work: <b>saying no</b>, <b>apologising</b> when you've got something wrong, and <b>giving feedback</b> someone may not want to hear. Browse the phrases for each, then try the quick check.",
        "tabs": [{"key": "no", "label": "Saying no"}, {"key": "sorry", "label": "Apologising"}, {"key": "fb", "label": "Giving feedback"}, {"key": "quiz", "label": "Quick check"}],
        "categories": {
            "no": [
                {"label": "\"I'd love to, but I'm at capacity right now.\"", "example": "A warm \"no\" with a reason. \"At capacity\" is a professional way to say \"too busy\"."},
                {"label": "\"I'm afraid that won't be possible by Friday — could we say Wednesday?\"", "example": "\"I'm afraid\" softens bad news; the alternative keeps the conversation going."},
                {"label": "\"Let me check my priorities with Claire and come back to you.\"", "example": "Buys time and brings in the person who sets your workload."},
                {"label": "\"I'm not the best person for this, but Sam might be.\"", "example": "Declining by redirecting. Only do it if Sam really is a good fit."},
            ],
            "sorry": [
                {"label": "\"That's my mistake — I'll fix it today.\"", "example": "Owns it and gives a next step. Short apologies sound more confident than long ones."},
                {"label": "\"I'm sorry, I should have checked the figures.\"", "example": "\"Should have\" admits what you did wrong without drama."},
                {"label": "\"Thanks for flagging it.\"", "example": "When someone points out your mistake, thank them. It turns criticism into teamwork."},
                {"label": "\"No worries at all.\"", "example": "Accepting someone else's apology for something small. Generous and very British."},
            ],
            "fb": [
                {"label": "\"What worked really well was…\"", "example": "Start with something specific and genuine, not a generic \"Great job\"."},
                {"label": "\"One thing I'd suggest is…\"", "example": "Frames criticism as a suggestion. Clear, but not a command."},
                {"label": "\"I wonder if the intro could be a bit shorter.\"", "example": "\"I wonder if\" + \"a bit\" softens the point, but it's still a clear request to change it."},
                {"label": "\"How do you feel it went?\"", "example": "Asking for their view first. People accept feedback more easily when they've named the problem themselves."},
            ],
        },
        "quiz_labels": {"no": "saying no", "sorry": "apologising", "fb": "giving feedback"},
        "rules_html": '''
          <div class="formula" style="border-left-color:var(--c-present)">✅ <b>Saying no:</b> warm start + reason + alternative. "I'd love to, but I'm at capacity until the 15th — could I help with the next one instead?"</div>
          <div class="formula" style="border-left-color:var(--c-continuous)">✅ <b>Apologising:</b> own it → fix it → prevent it. "That's my mistake. I've sent the right file. I'll double-check attachments from now on." Keep excuses out of the first sentence.</div>
          <div class="formula" style="border-left-color:var(--c-future);margin-bottom:20px">✅ <b>Feedback:</b> specific positive → one or two specific suggestions → a question. When <i>receiving</i> it: thank, ask for an example, don't defend yourself on the spot.</div>
          <div class="warn-box">
            <span>🎯</span>
            <span style="flex:1;min-width:0"><b>The tricky part for Polish speakers:</b> British "sorry" and Polish <i>przepraszam</i> don't work the same way. British people say sorry constantly for tiny things ("Sorry, can I just squeeze past?"), so leaving it out can sound cold. But for real mistakes, the British expect a <b>short</b> apology that takes responsibility, not a long explanation of whose fault it was.<br><br>
            ❌ "The system didn't save it, and nobody told me the deadline changed." → sounds like blaming.<br>
            ✅ "I'm sorry — I missed the deadline change. I'll have it to you by 3."<br><br>
            When decoding British feedback, remember Lesson 2: "a few minor points" may be serious, and "have you considered…?" often means "you should."</span>
          </div>
          <div class="tip-box" style="margin-top:12px">🌍 <span style="flex:1;min-width:0"><b>Elsewhere:</b> Americans often expect lots of praise around criticism (the "feedback sandwich") and may hear British understatement as approval. Dutch and German colleagues usually give direct, unsoftened feedback and may find the British style evasive. In much of East Asia, criticism in front of others causes serious loss of face, so give it privately. Everywhere, praise in public and criticise in private.</span></div>'''
    },
    "compare": {
        "title": "Too blunt, too stiff, or just right?",
        "instruction": "Hover over (or tap) each version to see how it is likely to land.",
        "items": [
            {"key": "c1", "label": "Too blunt", "text": "No, I don't have time.", "explain": "True, but it closes the door. Your manager hears \"not my problem\"."},
            {"key": "c2", "label": "Too stiff", "text": "I deeply regret that I must decline this most generous opportunity.", "explain": "Over-formal and over-apologetic. It sounds sarcastic or anxious."},
            {"key": "c3", "label": "Just right", "text": "I'd love to help, but I'm at capacity until the audit's done — could we revisit it in May?", "explain": "Warm, honest, specific reason, and a real alternative.", "groupEnd": True},
            {"key": "c4", "label": "Too blunt", "text": "Your presentation was too long and boring.", "explain": "A personal verdict with no specifics. It hurts and gives the person nothing to act on."},
            {"key": "c5", "label": "Too stiff", "text": "It might perhaps possibly be worth considering whether the length could conceivably be revisited.", "explain": "So many softeners that the message disappears. The person may not realise there's a problem at all."},
            {"key": "c6", "label": "Just right", "text": "The data was really clear. One thing I'd suggest is cutting it to 15 minutes — you'd keep the room with you.", "explain": "Specific praise, one clear suggestion, and a reason that's about their success."},
        ]
    },
    "reading": {
        "heading": "Three Sentences That Saved a Contract",
        "passage_paragraphs": [
            f'''When Kamil discovered that his team had sent a major client the wrong pricing, his first instinct was to explain. His draft email began with a long paragraph about a spreadsheet error, a colleague who had been off sick and a system update. His manager read it and deleted almost all of it. \"They don't want the story,\" she said. \"They want to know that you know, and that it's fixed.\"''',
            f'''The email they finally sent was three sentences long. It began {gram("g1","“I'm sorry — we sent you the wrong pricing on Tuesday, and that's our mistake.”")} The second sentence gave the correct figures; the third explained what would stop it happening again. The client's reply was two words: {gram("g2","“No worries.”")} What could have become a {vocab("dispute","dispute")} was over in an afternoon, because the apology was {vocab("accountable","accountable")} rather than {vocab("defensive","defensive")}.''',
            f'''The same manager taught Kamil how to say no. When the sales director asked him to add a new feature two weeks before launch, Kamil's honest answer was \"impossible\": the team was already {vocab("at capacity","at capacity")}. Instead of saying so bluntly, he said {gram("g3","“I'd love to, but we're flat out until launch — could we look at it for the June release?”")} The director agreed at once. A refusal with a reason and an {vocab("alternative","alternative")} feels like a plan; a refusal without one feels like a closed door.''',
            f'''Feedback was the hardest skill. Kamil's reviews of junior colleagues' work were accurate but {vocab("harsh","harsh")}, and people had stopped asking for them. He learnt to start with something specific that genuinely worked, then offer {gram("g4","“One thing I'd suggest is…”")} and finish with a question. The content of his feedback barely changed; the way people received it changed completely. And when his own manager criticised him, he practised the hardest phrase of all: {gram("g5","“Thanks, that's really useful — can you give me an example?”")} It is difficult to say when you want to {vocab("justify","justify")} yourself, which is exactly why it impresses people.''',
        ],
        "comprehension": [
            {"prompt": "Why did Kamil's manager delete most of his first email?", "options": [
                {"label": "It explained too much instead of simply owning the mistake.", "value": "right", "correct": True},
                {"label": "It contained the wrong pricing again.", "value": "wrong", "correct": False}]},
            {"prompt": "Why did the sales director accept Kamil's \"no\"?", "options": [
                {"label": "It came with a reason and an alternative date.", "value": "right", "correct": True},
                {"label": "Kamil's manager overruled the director.", "value": "wrong", "correct": False}]},
            {"prompt": "What changed about Kamil's feedback?", "options": [
                {"label": "Mainly how he delivered it, not what he said.", "value": "right", "correct": True},
                {"label": "He stopped mentioning problems at all.", "value": "wrong", "correct": False}]},
        ],
        "vocab_data": {
            "dispute": {"word": "dispute", "ipa": "/dɪˈspjuːt/", "meaning": "a serious disagreement, especially between organisations", "example": "The pricing dispute went on for months."},
            "accountable": {"word": "accountable", "ipa": "/əˈkaʊn.tə.bəl/", "meaning": "accepting responsibility for your actions", "example": "A good leader holds herself accountable."},
            "defensive": {"word": "defensive", "ipa": "/dɪˈfen.sɪv/", "meaning": "reacting to criticism by trying to protect yourself or make excuses", "example": "He gets defensive whenever anyone questions his work."},
            "at capacity": {"word": "at capacity", "ipa": "/æt kəˈpæs.ə.ti/", "meaning": "as busy or as full as possible; unable to take on more", "example": "The team is at capacity until the end of the quarter."},
            "alternative": {"word": "alternative", "ipa": "/ɒlˈtɜː.nə.tɪv/", "meaning": "another possible option", "example": "If Friday doesn't work, is there an alternative?"},
            "harsh": {"word": "harsh", "ipa": "/hɑːʃ/", "meaning": "unkind, severe, or more critical than necessary", "example": "The feedback was fair but a bit harsh."},
            "justify": {"word": "justify", "ipa": "/ˈdʒʌs.tɪ.faɪ/", "meaning": "to give reasons to show that something you did was right", "example": "You don't need to justify every decision."},
        },
        "gram_explanations": {
            "g1": "Own it in the first sentence: \"I'm sorry\" + what happened + \"that's our mistake\". No excuses until the problem is fixed.",
            "g2": "The standard British way to accept an apology for something that's been dealt with. Friendly and final.",
            "g3": "Warm start (\"I'd love to\") + reason (\"flat out\" = extremely busy) + alternative (\"could we…?\"). A no that feels like a plan.",
            "g4": "Frames criticism as a suggestion. It's still a clear request to change something.",
            "g5": "Receiving feedback well: thank, then ask for specifics. It shows confidence and gets you useful detail.",
        },
    },
    "vocab_check": {
        "match": [
            {"prompt": "If someone is \"defensive\", they…", "options": [{"label": "react to criticism by making excuses", "value": "right", "correct": True}, {"label": "protect their team from extra work", "value": "wrong", "correct": False}, {"label": "are very confident", "value": "wrong2", "correct": False}]},
            {"prompt": "\"At capacity\" means…", "options": [{"label": "too busy to take on more", "value": "right", "correct": True}, {"label": "fully qualified", "value": "wrong", "correct": False}, {"label": "about to be promoted", "value": "wrong2", "correct": False}]},
            {"prompt": "An \"accountable\" person…", "options": [{"label": "accepts responsibility for what they do", "value": "right", "correct": True}, {"label": "works in the finance department", "value": "wrong", "correct": False}, {"label": "blames others for mistakes", "value": "wrong2", "correct": False}]},
            {"prompt": "\"Harsh\" feedback is…", "options": [{"label": "more severe or unkind than necessary", "value": "right", "correct": True}, {"label": "detailed and specific", "value": "wrong", "correct": False}, {"label": "delivered in writing", "value": "wrong2", "correct": False}]},
            {"prompt": "A \"dispute\" is…", "options": [{"label": "a serious disagreement", "value": "right", "correct": True}, {"label": "a friendly chat", "value": "wrong", "correct": False}, {"label": "a type of contract", "value": "wrong2", "correct": False}]},
        ],
        "gapfill": [
            {"before": "You don't need to", "after": "every decision you make.", "answers": ["justify", "explain"], "width": 100},
            {"before": "If Tuesday doesn't work, is there an", "after": "?", "answers": ["alternative", "option"], "width": 120},
            {"before": "He always gets", "after": "when someone questions his figures.", "answers": ["defensive", "upset"], "width": 110},
            {"before": "The team is", "after": "capacity until the end of June.", "answers": ["at"], "width": 70},
        ],
    },
    "practice": {
        "gapfill_focus": "phrases for difficult conversations (one word per gap)",
        "gapfill": [
            {"before": "I'm", "after": "that won't be possible by Friday.", "answers": ["afraid"], "width": 90},
            {"before": "That's my", "after": "— I'll fix it today.", "answers": ["mistake", "fault"], "width": 100},
            {"before": "Thanks for", "after": "it — I hadn't noticed.", "answers": ["flagging", "spotting", "mentioning"], "width": 100},
            {"before": "One thing I'd", "after": "is cutting the intro.", "answers": ["suggest"], "width": 100},
            {"before": "No", "after": "at all — it happens.", "answers": ["worries", "problem"], "width": 90},
            {"before": "I should", "after": "checked the figures before sending them.", "answers": ["have"], "width": 70},
        ],
        "second": {
            "type": "errorspot", "title": "Spot the faux pas",
            "instruction": "Each line would damage the relationship. Tap the word that causes the problem.",
            "items": [
                {"words": ["The", "mistake", "happened", "because", "the", "system", "is", "terrible."], "error_indices": [3], "explanation": "Starting with \"because\" turns an apology into an excuse. Own it first: \"I'm sorry — that's my mistake. I've corrected it.\""},
                {"words": ["No,", "I", "can't", "do", "it.", "Ask", "someone", "else."], "error_indices": [5], "explanation": "Pushing the task away sounds dismissive. Give a reason and an alternative: \"I'm at capacity, but Sam might be able to help.\""},
                {"words": ["Your", "presentation", "was", "boring."], "error_indices": [3], "explanation": "A personal verdict gives nothing to act on. Be specific and constructive: \"One thing I'd suggest is adding a real example early on.\""},
            ],
        },
        "builders": [
            {"words": ["I'd", "love", "to,", "but", "I'm", "at", "capacity."]},
            {"words": ["That's", "my", "mistake", "—", "I'll", "fix", "it."]},
            {"words": ["One", "thing", "I'd", "suggest", "is", "cutting", "the", "intro."]},
        ],
    },
    "speaking": {
        "solo_text": "Choose one: (a) say no to your manager's request to work this weekend, with a reason and an alternative; (b) apologise to a client for a missed deadline in three sentences: own it, fix it, prevent it; or (c) give a colleague feedback on a presentation that was far too long.",
        "group_questions": [
            "Role-play: A asks B for a big favour; B says no well. Then swap. Which \"no\" felt most acceptable, and why?",
            "What's the best (or worst) feedback you've ever received at work? What made it effective or damaging?",
            "Is it harder in your culture to say no to a manager, to apologise, or to criticise a colleague? Why?",
        ],
    },
    "listening": {
        "intro": "Tomasz has made a mistake with a client report and asks Anna how to handle it.",
        "dialogue": [
            {"speaker": "Tomasz", "line": "I sent Harris & Co last month's figures instead of this month's. I'm writing an email explaining what happened."},
            {"speaker": "Anna", "line": "How long is the explanation?"},
            {"speaker": "Tomasz", "line": "About a page. The template was wrong, the file names were confusing…"},
            {"speaker": "Anna", "line": "Cut it. Three lines: sorry, that's my mistake; here are the correct figures; I've added a check so it won't happen again."},
            {"speaker": "Tomasz", "line": "Won't they think I'm hiding something if I don't explain?"},
            {"speaker": "Anna", "line": "No. Long explanations sound like excuses. If they want the details, they'll ask."},
            {"speaker": "Tomasz", "line": "And Mark wants me to take over the Leeds project too. I can't, honestly."},
            {"speaker": "Anna", "line": "Then tell him you'd love to, but you're at capacity until the Harris work's done, and suggest a date."},
        ],
        "comprehension": [
            {"prompt": "What does Anna say the apology email should contain?", "options": [{"label": "Owning the mistake, the correct figures and how it won't happen again.", "value": "right", "correct": True}, {"label": "A full page explaining the causes of the error.", "value": "wrong", "correct": False}]},
            {"prompt": "Why does Anna advise against a long explanation?", "options": [{"label": "It sounds like making excuses.", "value": "right", "correct": True}, {"label": "Clients don't read emails longer than one line.", "value": "wrong", "correct": False}]},
            {"prompt": "How should Tomasz say no to the Leeds project?", "options": [{"label": "Say he'd love to, explain he's at capacity, and suggest a date.", "value": "right", "correct": True}, {"label": "Simply tell Mark he can't do it.", "value": "wrong", "correct": False}]},
        ],
    },
    "exit": [
        {"prompt": "The best structure for saying no is…", "options": [{"label": "warm start + reason + alternative", "value": "right", "correct": True}, {"label": "a quick \"no\" so there's no confusion", "value": "wrong", "correct": False}]},
        {"prompt": "A professional apology starts with…", "options": [{"label": "owning the mistake", "value": "right", "correct": True}, {"label": "explaining the causes", "value": "wrong", "correct": False}]},
        {"prompt": "When you receive critical feedback, you say…", "options": [{"label": "\"Thanks — can you give me an example?\"", "value": "right", "correct": True}, {"label": "\"That's not fair.\"", "value": "wrong", "correct": False}]},
        {"prompt": "\"I'm afraid that won't be possible\" is…", "options": [{"label": "a polite way to deliver bad news", "value": "right", "correct": True}, {"label": "a sign that the speaker is scared", "value": "wrong", "correct": False}]},
        {"prompt": "Where should you usually give critical feedback?", "options": [{"label": "In private", "value": "right", "correct": True}, {"label": "In front of the team, so everyone learns", "value": "wrong", "correct": False}]},
    ],
})
