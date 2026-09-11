# 🎬 DIRECTOR'S CUT
> **Turn ordinary moments into movie scenes.**  
> *Warning: unnecessary drama may occur.*

Director's Cut is a local web application built for hackathons. It watches a person through their webcam, recognizes predefined human actions using computer vision (MediaPipe Pose), and automatically turns those ordinary actions into cinematic movie scenes with background music, dynamic captions, visual effects, and meme reactions.

---

## 🎭 The 10 Cinematic Actions

The application automatically identifies 10 distinct actions using geometric MediaPipe Pose tracking and triggers their cinematic treatment with your 10 custom BGMs in mixed form and comical captions:

1. **`ENTRY`** ➔ **Grand Entrance**  
   *Music pool:* `ramasami.mp3`, `Ladies and gentlement.mp3`, `meeshamadhavan.mp3`  
   *Captions:* "A wild main character appeared!", "Main character aura: 1000%."
2. **`BOTH HANDS UP`** ➔ **World Champion Victory**  
   *Music pool:* `arkum tholkate.mp3`, `Ladies and gentlement.mp3`, `puthiyamukham.mp3`  
   *Captions:* "HE'S THE CHAMPION OF THE WORLD!", "Rocky training montage unlocked."
3. **`RAISING HAND`** ➔ **Spider-Man Theme / Suspense**  
   *Music pool:* `spidy.mp3`, `puthiyamukham.mp3`, `bg4.mp3`  
   *Captions:* "Bro thinks he has web-shooters.", "Spider-Man stretch activated."
4. **`HANDS ON HEAD`** ➔ **Existential Shock / Plot Twist**  
   *Music pool:* `neekolavalo.mp3`, `bg4.mp3`, `spidy.mp3`  
   *Captions:* "MIND = COMPLETELY BLOWN.", "Bro just remembered he left the stove on."
5. **`THINKING`** ➔ **Detective Noir / Mastermind**  
   *Music pool:* `meeshamadhavan.mp3`, `bg4.mp3`, `ramasami.mp3`  
   *Captions:* "The Thinker has entered the chat.", "Brain cells operating at 110% capacity."
6. **`DRINKING WATER`** ➔ **Slow-Motion Romance**  
   *Music pool:* `kattipudu.mp3`, `neekolavalo.mp3`  
   *Captions:* "Taking a sip like he's in a cologne commercial.", "Hydrated and unnecessarily dramatic."
7. **`HAND ON HEART`** ➔ **Dramatic Allegiance / Oath**  
   *Music pool:* `kattipudu.mp3`, `arkum tholkate.mp3`, `Ladies and gentlement.mp3`  
   *Captions:* "An emotional allegiance to the cinematic arts.", "Pledging loyalty to the snack cabinet."
8. **`STANDING UP`** ➔ **Hero Ascension (Act 3)**  
   *Music pool:* `puthiyamukham.mp3`, `arkum tholkate.mp3`, `meeshamadhavan.mp3`  
   *Captions:* "HE HAS RISEN.", "Standing up like a superhero in the third act."
9. **`SITTING DOWN`** ➔ **Main Character Energy / Mafia Boss**  
   *Music pool:* `meeshamadhavan.mp3`, `ramasami.mp3`, `Ladies and gentlement.mp3`  
   *Captions:* "Bro sat down like a mafia boss.", "Chair secured. Zero regrets."
10. **`EXIT`** ➔ **Tragic Farewell / Ghosted**  
    *Music pool:* `exit.mp3`, `bg4.mp3`, `ramasami.mp3`  
    *Captions:* "And bro just dipped.", "Gone. Reduced to atoms."

---

## 🎬 Opening Clapper & Film-Reel Loader
- When you click **`START MY MOVIE`**, a spinning golden film-reel loader appears and plays **`start_camera_action.mp3`** ("Camera... rolling... and ACTION!").
- The stage smoothly unveils exactly when the clapper audio finishes!

---

## 🎵 Your 10 Custom Soundtracks in Mixed Form

All soundtracks are loaded dynamically from **`music/`** (mirrored to **`static/music/`**). Each action has a pool of your tracks that randomly shuffles:

```
music/
├── start_camera_action.mp3  <-- Opening clapper audio
├── ramasami.mp3             <-- Grand Entrance / Comedy Mass Beat
├── spidy.mp3                <-- Spider-Man suspense
├── Ladies and gentlement.mp3<-- Victory / Hype / Grand Announcement
├── arkum tholkate.mp3       <-- Unbeatable Champion / Powerful Ascension
├── meeshamadhavan.mp3       <-- Mustache Twirl / Heist Mastermind / Mafia Sit
├── kattipudu.mp3            <-- Slow-Motion Romance / Emotional Heart
├── neekolavalo.mp3          <-- Dramatic Plot Twist / Catchy Upbeat
├── puthiyamukham.mp3        <-- Hero Arrival / Rising Power
├── bg4.mp3                  <-- Tension / Suspense / Detective
└── exit.mp3                 <-- Tragic & Comical Exit
```

### How to Add or Swap Songs:
1. Simply drop your MP3 files into `static/music/` using any of the names above.
2. Or add more file names into `CINEMATIC_MODES[...]["bgm_pool"]` in `vision/cinematic.py` to shuffle among as many songs as you want!
3. Cache-busting (`?t=timestamp`) is built into the frontend, so new audio files play immediately without needing to clear browser cache.

---

## 🚀 Quickstart Guide

### 1. Run the Application
In your terminal, run:
```bash
./.venv/bin/python app.py
```

### 2. Open in Browser
Visit **`http://127.0.0.1:5050`** in Chrome, Safari, Edge, or Firefox.  
*(Note: Port 5050 avoids macOS AirPlay Receiver conflicts on port 5000).*

### 3. Experience the Movie
1. Click **`START MY MOVIE`** and hear the clapperboard count down: *"Camera... and ACTION!"*
2. Walk onto set to trigger your **`ENTRY`** (`ramasami.mp3` or heroic anthem).
3. Try different actions:
   - Put **Both Hands Up** in victory 🏆
   - **Raise Hand** like Spider-Man 🕸️ (`spidy.mp3`)
   - Grab your temples for **Shock / Mind Blown** 😱
   - Rest your chin on your hand to **Think** 🤔
   - Take a sip of water for a **Romantic Sip** 💧
   - Place a hand over your chest for **Hand on Heart** ❤️
   - **Stand Up** or **Sit Down** 🎬
   - Step out of the frame for the **Tragic Exit** 🚪
4. Click **`STOP MOVIE`** anytime to turn off your camera and return to the home screen.

---

## 🛠️ Developer Diagnostics
- Press **`Ctrl + Shift + D`** on your keyboard while on set to view live FPS, latency, confidence, cooldown timers, and skeleton overlay.
