"""
Builds audio-manifest.json: the complete list of audio clips the course
needs, ready for generate_audio.py to turn into real MP3 files.

Architecture note: the original B1+/B2 course's equivalent script
(extract_audio_manifest.js) parsed the vocab/dialogue data back out of
each lesson's embedded inline <script> block using Node's `vm` module,
because that course's content only ever existed as already-generated
HTML. This course's content lives as structured Python data BEFORE it's
ever turned into HTML (lessons_section1.py..lessons_section4.py), so
there's a strictly simpler and more robust option: import that data
directly. No HTML parsing, no risk of the extractor and the generator
drifting apart. Same end artifact (audio-manifest.json), same shape,
simpler path to it.

Two kinds of clips:
  - vocab: one MP3 per unique vocab word across the whole course
    (deduplicated — several lessons may reuse a word), read aloud by a
    single consistent narrator voice. Written to audio/vocab/{slug}.mp3,
    where {slug} is exactly what Course.slugifyForAudio() in
    course-engine.js produces for that word — this must match exactly,
    since that's the filename the browser looks for.
  - dialogue: one combined MP3 per lesson (all of Anna & Tomasz's lines
    stitched together with a short pause between turns), plus a sidecar
    timing JSON so the transcript can highlight the correct line in
    real time as the recording plays. Written to
    audio/{shortPrefix}-listening.mp3 + audio/{shortPrefix}-listening.json.

Run: python3 extract_audio_manifest.py
"""
import json
import re

import lessons_section1 as s1
import lessons_section2 as s2
import lessons_section3 as s3
import lessons_section4 as s4

SECTION_MODULES = [s1, s2, s3, s4]

# Must exactly mirror Course.slugifyForAudio() in shared/course-engine.js:
#   text.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
#     .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
import unicodedata


def slugify_for_audio(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def lesson_short_prefix(lesson_id):
    m = re.match(r"^weq-(lesson-\d+)", lesson_id)
    assert m, f"unexpected lesson id shape: {lesson_id}"
    return m.group(1)


# Voices confirmed for this project (Google Cloud TTS, en-GB Neural2
# lineup) — same assignment as the original B1+/B2 course, since this
# course keeps the same two dialogue speakers. Re-verify these voice
# names are still offered if it's been a long time since this was
# written; Google has occasionally retired specific voices in this family.
VOICE_ANNA = "en-GB-Neural2-A"      # female — dialogue speaker "Anna"
VOICE_TOMASZ = "en-GB-Neural2-B"    # male — dialogue speaker "Tomasz"
VOICE_NARRATOR = "en-GB-Neural2-F"  # female — single vocab-word narrator voice
PAUSE_MS_BETWEEN_TURNS = 450        # stitching pause between dialogue lines


def build_manifest():
    vocab_seen = {}  # slug -> word (first-seen spelling wins; dedup by slug)
    dialogues = []

    for mod in SECTION_MODULES:
        for lesson in mod.LESSONS:
            vocab_data = lesson["reading"]["vocab_data"]
            for entry in vocab_data.values():
                word = entry["word"]
                slug = slugify_for_audio(word)
                if not slug:
                    continue
                vocab_seen.setdefault(slug, word)

            dialogue = lesson["listening"]["dialogue"]
            dialogues.append({
                "lessonId": lesson["id"],
                "shortPrefix": lesson_short_prefix(lesson["id"]),
                "title": lesson["title"],
                "lines": [{"speaker": ln["speaker"], "line": ln["line"]} for ln in dialogue],
            })

    vocab_items = [
        {"slug": slug, "word": word, "voice": VOICE_NARRATOR, "path": f"audio/vocab/{slug}.mp3"}
        for slug, word in sorted(vocab_seen.items())
    ]

    manifest = {
        "voices": {"anna": VOICE_ANNA, "tomasz": VOICE_TOMASZ, "narrator": VOICE_NARRATOR},
        "pauseMsBetweenTurns": PAUSE_MS_BETWEEN_TURNS,
        "vocab": vocab_items,
        "dialogues": dialogues,
    }
    return manifest


def main():
    manifest = build_manifest()
    with open("audio-manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    total_lines = sum(len(d["lines"]) for d in manifest["dialogues"])
    print(f"Wrote audio-manifest.json: {len(manifest['vocab'])} unique vocab words, "
          f"{len(manifest['dialogues'])} dialogues ({total_lines} lines total).")


if __name__ == "__main__":
    main()
