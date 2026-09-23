"""
Generates all real audio for the English+ B2+/C1 Companion Course from
audio-manifest.json (run extract_audio_manifest.py first, or this script
will do it for you if the manifest is missing).

Requires:
    pip install requests pydub
    ffmpeg installed separately and on PATH (pydub shells out to it for
    MP3 encoding/concatenation) — on a Mac: `brew install ffmpeg`.

API key:
    This script reads your Google Cloud Text-to-Speech API key from the
    GOOGLE_TTS_API_KEY environment variable. It deliberately does NOT
    accept the key as a plain command-line argument or read it from any
    file that might get committed — set it in your shell before running:

        export GOOGLE_TTS_API_KEY="your-key-here"
        python3 generate_audio.py

    Security note: since this key was shared in a chat transcript at
    some point, it's worth restricting it in the Google Cloud Console
    (Credentials -> this key -> API restrictions -> Cloud Text-to-Speech
    API only) and/or rotating it, so a leaked copy can't be used for
    anything beyond generating speech.

What it does:
    - Vocab: one MP3 per unique word (audio/vocab/{slug}.mp3), narrated
      by a single consistent voice, via one Text-to-Speech API call each.
    - Dialogues: for each lesson, synthesizes each line separately (with
      the correct speaker's voice), then stitches them into one combined
      MP3 per lesson (audio/{shortPrefix}-listening.mp3) with a short
      pause between turns via pydub, and writes a sidecar timing file
      (audio/{shortPrefix}-listening.json) recording each line's
      [start, end) time in the combined file — course-engine.js uses
      this to highlight the correct transcript line in sync with
      playback. Per-line temp clips are deleted after stitching.

    Every output file is skipped if it already exists, so this script is
    safe to re-run after an interruption (or after editing just one
    lesson's dialogue) without re-paying for clips you already have.

Usage:
    python3 generate_audio.py                 # generate everything
    python3 generate_audio.py --lesson=lesson-01   # just one lesson's dialogue (cheap sanity check)
    python3 generate_audio.py --vocab-only     # skip all dialogues
    python3 generate_audio.py --dialogues-only # skip all vocab words
    python3 generate_audio.py --dry-run        # print the plan, call nothing, spend nothing
"""
import argparse
import json
import os
import sys
import time

MANIFEST_PATH = "audio-manifest.json"
TTS_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"


def ensure_manifest():
    if not os.path.exists(MANIFEST_PATH):
        print(f"{MANIFEST_PATH} not found — building it from the lesson data first...")
        import extract_audio_manifest
        extract_audio_manifest.main()
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def synthesize(api_key, text, voice_name, session):
    """One Google Cloud TTS REST call -> raw MP3 bytes."""
    lang_code = "-".join(voice_name.split("-")[:2])  # "en-GB-Neural2-A" -> "en-GB"
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": lang_code, "name": voice_name},
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": 0.98},
    }
    resp = session.post(f"{TTS_ENDPOINT}?key={api_key}", json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"TTS API error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    import base64
    return base64.b64decode(data["audioContent"])


def generate_vocab(manifest, api_key, session, dry_run):
    items = manifest["vocab"]
    os.makedirs("audio/vocab", exist_ok=True)
    made, skipped = 0, 0
    for item in items:
        path = item["path"]
        if os.path.exists(path):
            skipped += 1
            continue
        if dry_run:
            print(f"[dry-run] would generate {path}  <- \"{item['word']}\" ({item['voice']})")
            continue
        try:
            audio_bytes = synthesize(api_key, item["word"], item["voice"], session)
            with open(path, "wb") as f:
                f.write(audio_bytes)
            made += 1
            print(f"  vocab: {path}")
        except Exception as e:
            print(f"  FAILED vocab '{item['word']}' -> {path}: {e}", file=sys.stderr)
        time.sleep(0.05)  # be gentle with the API
    print(f"Vocab: {made} generated, {skipped} already present, {len(items)} total.")


def generate_dialogues(manifest, api_key, session, dry_run, only_lesson=None):
    try:
        from pydub import AudioSegment
    except ImportError:
        if not dry_run:
            print("pydub is required for dialogue stitching. Install with: pip install pydub", file=sys.stderr)
            print("(ffmpeg must also be installed and on PATH.)", file=sys.stderr)
            sys.exit(1)
        AudioSegment = None

    os.makedirs("audio", exist_ok=True)
    pause_ms = manifest.get("pauseMsBetweenTurns", 450)
    voices = manifest["voices"]
    made, skipped = 0, 0

    for dlg in manifest["dialogues"]:
        prefix = dlg["shortPrefix"]
        if only_lesson and prefix != only_lesson:
            continue
        mp3_path = f"audio/{prefix}-listening.mp3"
        json_path = f"audio/{prefix}-listening.json"
        if os.path.exists(mp3_path) and os.path.exists(json_path):
            skipped += 1
            continue
        if dry_run:
            print(f"[dry-run] would generate {mp3_path} + {json_path} ({len(dlg['lines'])} lines, lesson: {dlg['title']})")
            continue

        combined = AudioSegment.empty()
        pause = AudioSegment.silent(duration=pause_ms)
        timings = []
        tmp_files = []
        try:
            for i, line in enumerate(dlg["lines"]):
                voice = voices["anna"] if line["speaker"] == "Anna" else voices["tomasz"]
                audio_bytes = synthesize(api_key, line["line"], voice, session)
                tmp_path = f"audio/_tmp_{prefix}_line{i}.mp3"
                with open(tmp_path, "wb") as f:
                    f.write(audio_bytes)
                tmp_files.append(tmp_path)
                clip = AudioSegment.from_mp3(tmp_path)
                start = len(combined) / 1000.0
                combined += clip
                end = len(combined) / 1000.0
                timings.append({"start": round(start, 2), "end": round(end, 2), "speaker": line["speaker"]})
                if i < len(dlg["lines"]) - 1:
                    combined += pause
                time.sleep(0.05)

            combined.export(mp3_path, format="mp3")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(timings, f, indent=2)
            made += 1
            print(f"  dialogue: {mp3_path} ({len(dlg['lines'])} lines, {len(combined)/1000:.1f}s)")
        except Exception as e:
            print(f"  FAILED dialogue for {prefix}: {e}", file=sys.stderr)
        finally:
            for t in tmp_files:
                try:
                    os.remove(t)
                except OSError:
                    pass

    print(f"Dialogues: {made} generated, {skipped} already present, {len(manifest['dialogues'])} total.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", default=None, help="Only generate this lesson's dialogue, e.g. --lesson=lesson-01")
    parser.add_argument("--vocab-only", action="store_true")
    parser.add_argument("--dialogues-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without calling the API or spending quota")
    args = parser.parse_args()

    manifest = ensure_manifest()

    api_key = os.environ.get("GOOGLE_TTS_API_KEY")
    if not api_key and not args.dry_run:
        print("Set GOOGLE_TTS_API_KEY in your environment first:\n"
              "  export GOOGLE_TTS_API_KEY=\"your-key-here\"", file=sys.stderr)
        sys.exit(1)

    session = None
    if not args.dry_run:
        import requests
        session = requests.Session()

    if args.lesson:
        generate_dialogues(manifest, api_key, session, args.dry_run, only_lesson=args.lesson)
        return

    if not args.dialogues_only:
        generate_vocab(manifest, api_key, session, args.dry_run)
    if not args.vocab_only:
        generate_dialogues(manifest, api_key, session, args.dry_run)


if __name__ == "__main__":
    main()
