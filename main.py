# main.py - Girly Pink Bio Link Portfolio by RUHI X QNR
# Complete Single-File Flask Application with Admin Panel

import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session, flash, jsonify, make_response
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.permanent_session_lifetime = timedelta(hours=24)

# ============================================================
# DATABASE / CONFIG FILE (JSON-based for single-file simplicity)
# ============================================================
DATA_FILE = "bio_data.json"

DEFAULT_DATA = {
    "admin": {
        "email": "RUHIVIG@BIO.COM",
        "password_hash": hashlib.sha256("RUHIVIGQNR".encode()).hexdigest()
    },
    "profile": {
        "name": "愛 | 𝗥𝗨𝗛𝗜 𝗫 𝗤𝗡𝗥〆",
        "tagline": "✨ Digital Creator • Bot Developer • Aesthetic Soul ✨",
        "about": "Hey there! I'm Ruhi 💖 A passionate digital creator and bot developer from India. I love creating beautiful things with code and spreading aesthetic vibes. Welcome to my little corner of the internet! 🌸",
        "profile_pic": "https://i.imgur.com/placeholder.jpg",
        "background_video": "https://assets.mixkit.co/videos/preview/mixkit-pink-and-blue-ink-1192-large.mp4"
    },
    "bio_info": {
        "age": "17",
        "birthday": "January 1",
        "location": "India 🇮🇳",
        "religion": "Hindu 🙏",
        "idol": "BTS 💜",
        "relationship": "Single 💗",
        "hobbies": "Coding, Music, Anime",
        "language": "Hindi, English"
    },
    "skills": ["HTML", "CSS", "Python", "Bot Making", "Web Design", "JavaScript"],
    "social_links": {
        "youtube": {
            "label": "YouTube",
            "url": "https://youtube.com/@placeholder",
            "icon": "fab fa-youtube",
            "color": "#FF0000",
            "enabled": True
        },
        "telegram1": {
            "label": "Telegram Channel",
            "url": "https://t.me/RUHI_X_QNR85",
            "icon": "fab fa-telegram",
            "color": "#0088cc",
            "enabled": True
        },
        "telegram2": {
            "label": "Telegram Group",
            "url": "https://t.me/+eUyUJJzrMzExOTQ1",
            "icon": "fab fa-telegram",
            "color": "#0088cc",
            "enabled": True
        },
        "whatsapp": {
            "label": "WhatsApp Channel",
            "url": "https://whatsapp.com/channel/placeholder",
            "icon": "fab fa-whatsapp",
            "color": "#25D366",
            "enabled": True
        },
        "instagram": {
            "label": "Instagram",
            "url": "https://instagram.com/placeholder",
            "icon": "fab fa-instagram",
            "color": "#E1306C",
            "enabled": True
        },
        "github": {
            "label": "GitHub",
            "url": "https://github.com/placeholder",
            "icon": "fab fa-github",
            "color": "#fff",
            "enabled": False
        }
    },
    "second_developer": {
        "enabled": True,
        "name": "✦ Second Developer ✦",
        "about": "Co-developer and creative partner. Together we build amazing things! 🚀",
        "profile_pic": "https://i.imgur.com/placeholder2.jpg",
        "skills": ["Python", "JavaScript", "Bot Making"],
        "social_url": "https://t.me/placeholder"
    },
    "music": {
        "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "autoplay": False
    },
    "custom_css": "",
    "visitor_count": 0,
    "created_at": str(datetime.now())
}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for key in DEFAULT_DATA:
                if key not in data:
                    data[key] = DEFAULT_DATA[key]
            return data
        except (json.JSONDecodeError, Exception):
            return DEFAULT_DATA.copy()
    else:
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    data = load_data()
    data['visitor_count'] = data.get('visitor_count', 0) + 1
    save_data(data)
    return render_template_string(MAIN_HTML, data=data)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        data = load_data()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if (email.upper() == data['admin']['email'].upper() and
                password_hash == data['admin']['password_hash']):
            session.permanent = True
            session['admin_logged_in'] = True
            flash('Welcome back, Admin! 💖', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials! ❌', 'error')
    return render_template_string(ADMIN_LOGIN_HTML)


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully! 👋', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    data = load_data()
    return render_template_string(ADMIN_DASHBOARD_HTML, data=data)


@app.route('/admin/update/profile', methods=['POST'])
@admin_required
def update_profile():
    data = load_data()
    data['profile']['name'] = request.form.get('name', data['profile']['name'])
    data['profile']['tagline'] = request.form.get('tagline', data['profile']['tagline'])
    data['profile']['about'] = request.form.get('about', data['profile']['about'])
    data['profile']['profile_pic'] = request.form.get('profile_pic', data['profile']['profile_pic'])
    data['profile']['background_video'] = request.form.get('background_video', data['profile']['background_video'])
    save_data(data)
    flash('Profile updated successfully! ✅', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update/bio', methods=['POST'])
@admin_required
def update_bio():
    data = load_data()
    for key in data['bio_info']:
        val = request.form.get(key)
        if val is not None:
            data['bio_info'][key] = val
    skills_raw = request.form.get('skills', '')
    if skills_raw:
        data['skills'] = [s.strip() for s in skills_raw.split(',') if s.strip()]
    save_data(data)
    flash('Bio info updated! ✅', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update/socials', methods=['POST'])
@admin_required
def update_socials():
    data = load_data()
    for key in data['social_links']:
        label = request.form.get(f'{key}_label')
        url_val = request.form.get(f'{key}_url')
        enabled = request.form.get(f'{key}_enabled')
        if label is not None:
            data['social_links'][key]['label'] = label
        if url_val is not None:
            data['social_links'][key]['url'] = url_val
        data['social_links'][key]['enabled'] = enabled == 'on'
    save_data(data)
    flash('Social links updated! ✅', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update/second_dev', methods=['POST'])
@admin_required
def update_second_dev():
    data = load_data()
    data['second_developer']['enabled'] = request.form.get('enabled') == 'on'
    data['second_developer']['name'] = request.form.get('name', data['second_developer']['name'])
    data['second_developer']['about'] = request.form.get('about', data['second_developer']['about'])
    data['second_developer']['profile_pic'] = request.form.get('profile_pic', data['second_developer']['profile_pic'])
    data['second_developer']['social_url'] = request.form.get('social_url', data['second_developer']['social_url'])
    skills_raw = request.form.get('skills', '')
    if skills_raw:
        data['second_developer']['skills'] = [s.strip() for s in skills_raw.split(',') if s.strip()]
    save_data(data)
    flash('Second developer updated! ✅', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update/music', methods=['POST'])
@admin_required
def update_music():
    data = load_data()
    data['music']['url'] = request.form.get('music_url', data['music']['url'])
    data['music']['autoplay'] = request.form.get('autoplay') == 'on'
    save_data(data)
    flash('Music settings updated! ✅', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update/password', methods=['POST'])
@admin_required
def update_password():
    data = load_data()
    current = request.form.get('current_password', '')
    new_pass = request.form.get('new_password', '')
    confirm = request.form.get('confirm_password', '')
    current_hash = hashlib.sha256(current.encode()).hexdigest()
    if current_hash != data['admin']['password_hash']:
        flash('Current password is incorrect! ❌', 'error')
    elif new_pass != confirm:
        flash('New passwords do not match! ❌', 'error')
    elif len(new_pass) < 4:
        flash('Password must be at least 4 characters! ❌', 'error')
    else:
        data['admin']['password_hash'] = hashlib.sha256(new_pass.encode()).hexdigest()
        save_data(data)
        flash('Password changed successfully! 🔐', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update/email', methods=['POST'])
@admin_required
def update_email():
    data = load_data()
    new_email = request.form.get('new_email', '').strip()
    if new_email:
        data['admin']['email'] = new_email
        save_data(data)
        flash(f'Admin email updated to {new_email}! ✅', 'success')
    else:
        flash('Email cannot be empty! ❌', 'error')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/update/custom_css', methods=['POST'])
@admin_required
def update_custom_css():
    data = load_data()
    data['custom_css'] = request.form.get('custom_css', '')
    save_data(data)
    flash('Custom CSS updated! ✅', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/reset', methods=['POST'])
@admin_required
def reset_data():
    save_data(DEFAULT_DATA.copy())
    flash('All data reset to defaults! 🔄', 'success')
    return redirect(url_for('admin_dashboard'))


# ============================================================
# MAIN BIO PAGE HTML
# ============================================================

MAIN_HTML = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ data.profile.name }} | Bio Link</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        /* ======== RESET & ROOT ======== */
        * { margin:0; padding:0; box-sizing:border-box; }
        :root {
            --pink: #ff2d95;
            --magenta: #ff00ff;
            --hot-pink: #ff69b4;
            --deep-pink: #c2185b;
            --neon-pink: #ff1493;
            --dark-bg: #0a0a0a;
            --card-bg: rgba(255,20,147,0.08);
            --glass-bg: rgba(255,255,255,0.05);
            --glass-border: rgba(255,20,147,0.25);
            --text: #fff;
            --text-secondary: rgba(255,255,255,0.7);
            --radius: 30px;
            --radius-lg: 40px;
            --radius-xl: 50px;
        }

        html { scroll-behavior: smooth; }

        body {
            font-family: 'Poppins', sans-serif;
            background: var(--dark-bg);
            color: var(--text);
            overflow-x: hidden;
            min-height: 100vh;
        }

        /* ======== LOADING SCREEN ======== */
        #loading-screen {
            position: fixed; top:0; left:0; width:100%; height:100%;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0011 50%, #0a0a0a 100%);
            z-index: 99999; display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            transition: opacity 0.8s ease, visibility 0.8s ease;
        }
        #loading-screen.hidden { opacity:0; visibility:hidden; pointer-events:none; }

        .loading-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem; font-weight:900;
            color: var(--neon-pink);
            text-shadow: 0 0 20px var(--pink), 0 0 40px var(--magenta), 0 0 80px var(--pink);
            letter-spacing: 8px; margin-bottom: 40px;
            animation: glitchText 2s infinite;
        }

        .loading-bar-container {
            width: 300px; height: 4px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px; overflow: hidden;
            position: relative;
        }
        .loading-bar {
            height: 100%; width: 0%;
            background: linear-gradient(90deg, var(--pink), var(--magenta), var(--hot-pink));
            border-radius: 10px;
            animation: loadBar 2.5s ease-in-out forwards;
            box-shadow: 0 0 20px var(--pink);
        }
        .loading-text {
            margin-top: 20px; font-size: 0.75rem;
            color: var(--text-secondary); letter-spacing: 3px;
            font-family: 'Orbitron', sans-serif;
        }
        .loading-percent {
            margin-top: 10px; font-size: 2rem; font-weight: 700;
            color: var(--neon-pink);
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 10px var(--pink);
        }

        .loading-hearts {
            position: absolute; width: 100%; height: 100%;
            pointer-events: none; overflow: hidden;
        }
        .loading-heart {
            position: absolute; font-size: 1.5rem;
            animation: floatUpHeart 3s ease-in infinite;
            opacity: 0;
        }

        @keyframes loadBar { 0%{width:0%} 100%{width:100%} }
        @keyframes glitchText {
            0%,100%{transform:translate(0)} 20%{transform:translate(-2px,2px)}
            40%{transform:translate(2px,-2px)} 60%{transform:translate(-1px,-1px)}
            80%{transform:translate(1px,1px)}
        }
        @keyframes floatUpHeart {
            0%{transform:translateY(100vh) scale(0);opacity:0}
            10%{opacity:1}
            100%{transform:translateY(-20vh) scale(1);opacity:0}
        }

        /* ======== BACKGROUND ======== */
        .bg-video-container {
            position:fixed; top:0; left:0; width:100%; height:100%;
            z-index:0; overflow:hidden;
        }
        .bg-video-container video {
            width:100%; height:100%; object-fit:cover;
        }
        .bg-overlay {
            position:fixed; top:0; left:0; width:100%; height:100%;
            background: linear-gradient(135deg,
                rgba(10,0,20,0.85) 0%,
                rgba(40,0,30,0.80) 30%,
                rgba(20,0,40,0.85) 60%,
                rgba(10,0,10,0.90) 100%);
            z-index:1;
        }

        /* ======== FLOATING PARTICLES ======== */
        .particles-container {
            position:fixed; top:0; left:0; width:100%; height:100%;
            z-index:2; pointer-events:none; overflow:hidden;
        }
        .particle {
            position:absolute;
            animation: floatParticle linear infinite;
            opacity:0;
        }
        @keyframes floatParticle {
            0%{transform:translateY(100vh) rotate(0deg);opacity:0}
            10%{opacity:0.8}
            90%{opacity:0.8}
            100%{transform:translateY(-10vh) rotate(720deg);opacity:0}
        }

        /* ======== SPARKLE CURSOR TRAIL ======== */
        .sparkle {
            position:fixed; pointer-events:none; z-index:9998;
            font-size:12px; animation: sparkleAnim 1s ease-out forwards;
        }
        @keyframes sparkleAnim {
            0%{transform:scale(1) rotate(0deg);opacity:1}
            100%{transform:scale(0) rotate(180deg) translateY(-50px);opacity:0}
        }

        /* ======== MAIN CONTENT ======== */
        .main-content {
            position:relative; z-index:10;
            max-width: 520px; margin: 0 auto;
            padding: 20px 15px 100px;
            opacity:0; transform:translateY(30px);
            animation: fadeInUp 1s ease 3s forwards;
        }
        @keyframes fadeInUp {
            to{opacity:1;transform:translateY(0)}
        }

        /* ======== GLASS CARD ======== */
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 30px;
            margin-bottom: 20px;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .glass-card::before {
            content:'';position:absolute;top:0;left:0;right:0;
            height:1px;
            background:linear-gradient(90deg,transparent,rgba(255,20,147,0.5),transparent);
        }
        .glass-card:hover {
            border-color: rgba(255,20,147,0.5);
            box-shadow: 0 8px 40px rgba(255,20,147,0.15);
            transform: translateY(-3px);
        }

        /* ======== PROFILE SECTION ======== */
        .profile-section { text-align:center; padding-top:30px; }

        .profile-pic-wrapper {
            width: 150px; height: 150px;
            margin: 0 auto 20px;
            position: relative;
            border-radius: 50%;
        }
        .profile-pic-ring {
            position:absolute; top:-8px; left:-8px;
            width: 166px; height: 166px;
            border-radius: 50%;
            border: 3px solid transparent;
            border-top-color: var(--neon-pink);
            border-right-color: var(--magenta);
            border-bottom-color: var(--hot-pink);
            animation: spinRing 3s linear infinite;
            filter: drop-shadow(0 0 10px var(--pink));
        }
        .profile-pic-ring-inner {
            position:absolute; top:-4px; left:-4px;
            width: 158px; height: 158px;
            border-radius: 50%;
            border: 2px solid transparent;
            border-top-color: var(--hot-pink);
            border-left-color: var(--magenta);
            animation: spinRing 2s linear infinite reverse;
            filter: drop-shadow(0 0 6px var(--magenta));
        }
        @keyframes spinRing { to{transform:rotate(360deg)} }

        .profile-pic {
            width: 150px; height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid rgba(255,20,147,0.5);
            position: relative; z-index: 2;
        }

        .profile-name {
            font-size: 1.6rem; font-weight: 800;
            background: linear-gradient(135deg, var(--neon-pink), var(--magenta), var(--hot-pink), #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            margin-bottom: 8px;
            animation: shimmer 3s ease-in-out infinite;
            background-size: 200% 200%;
        }
        @keyframes shimmer {
            0%,100%{background-position:0% 50%}
            50%{background-position:100% 50%}
        }

        .profile-tagline {
            font-size: 0.85rem;
            color: var(--text-secondary);
            letter-spacing: 1px;
        }

        .online-badge {
            display:inline-flex; align-items:center; gap:6px;
            background: rgba(0,255,100,0.1);
            border: 1px solid rgba(0,255,100,0.3);
            border-radius: 30px;
            padding: 4px 16px; margin-top: 12px;
            font-size: 0.75rem; color: #00ff64;
        }
        .online-dot {
            width:8px; height:8px; border-radius:50%;
            background:#00ff64;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%,100%{opacity:1;transform:scale(1)}
            50%{opacity:0.5;transform:scale(0.8)}
        }

        /* ======== SECTION TITLES ======== */
        .section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.85rem; font-weight: 700;
            color: var(--neon-pink);
            letter-spacing: 4px;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(255,20,147,0.5);
        }
        .section-title i { margin-right: 8px; }

        /* ======== ABOUT SECTION ======== */
        .about-text {
            font-size: 0.9rem; line-height: 1.8;
            color: var(--text-secondary);
            text-align: center;
        }

        /* ======== BIO GRID ======== */
        .bio-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        .bio-item {
            background: rgba(255,20,147,0.06);
            border: 1px solid rgba(255,20,147,0.15);
            border-radius: var(--radius);
            padding: 16px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .bio-item:hover {
            border-color: var(--neon-pink);
            background: rgba(255,20,147,0.12);
            transform: scale(1.03);
        }
        .bio-item-label {
            font-size: 0.65rem; text-transform: uppercase;
            letter-spacing: 2px; color: var(--neon-pink);
            margin-bottom: 6px; font-weight: 600;
        }
        .bio-item-value {
            font-size: 0.9rem; font-weight: 600;
            color: var(--text);
        }

        /* ======== SKILLS TAGS ======== */
        .skills-container {
            display: flex; flex-wrap: wrap;
            gap: 8px; justify-content: center;
            margin-top: 15px;
        }
        .skill-tag {
            background: linear-gradient(135deg, rgba(255,20,147,0.15), rgba(255,0,255,0.1));
            border: 1px solid rgba(255,20,147,0.3);
            border-radius: 30px;
            padding: 8px 20px;
            font-size: 0.8rem; font-weight: 500;
            color: var(--hot-pink);
            transition: all 0.3s ease;
            cursor: default;
        }
        .skill-tag:hover {
            background: linear-gradient(135deg, rgba(255,20,147,0.3), rgba(255,0,255,0.2));
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(255,20,147,0.3);
            color: #fff;
        }

        /* ======== SOCIAL BUTTONS ======== */
        .social-btn {
            display: flex; align-items: center; gap: 15px;
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 18px 24px;
            margin-bottom: 12px;
            color: var(--text); text-decoration: none;
            font-weight: 600; font-size: 0.95rem;
            transition: all 0.4s ease;
            position: relative; overflow: hidden;
            cursor: pointer;
        }
        .social-btn::after {
            content: ''; position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            transition: left 0.5s ease;
        }
        .social-btn:hover::after { left: 100%; }
        .social-btn:hover {
            transform: translateY(-3px) scale(1.02);
            border-color: rgba(255,20,147,0.6);
            box-shadow: 0 10px 40px rgba(255,20,147,0.2);
        }
        .social-btn .icon {
            width: 45px; height: 45px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
        }
        .social-btn .arrow {
            margin-left: auto; font-size: 1rem;
            color: var(--text-secondary);
            transition: transform 0.3s ease;
        }
        .social-btn:hover .arrow { transform: translateX(5px); }

        /* ======== SECOND DEVELOPER TOGGLE ======== */
        .toggle-btn {
            display: block; width: 100%; padding: 18px;
            background: linear-gradient(135deg, rgba(255,20,147,0.15), rgba(255,0,255,0.1));
            border: 2px solid var(--neon-pink);
            border-radius: var(--radius-lg);
            color: var(--neon-pink); font-weight: 700;
            font-size: 1rem; cursor: pointer;
            transition: all 0.4s ease;
            font-family: 'Poppins', sans-serif;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(255,20,147,0.5);
        }
        .toggle-btn:hover {
            background: linear-gradient(135deg, rgba(255,20,147,0.3), rgba(255,0,255,0.2));
            box-shadow: 0 0 30px rgba(255,20,147,0.4);
            transform: scale(1.02);
        }
        .second-dev-section {
            max-height: 0; overflow: hidden;
            transition: max-height 0.6s ease, opacity 0.4s ease;
            opacity: 0;
        }
        .second-dev-section.active {
            max-height: 800px; opacity: 1;
        }

        /* ======== MUSIC BUTTON ======== */
        .music-btn {
            position: fixed; bottom: 25px; right: 25px;
            width: 55px; height: 55px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--pink), var(--magenta));
            border: none; color: #fff; font-size: 1.2rem;
            cursor: pointer; z-index: 1000;
            box-shadow: 0 4px 20px rgba(255,20,147,0.5);
            transition: all 0.3s ease;
            display: flex; align-items: center; justify-content: center;
        }
        .music-btn:hover { transform: scale(1.1); }
        .music-btn.playing {
            animation: musicPulse 1s ease-in-out infinite;
        }
        @keyframes musicPulse {
            0%,100%{box-shadow:0 4px 20px rgba(255,20,147,0.5)}
            50%{box-shadow:0 4px 40px rgba(255,20,147,0.8)}
        }

        /* ======== VISITOR COUNTER ======== */
        .visitor-counter {
            text-align: center; padding: 15px;
            font-size: 0.75rem; color: var(--text-secondary);
            letter-spacing: 2px;
        }
        .visitor-counter span {
            color: var(--neon-pink); font-weight: 700;
        }

        /* ======== TOAST NOTIFICATIONS ======== */
        .toast-container {
            position: fixed; top: 20px; right: 20px;
            z-index: 99999; display: flex;
            flex-direction: column; gap: 10px;
        }
        .toast {
            background: rgba(20,0,20,0.95);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 14px 24px;
            color: var(--text);
            font-size: 0.85rem;
            animation: slideInToast 0.5s ease, fadeOutToast 0.5s ease 2.5s forwards;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: flex; align-items: center; gap: 10px;
        }
        @keyframes slideInToast {
            from{transform:translateX(100%);opacity:0}
            to{transform:translateX(0);opacity:1}
        }
        @keyframes fadeOutToast {
            to{transform:translateX(100%);opacity:0}
        }

        /* ======== FOOTER ======== */
        .footer {
            text-align: center; padding: 20px;
            font-size: 0.7rem; color: rgba(255,255,255,0.3);
            letter-spacing: 2px;
        }
        .footer a { color: var(--neon-pink); text-decoration: none; }

        /* ======== SCROLLBAR ======== */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--dark-bg); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--pink), var(--magenta));
            border-radius: 10px;
        }

        /* ======== RESPONSIVE ======== */
        @media (max-width: 480px) {
            .main-content { padding: 15px 10px 100px; }
            .glass-card { padding: 20px; border-radius: var(--radius); }
            .profile-name { font-size: 1.3rem; }
            .bio-grid { gap: 8px; }
            .bio-item { padding: 12px; border-radius: 20px; }
            .social-btn { padding: 14px 18px; border-radius: var(--radius); }
            .profile-pic-wrapper { width: 120px; height: 120px; }
            .profile-pic { width: 120px; height: 120px; }
            .profile-pic-ring { width: 136px; height: 136px; }
            .profile-pic-ring-inner { width: 128px; height: 128px; }
        }

        /* ======== CUSTOM CSS INJECTION ======== */
        {{ data.custom_css }}
    </style>
</head>
<body>

<!-- ======== LOADING SCREEN ======== -->
<div id="loading-screen">
    <div class="loading-hearts" id="loadingHearts"></div>
    <div class="loading-title">SYSTEM ACCESS</div>
    <div class="loading-bar-container">
        <div class="loading-bar"></div>
    </div>
    <div class="loading-text">INITIALIZING PROFILE...</div>
    <div class="loading-percent" id="loadPercent">0%</div>
</div>

<!-- ======== BACKGROUND VIDEO ======== -->
<div class="bg-video-container">
    <!-- REPLACE THIS VIDEO URL WITH YOUR OWN -->
    <video autoplay muted loop playsinline>
        <source src="{{ data.profile.background_video }}" type="video/mp4">
    </video>
</div>
<div class="bg-overlay"></div>

<!-- ======== FLOATING PARTICLES ======== -->
<div class="particles-container" id="particles"></div>

<!-- ======== TOAST CONTAINER ======== -->
<div class="toast-container" id="toastContainer"></div>

<!-- ======== MAIN CONTENT ======== -->
<div class="main-content" id="mainContent">

    <!-- PROFILE SECTION -->
    <div class="glass-card profile-section">
        <div class="profile-pic-wrapper">
            <div class="profile-pic-ring"></div>
            <div class="profile-pic-ring-inner"></div>
            <!-- REPLACE THIS PROFILE PICTURE URL -->
            <img src="{{ data.profile.profile_pic }}" alt="Profile" class="profile-pic"
                 onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI3NSIgY3k9Ijc1IiByPSI3NSIgZmlsbD0iIzMzMCIvPjx0ZXh0IHg9Ijc1IiB5PSI4NSIgZm9udC1zaXplPSI0MCIgZmlsbD0iI2ZmMTQ5MyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IkFyaWFsIj7wn4y4PC90ZXh0Pjwvc3ZnPg=='">
        </div>
        <h1 class="profile-name">{{ data.profile.name }}</h1>
        <p class="profile-tagline">{{ data.profile.tagline }}</p>
        <div class="online-badge">
            <div class="online-dot"></div>
            Online Now
        </div>
    </div>

    <!-- ABOUT SECTION -->
    <div class="glass-card">
        <div class="section-title"><i class="fas fa-heart"></i> ABOUT ME</div>
        <p class="about-text">{{ data.profile.about }}</p>
    </div>

    <!-- BIO INFO GRID -->
    <div class="glass-card">
        <div class="section-title"><i class="fas fa-info-circle"></i> BIO INFO</div>
        <div class="bio-grid">
            <div class="bio-item">
                <div class="bio-item-label">🎂 Age</div>
                <div class="bio-item-value">{{ data.bio_info.age }}</div>
            </div>
            <div class="bio-item">
                <div class="bio-item-label">🎉 Birthday</div>
                <div class="bio-item-value">{{ data.bio_info.birthday }}</div>
            </div>
            <div class="bio-item">
                <div class="bio-item-label">📍 Location</div>
                <div class="bio-item-value">{{ data.bio_info.location }}</div>
            </div>
            <div class="bio-item">
                <div class="bio-item-label">🙏 Religion</div>
                <div class="bio-item-value">{{ data.bio_info.religion }}</div>
            </div>
            <div class="bio-item">
                <div class="bio-item-label">⭐ Idol</div>
                <div class="bio-item-value">{{ data.bio_info.idol }}</div>
            </div>
            <div class="bio-item">
                <div class="bio-item-label">💝 Status</div>
                <div class="bio-item-value">{{ data.bio_info.relationship }}</div>
            </div>
            <div class="bio-item">
                <div class="bio-item-label">🎮 Hobbies</div>
                <div class="bio-item-value">{{ data.bio_info.hobbies }}</div>
            </div>
            <div class="bio-item">
                <div class="bio-item-label">🗣 Language</div>
                <div class="bio-item-value">{{ data.bio_info.language }}</div>
            </div>
        </div>

        <!-- SKILLS -->
        <div class="section-title" style="margin-top:25px"><i class="fas fa-code"></i> SKILLS</div>
        <div class="skills-container">
            {% for skill in data.skills %}
            <span class="skill-tag">{{ skill }}</span>
            {% endfor %}
        </div>
    </div>

    <!-- SOCIAL LINKS -->
    <div class="glass-card">
        <div class="section-title"><i class="fas fa-link"></i> CONNECT</div>
        {% for key, link in data.social_links.items() %}
        {% if link.enabled %}
        <a href="{{ link.url }}" target="_blank" rel="noopener" class="social-btn"
           onclick="showToast('Opening {{ link.label }}... 💖')">
            <div class="icon" style="background:{{ link.color }}22;color:{{ link.color }}">
                <i class="{{ link.icon }}"></i>
            </div>
            <span>{{ link.label }}</span>
            <span class="arrow"><i class="fas fa-arrow-right"></i></span>
        </a>
        {% endif %}
        {% endfor %}
    </div>

    <!-- SECOND DEVELOPER TOGGLE -->
    {% if data.second_developer.enabled %}
    <div class="glass-card" style="padding:15px;">
        <button class="toggle-btn" onclick="toggleSecondDev()">
            ✨ SECOND DEVELOPER ✨
        </button>
    </div>

    <div class="second-dev-section" id="secondDevSection">
        <div class="glass-card profile-section">
            <div class="profile-pic-wrapper" style="width:100px;height:100px;">
                <div class="profile-pic-ring" style="width:116px;height:116px;"></div>
                <img src="{{ data.second_developer.profile_pic }}" alt="Dev 2"
                     class="profile-pic" style="width:100px;height:100px;"
                     onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI1MCIgZmlsbD0iIzMzMCIvPjx0ZXh0IHg9IjUwIiB5PSI2MCIgZm9udC1zaXplPSIzMCIgZmlsbD0iI2ZmMTQ5MyIgdGV4dC1hbmNob3I9Im1pZGRsZSI+8J+SqzwvdGV4dD48L3N2Zz4='">
            </div>
            <h2 class="profile-name" style="font-size:1.2rem;">{{ data.second_developer.name }}</h2>
            <p class="about-text" style="margin-top:10px;">{{ data.second_developer.about }}</p>
            <div class="skills-container" style="margin-top:15px;">
                {% for skill in data.second_developer.skills %}
                <span class="skill-tag">{{ skill }}</span>
                {% endfor %}
            </div>
            <a href="{{ data.second_developer.social_url }}" target="_blank" rel="noopener"
               class="social-btn" style="margin-top:15px;justify-content:center;"
               onclick="showToast('Opening profile... 🌸')">
                <i class="fab fa-telegram"></i>
                <span>Contact</span>
            </a>
        </div>
    </div>
    {% endif %}

    <!-- VISITOR COUNTER -->
    <div class="visitor-counter">
        👁 TOTAL VIEWS: <span>{{ data.visitor_count }}</span>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        Made with 💖 by <a href="#">{{ data.profile.name }}</a><br>
        © 2025 All Rights Reserved
    </div>
</div>

<!-- ======== MUSIC BUTTON ======== -->
<button class="music-btn" id="musicBtn" onclick="toggleMusic()">
    <i class="fas fa-music" id="musicIcon"></i>
</button>
<!-- REPLACE THIS MUSIC URL WITH YOUR OWN MP3 -->
<audio id="bgMusic" loop preload="auto">
    <source src="{{ data.music.url }}" type="audio/mpeg">
</audio>

<script>
    // ======== LOADING SCREEN ========
    (function() {
        const loadPercent = document.getElementById('loadPercent');
        const heartsContainer = document.getElementById('loadingHearts');
        let percent = 0;
        const hearts = ['💖','💗','💕','✨','🌸','💝','💞','🎀'];
        for(let i=0;i<20;i++){
            const h = document.createElement('div');
            h.className='loading-heart';
            h.textContent=hearts[Math.floor(Math.random()*hearts.length)];
            h.style.left=Math.random()*100+'%';
            h.style.animationDelay=Math.random()*3+'s';
            h.style.animationDuration=(2+Math.random()*3)+'s';
            heartsContainer.appendChild(h);
        }
        const interval = setInterval(()=>{
            percent += Math.floor(Math.random()*8)+1;
            if(percent>100) percent=100;
            loadPercent.textContent = percent+'%';
            if(percent>=100){
                clearInterval(interval);
                setTimeout(()=>{
                    document.getElementById('loading-screen').classList.add('hidden');
                },600);
            }
        },80);
    })();

    // ======== FLOATING PARTICLES ========
    (function(){
        const container=document.getElementById('particles');
        const items=['💖','💗','✨','🌸','💕','⭐','💝','🎀','🦋','💞'];
        for(let i=0;i<25;i++){
            const p=document.createElement('div');
            p.className='particle';
            p.textContent=items[Math.floor(Math.random()*items.length)];
            p.style.left=Math.random()*100+'%';
            p.style.fontSize=(0.6+Math.random()*1.2)+'rem';
            p.style.animationDuration=(8+Math.random()*15)+'s';
            p.style.animationDelay=Math.random()*10+'s';
            container.appendChild(p);
        }
    })();

    // ======== SPARKLE CURSOR TRAIL ========
    let lastSparkle=0;
    document.addEventListener('mousemove',function(e){
        if(Date.now()-lastSparkle<60) return;
        lastSparkle=Date.now();
        createSparkle(e.clientX,e.clientY);
    });
    document.addEventListener('touchmove',function(e){
        if(Date.now()-lastSparkle<80) return;
        lastSparkle=Date.now();
        const t=e.touches[0];
        createSparkle(t.clientX,t.clientY);
    },{passive:true});

    function createSparkle(x,y){
        const s=document.createElement('div');
        s.className='sparkle';
        const items=['✨','💖','⭐','💗','🌸'];
        s.textContent=items[Math.floor(Math.random()*items.length)];
        s.style.left=x+'px';
        s.style.top=y+'px';
        document.body.appendChild(s);
        setTimeout(()=>s.remove(),1000);
    }

    // ======== TOAST NOTIFICATIONS ========
    function showToast(msg){
        const c=document.getElementById('toastContainer');
        const t=document.createElement('div');
        t.className='toast';
        t.innerHTML='<span>💖</span> <span>'+msg+'</span>';
        c.appendChild(t);
        setTimeout(()=>t.remove(),3000);
    }

    // ======== MUSIC TOGGLE ========
    let musicPlaying=false;
    function toggleMusic(){
        const audio=document.getElementById('bgMusic');
        const btn=document.getElementById('musicBtn');
        const icon=document.getElementById('musicIcon');
        if(musicPlaying){
            audio.pause();
            btn.classList.remove('playing');
            icon.className='fas fa-music';
            showToast('Music paused 🎵');
        } else {
            audio.play().then(()=>{
                btn.classList.add('playing');
                icon.className='fas fa-pause';
                showToast('Now playing music 🎶');
            }).catch(()=>{
                showToast('Click again to play music 🎵');
            });
        }
        musicPlaying=!musicPlaying;
    }

    // ======== SECOND DEVELOPER TOGGLE ========
    function toggleSecondDev(){
        const s=document.getElementById('secondDevSection');
        if(s){
            s.classList.toggle('active');
            if(s.classList.contains('active')){
                showToast('Second developer revealed! 🌟');
                s.scrollIntoView({behavior:'smooth',block:'start'});
            }
        }
    }

    // ======== AUTO MUSIC (if enabled) ========
    {% if data.music.autoplay %}
    document.addEventListener('click',function autoPlay(){
        document.getElementById('bgMusic').play().then(()=>{
            document.getElementById('musicBtn').classList.add('playing');
            document.getElementById('musicIcon').className='fas fa-pause';
            musicPlaying=true;
        }).catch(()=>{});
        document.removeEventListener('click',autoPlay);
    },{once:true});
    {% endif %}
</script>
</body>
</html>
'''

# ============================================================
# ADMIN LOGIN PAGE HTML
# ============================================================

ADMIN_LOGIN_HTML = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>Admin Login | RuhibioQNR</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            font-family:'Poppins',sans-serif;
            background:linear-gradient(135deg,#0a0a0a,#1a0011,#0a001a);
            min-height:100vh;display:flex;align-items:center;justify-content:center;
            overflow:hidden;
        }
        .particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}
        .particle{position:absolute;animation:floatP linear infinite;opacity:0}
        @keyframes floatP{
            0%{transform:translateY(100vh);opacity:0}
            10%{opacity:.7}90%{opacity:.7}
            100%{transform:translateY(-10vh);opacity:0}
        }
        .login-container{
            position:relative;z-index:10;
            width:400px;max-width:90%;
        }
        .login-card{
            background:rgba(255,255,255,0.03);
            backdrop-filter:blur(25px);
            border:1px solid rgba(255,20,147,0.2);
            border-radius:40px;padding:50px 35px;
            box-shadow:0 20px 60px rgba(0,0,0,0.5);
            position:relative;overflow:hidden;
        }
        .login-card::before{
            content:'';position:absolute;top:0;left:0;right:0;height:2px;
            background:linear-gradient(90deg,transparent,#ff1493,transparent);
        }
        .login-icon{
            width:80px;height:80px;margin:0 auto 25px;
            background:linear-gradient(135deg,#ff1493,#ff00ff);
            border-radius:50%;display:flex;align-items:center;justify-content:center;
            font-size:2rem;color:#fff;
            box-shadow:0 0 40px rgba(255,20,147,0.5);
            animation:pulseIcon 2s infinite;
        }
        @keyframes pulseIcon{
            0%,100%{box-shadow:0 0 40px rgba(255,20,147,0.5)}
            50%{box-shadow:0 0 60px rgba(255,20,147,0.8)}
        }
        .login-title{
            font-family:'Orbitron',sans-serif;
            text-align:center;font-size:1.1rem;
            color:#ff1493;letter-spacing:5px;
            margin-bottom:30px;
            text-shadow:0 0 15px rgba(255,20,147,0.5);
        }
        .form-group{margin-bottom:20px}
        .form-group label{
            display:block;font-size:.75rem;
            color:rgba(255,255,255,0.5);letter-spacing:2px;
            text-transform:uppercase;margin-bottom:8px;
        }
        .form-group input{
            width:100%;padding:14px 20px;
            background:rgba(255,20,147,0.05);
            border:1px solid rgba(255,20,147,0.2);
            border-radius:30px;color:#fff;
            font-family:'Poppins',sans-serif;font-size:.9rem;
            outline:none;transition:all .3s;
        }
        .form-group input:focus{
            border-color:#ff1493;
            box-shadow:0 0 20px rgba(255,20,147,0.2);
        }
        .form-group input::placeholder{color:rgba(255,255,255,0.2)}
        .login-btn{
            width:100%;padding:16px;
            background:linear-gradient(135deg,#ff1493,#ff00ff);
            border:none;border-radius:30px;
            color:#fff;font-size:1rem;font-weight:700;
            cursor:pointer;letter-spacing:3px;
            font-family:'Poppins',sans-serif;
            transition:all .3s;margin-top:10px;
            text-transform:uppercase;
        }
        .login-btn:hover{
            transform:translateY(-3px);
            box-shadow:0 10px 40px rgba(255,20,147,0.5);
        }
        .flash-msg{
            text-align:center;padding:10px;margin-bottom:15px;
            border-radius:20px;font-size:.85rem;
        }
        .flash-error{background:rgba(255,0,0,0.15);color:#ff6b6b;border:1px solid rgba(255,0,0,0.3)}
        .flash-success{background:rgba(0,255,0,0.1);color:#00ff64;border:1px solid rgba(0,255,0,0.3)}
        .flash-info{background:rgba(0,136,255,0.1);color:#5bc0ff;border:1px solid rgba(0,136,255,0.3)}
        .back-link{
            display:block;text-align:center;margin-top:20px;
            color:rgba(255,255,255,0.4);text-decoration:none;font-size:.8rem;
        }
        .back-link:hover{color:#ff1493}
        .server-info{
            text-align:center;margin-top:20px;
            font-size:.65rem;color:rgba(255,255,255,0.2);
            letter-spacing:1px;
        }
    </style>
</head>
<body>
    <div class="particles" id="particles"></div>
    <div class="login-container">
        <div class="login-card">
            <div class="login-icon"><i class="fas fa-lock"></i></div>
            <div class="login-title">ADMIN ACCESS</div>
            {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
            {% for cat, msg in messages %}
            <div class="flash-msg flash-{{ cat }}">{{ msg }}</div>
            {% endfor %}
            {% endif %}
            {% endwith %}
            <form method="POST">
                <div class="form-group">
                    <label>Admin Email</label>
                    <input type="text" name="email" placeholder="Enter admin email..." required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter password..." required>
                </div>
                <button type="submit" class="login-btn">
                    <i class="fas fa-sign-in-alt"></i> ACCESS PANEL
                </button>
            </form>
            <a href="/" class="back-link">← Back to Bio</a>
            <div class="server-info">RuhibioQNR • Secure Admin Portal</div>
        </div>
    </div>
    <script>
        (function(){
            const c=document.getElementById('particles');
            const items=['💖','✨','🌸','💗','⭐','💕'];
            for(let i=0;i<15;i++){
                const p=document.createElement('div');
                p.className='particle';
                p.textContent=items[Math.floor(Math.random()*items.length)];
                p.style.left=Math.random()*100+'%';
                p.style.fontSize=(0.5+Math.random()*1)+'rem';
                p.style.animationDuration=(6+Math.random()*12)+'s';
                p.style.animationDelay=Math.random()*8+'s';
                c.appendChild(p);
            }
        })();
    </script>
</body>
</html>
'''

# ============================================================
# ADMIN DASHBOARD HTML
# ============================================================

ADMIN_DASHBOARD_HTML = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>Admin Dashboard | RuhibioQNR</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        :root{
            --pink:#ff1493;--magenta:#ff00ff;
            --dark:#0a0a0a;--card:rgba(255,255,255,0.03);
            --border:rgba(255,20,147,0.2);--radius:25px;
        }
        body{
            font-family:'Poppins',sans-serif;
            background:linear-gradient(135deg,#0a0a0a,#0d0015,#0a0a0a);
            color:#fff;min-height:100vh;
        }

        /* SIDEBAR */
        .sidebar{
            position:fixed;top:0;left:0;width:260px;height:100%;
            background:rgba(10,0,15,0.98);
            border-right:1px solid var(--border);
            z-index:100;padding:20px;overflow-y:auto;
            transition:transform .3s;
        }
        .sidebar-brand{
            font-family:'Orbitron',sans-serif;
            font-size:.9rem;color:var(--pink);
            letter-spacing:3px;text-align:center;
            padding:20px 0;border-bottom:1px solid var(--border);
            margin-bottom:20px;
            text-shadow:0 0 15px rgba(255,20,147,0.5);
        }
        .sidebar-menu{list-style:none}
        .sidebar-menu li{margin-bottom:5px}
        .sidebar-menu a{
            display:flex;align-items:center;gap:12px;
            padding:12px 18px;border-radius:15px;
            color:rgba(255,255,255,0.6);text-decoration:none;
            font-size:.85rem;transition:all .3s;
        }
        .sidebar-menu a:hover,.sidebar-menu a.active{
            background:rgba(255,20,147,0.1);
            color:var(--pink);border:1px solid rgba(255,20,147,0.2);
        }
        .sidebar-menu a i{width:20px;text-align:center}

        /* MAIN */
        .main-panel{
            margin-left:260px;padding:25px;
            min-height:100vh;
        }

        /* TOP BAR */
        .topbar{
            display:flex;justify-content:space-between;align-items:center;
            margin-bottom:30px;flex-wrap:wrap;gap:15px;
        }
        .topbar h1{
            font-family:'Orbitron',sans-serif;
            font-size:1.3rem;color:var(--pink);
            letter-spacing:3px;
            text-shadow:0 0 10px rgba(255,20,147,0.4);
        }
        .topbar-actions{display:flex;gap:10px;align-items:center}
        .topbar-btn{
            padding:10px 20px;border-radius:20px;
            border:1px solid var(--border);background:var(--card);
            color:#fff;font-family:'Poppins',sans-serif;
            font-size:.8rem;cursor:pointer;transition:all .3s;
            text-decoration:none;display:inline-flex;align-items:center;gap:8px;
        }
        .topbar-btn:hover{border-color:var(--pink);background:rgba(255,20,147,0.1)}
        .topbar-btn.danger{border-color:rgba(255,0,0,0.3);color:#ff6b6b}
        .topbar-btn.danger:hover{background:rgba(255,0,0,0.1)}

        /* STATS */
        .stats-grid{
            display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
            gap:15px;margin-bottom:30px;
        }
        .stat-card{
            background:var(--card);border:1px solid var(--border);
            border-radius:var(--radius);padding:22px;
            text-align:center;transition:all .3s;
        }
        .stat-card:hover{border-color:var(--pink);transform:translateY(-3px)}
        .stat-value{
            font-size:2rem;font-weight:800;
            background:linear-gradient(135deg,var(--pink),var(--magenta));
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        }
        .stat-label{
            font-size:.7rem;color:rgba(255,255,255,0.4);
            letter-spacing:2px;text-transform:uppercase;margin-top:5px;
        }

        /* SECTIONS */
        .admin-section{
            background:var(--card);border:1px solid var(--border);
            border-radius:var(--radius);padding:30px;
            margin-bottom:20px;transition:all .3s;
        }
        .admin-section:hover{border-color:rgba(255,20,147,0.35)}
        .section-header{
            font-family:'Orbitron',sans-serif;
            font-size:.8rem;color:var(--pink);
            letter-spacing:4px;text-transform:uppercase;
            margin-bottom:25px;display:flex;align-items:center;gap:10px;
            padding-bottom:15px;border-bottom:1px solid var(--border);
        }
        .section-header i{font-size:1rem}

        /* FORM ELEMENTS */
        .form-row{
            display:grid;grid-template-columns:1fr 1fr;
            gap:15px;margin-bottom:15px;
        }
        .form-row.full{grid-template-columns:1fr}
        .form-group{margin-bottom:15px}
        .form-group label{
            display:block;font-size:.7rem;
            color:rgba(255,255,255,0.5);letter-spacing:2px;
            text-transform:uppercase;margin-bottom:6px;font-weight:500;
        }
        .form-group input,.form-group textarea,.form-group select{
            width:100%;padding:12px 18px;
            background:rgba(255,20,147,0.04);
            border:1px solid rgba(255,20,147,0.15);
            border-radius:18px;color:#fff;
            font-family:'Poppins',sans-serif;font-size:.85rem;
            outline:none;transition:all .3s;
        }
        .form-group textarea{
            resize:vertical;min-height:80px;border-radius:20px;
        }
        .form-group input:focus,.form-group textarea:focus{
            border-color:var(--pink);
            box-shadow:0 0 15px rgba(255,20,147,0.15);
        }
        .form-group input::placeholder,.form-group textarea::placeholder{
            color:rgba(255,255,255,0.2);
        }

        /* CHECKBOX */
        .checkbox-group{
            display:flex;align-items:center;gap:10px;
            margin-bottom:10px;
        }
        .checkbox-group input[type=checkbox]{
            width:auto;appearance:none;
            width:20px;height:20px;
            background:rgba(255,20,147,0.1);
            border:2px solid rgba(255,20,147,0.3);
            border-radius:6px;cursor:pointer;
            position:relative;transition:all .3s;
        }
        .checkbox-group input[type=checkbox]:checked{
            background:var(--pink);border-color:var(--pink);
        }
        .checkbox-group input[type=checkbox]:checked::after{
            content:'✓';position:absolute;
            top:50%;left:50%;transform:translate(-50%,-50%);
            color:#fff;font-size:.75rem;font-weight:700;
        }
        .checkbox-group label{
            font-size:.85rem;color:rgba(255,255,255,0.7);
            margin-bottom:0;letter-spacing:0;text-transform:none;
        }

        /* SUBMIT BTN */
        .submit-btn{
            padding:14px 35px;
            background:linear-gradient(135deg,var(--pink),var(--magenta));
            border:none;border-radius:25px;
            color:#fff;font-size:.9rem;font-weight:600;
            cursor:pointer;font-family:'Poppins',sans-serif;
            transition:all .3s;letter-spacing:1px;
        }
        .submit-btn:hover{
            transform:translateY(-2px);
            box-shadow:0 8px 30px rgba(255,20,147,0.4);
        }

        /* SOCIAL EDIT ITEM */
        .social-edit-item{
            background:rgba(255,20,147,0.03);
            border:1px solid rgba(255,20,147,0.1);
            border-radius:20px;padding:20px;margin-bottom:15px;
        }
        .social-edit-header{
            font-weight:600;color:var(--pink);
            margin-bottom:12px;font-size:.9rem;
        }

        /* FLASH */
        .flash-container{margin-bottom:20px}
        .flash-msg{
            padding:14px 20px;border-radius:18px;
            margin-bottom:10px;font-size:.85rem;
            display:flex;align-items:center;gap:10px;
        }
        .flash-success{background:rgba(0,255,100,0.08);color:#00ff64;border:1px solid rgba(0,255,100,0.2)}
        .flash-error{background:rgba(255,0,0,0.08);color:#ff6b6b;border:1px solid rgba(255,0,0,0.2)}
        .flash-info{background:rgba(0,136,255,0.08);color:#5bc0ff;border:1px solid rgba(0,136,255,0.2)}

        /* MOBILE MENU */
        .mobile-toggle{
            display:none;position:fixed;top:15px;left:15px;
            z-index:200;width:45px;height:45px;
            background:var(--card);border:1px solid var(--border);
            border-radius:12px;color:var(--pink);
            font-size:1.2rem;cursor:pointer;
            align-items:center;justify-content:center;
        }

        /* SCROLLBAR */
        ::-webkit-scrollbar{width:5px}
        ::-webkit-scrollbar-track{background:transparent}
        ::-webkit-scrollbar-thumb{background:rgba(255,20,147,0.3);border-radius:10px}

        @media(max-width:768px){
            .sidebar{transform:translateX(-100%)}
            .sidebar.open{transform:translateX(0)}
            .main-panel{margin-left:0;padding:15px;padding-top:70px}
            .mobile-toggle{display:flex}
            .form-row{grid-template-columns:1fr}
            .topbar h1{font-size:1rem}
            .stats-grid{grid-template-columns:1fr 1fr}
        }
    </style>
</head>
<body>

<!-- MOBILE TOGGLE -->
<button class="mobile-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">
    <i class="fas fa-bars"></i>
</button>

<!-- SIDEBAR -->
<nav class="sidebar" id="sidebar">
    <div class="sidebar-brand">💖 RuhibioQNR<br><small style="font-size:.55rem;color:rgba(255,255,255,.3)">ADMIN PANEL</small></div>
    <ul class="sidebar-menu">
        <li><a href="#stats" class="active"><i class="fas fa-chart-bar"></i> Dashboard</a></li>
        <li><a href="#profile-section"><i class="fas fa-user"></i> Profile</a></li>
        <li><a href="#bio-section"><i class="fas fa-info-circle"></i> Bio Info</a></li>
        <li><a href="#socials-section"><i class="fas fa-link"></i> Social Links</a></li>
        <li><a href="#seconddev-section"><i class="fas fa-user-friends"></i> 2nd Developer</a></li>
        <li><a href="#music-section"><i class="fas fa-music"></i> Music</a></li>
        <li><a href="#security-section"><i class="fas fa-shield-alt"></i> Security</a></li>
        <li><a href="#css-section"><i class="fas fa-paint-brush"></i> Custom CSS</a></li>
        <li><a href="#danger-section"><i class="fas fa-exclamation-triangle"></i> Danger Zone</a></li>
        <li><a href="/"><i class="fas fa-eye"></i> View Bio</a></li>
        <li><a href="/admin/logout"><i class="fas fa-sign-out-alt"></i> Logout</a></li>
    </ul>
</nav>

<!-- MAIN PANEL -->
<div class="main-panel">
    <!-- TOP BAR -->
    <div class="topbar">
        <h1>DASHBOARD</h1>
        <div class="topbar-actions">
            <a href="/" target="_blank" class="topbar-btn"><i class="fas fa-eye"></i> View Live</a>
            <a href="/admin/logout" class="topbar-btn danger"><i class="fas fa-sign-out-alt"></i> Logout</a>
        </div>
    </div>

    <!-- FLASH MESSAGES -->
    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
    <div class="flash-container">
        {% for cat, msg in messages %}
        <div class="flash-msg flash-{{ cat }}">{{ msg }}</div>
        {% endfor %}
    </div>
    {% endif %}
    {% endwith %}

    <!-- STATS -->
    <div class="stats-grid" id="stats">
        <div class="stat-card">
            <div class="stat-value">{{ data.visitor_count }}</div>
            <div class="stat-label">Total Views</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ data.social_links|length }}</div>
            <div class="stat-label">Social Links</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ data.skills|length }}</div>
            <div class="stat-label">Skills</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">✅</div>
            <div class="stat-label">Status: Active</div>
        </div>
    </div>

    <!-- ======== PROFILE EDIT ======== -->
    <div class="admin-section" id="profile-section">
        <div class="section-header"><i class="fas fa-user"></i> EDIT PROFILE</div>
        <form method="POST" action="/admin/update/profile">
            <div class="form-row">
                <div class="form-group">
                    <label>Display Name</label>
                    <input type="text" name="name" value="{{ data.profile.name }}">
                </div>
                <div class="form-group">
                    <label>Tagline</label>
                    <input type="text" name="tagline" value="{{ data.profile.tagline }}">
                </div>
            </div>
            <div class="form-group">
                <label>About Me</label>
                <textarea name="about" rows="3">{{ data.profile.about }}</textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Profile Picture URL</label>
                    <input type="url" name="profile_pic" value="{{ data.profile.profile_pic }}" placeholder="https://...">
                </div>
                <div class="form-group">
                    <label>Background Video URL</label>
                    <input type="url" name="background_video" value="{{ data.profile.background_video }}" placeholder="https://...mp4">
                </div>
            </div>
            <button type="submit" class="submit-btn"><i class="fas fa-save"></i> Save Profile</button>
        </form>
    </div>

    <!-- ======== BIO INFO EDIT ======== -->
    <div class="admin-section" id="bio-section">
        <div class="section-header"><i class="fas fa-info-circle"></i> EDIT BIO INFO</div>
        <form method="POST" action="/admin/update/bio">
            <div class="form-row">
                <div class="form-group">
                    <label>Age</label>
                    <input type="text" name="age" value="{{ data.bio_info.age }}">
                </div>
                <div class="form-group">
                    <label>Birthday</label>
                    <input type="text" name="birthday" value="{{ data.bio_info.birthday }}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" name="location" value="{{ data.bio_info.location }}">
                </div>
                <div class="form-group">
                    <label>Religion</label>
                    <input type="text" name="religion" value="{{ data.bio_info.religion }}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Idol</label>
                    <input type="text" name="idol" value="{{ data.bio_info.idol }}">
                </div>
                <div class="form-group">
                    <label>Relationship Status</label>
                    <input type="text" name="relationship" value="{{ data.bio_info.relationship }}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Hobbies</label>
                    <input type="text" name="hobbies" value="{{ data.bio_info.hobbies }}">
                </div>
                <div class="form-group">
                    <label>Language</label>
                    <input type="text" name="language" value="{{ data.bio_info.language }}">
                </div>
            </div>
            <div class="form-group">
                <label>Skills (comma separated)</label>
                <input type="text" name="skills" value="{{ data.skills|join(', ') }}"
                       placeholder="HTML, CSS, Python, Bot Making">
            </div>
            <button type="submit" class="submit-btn"><i class="fas fa-save"></i> Save Bio Info</button>
        </form>
    </div>

    <!-- ======== SOCIAL LINKS EDIT ======== -->
    <div class="admin-section" id="socials-section">
        <div class="section-header"><i class="fas fa-link"></i> EDIT SOCIAL LINKS</div>
        <form method="POST" action="/admin/update/socials">
            {% for key, link in data.social_links.items() %}
            <div class="social-edit-item">
                <div class="social-edit-header"><i class="{{ link.icon }}"></i> {{ key|upper }}</div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Label</label>
                        <input type="text" name="{{ key }}_label" value="{{ link.label }}">
                    </div>
                    <div class="form-group">
                        <label>URL</label>
                        <input type="url" name="{{ key }}_url" value="{{ link.url }}">
                    </div>
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="{{ key }}_enabled" name="{{ key }}_enabled"
                           {% if link.enabled %}checked{% endif %}>
                    <label for="{{ key }}_enabled">Enabled (visible on bio page)</label>
                </div>
            </div>
            {% endfor %}
            <button type="submit" class="submit-btn"><i class="fas fa-save"></i> Save Social Links</button>
        </form>
    </div>

    <!-- ======== SECOND DEVELOPER EDIT ======== -->
    <div class="admin-section" id="seconddev-section">
        <div class="section-header"><i class="fas fa-user-friends"></i> SECOND DEVELOPER</div>
        <form method="POST" action="/admin/update/second_dev">
            <div class="checkbox-group" style="margin-bottom:20px">
                <input type="checkbox" id="dev_enabled" name="enabled"
                       {% if data.second_developer.enabled %}checked{% endif %}>
                <label for="dev_enabled">Enable Second Developer Section</label>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" name="name" value="{{ data.second_developer.name }}">
                </div>
                <div class="form-group">
                    <label>Profile Picture URL</label>
                    <input type="url" name="profile_pic" value="{{ data.second_developer.profile_pic }}">
                </div>
            </div>
            <div class="form-group">
                <label>About</label>
                <textarea name="about" rows="2">{{ data.second_developer.about }}</textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Skills (comma separated)</label>
                    <input type="text" name="skills" value="{{ data.second_developer.skills|join(', ') }}">
                </div>
                <div class="form-group">
                    <label>Social/Contact URL</label>
                    <input type="url" name="social_url" value="{{ data.second_developer.social_url }}">
                </div>
            </div>
            <button type="submit" class="submit-btn"><i class="fas fa-save"></i> Save</button>
        </form>
    </div>

    <!-- ======== MUSIC EDIT ======== -->
    <div class="admin-section" id="music-section">
        <div class="section-header"><i class="fas fa-music"></i> MUSIC SETTINGS</div>
        <form method="POST" action="/admin/update/music">
            <div class="form-group">
                <label>Music MP3 URL</label>
                <input type="url" name="music_url" value="{{ data.music.url }}"
                       placeholder="https://example.com/music.mp3">
            </div>
            <div class="checkbox-group" style="margin-bottom:20px">
                <input type="checkbox" id="autoplay" name="autoplay"
                       {% if data.music.autoplay %}checked{% endif %}>
                <label for="autoplay">Auto-play on first click</label>
            </div>
            <button type="submit" class="submit-btn"><i class="fas fa-save"></i> Save Music</button>
        </form>
    </div>

    <!-- ======== SECURITY ======== -->
    <div class="admin-section" id="security-section">
        <div class="section-header"><i class="fas fa-shield-alt"></i> SECURITY</div>

        <!-- CHANGE EMAIL -->
        <form method="POST" action="/admin/update/email" style="margin-bottom:25px;">
            <div class="form-group">
                <label>Admin Email</label>
                <input type="text" name="new_email" value="{{ data.admin.email }}">
            </div>
            <button type="submit" class="submit-btn"><i class="fas fa-envelope"></i> Update Email</button>
        </form>

        <!-- CHANGE PASSWORD -->
        <form method="POST" action="/admin/update/password">
            <div class="form-row">
                <div class="form-group">
                    <label>Current Password</label>
                    <input type="password" name="current_password" placeholder="Current password" required>
                </div>
                <div class="form-group">
                    <label>New Password</label>
                    <input type="password" name="new_password" placeholder="New password" required>
                </div>
            </div>
            <div class="form-group">
                <label>Confirm New Password</label>
                <input type="password" name="confirm_password" placeholder="Confirm new password" required>
            </div>
            <button type="submit" class="submit-btn"><i class="fas fa-key"></i> Change Password</button>
        </form>
    </div>

    <!-- ======== CUSTOM CSS ======== -->
    <div class="admin-section" id="css-section">
        <div class="section-header"><i class="fas fa-paint-brush"></i> CUSTOM CSS</div>
        <form method="POST" action="/admin/update/custom_css">
            <div class="form-group">
                <label>Custom CSS (injected into bio page)</label>
                <textarea name="custom_css" rows="6" placeholder="/* Add custom styles here */
.profile-name { color: red !important; }">{{ data.custom_css }}</textarea>
            </div>
            <button type="submit" class="submit-btn"><i class="fas fa-save"></i> Save CSS</button>
        </form>
    </div>

    <!-- ======== DANGER ZONE ======== -->
    <div class="admin-section" id="danger-section" style="border-color:rgba(255,0,0,0.3)">
        <div class="section-header" style="color:#ff6b6b;border-color:rgba(255,0,0,0.2)">
            <i class="fas fa-exclamation-triangle"></i> DANGER ZONE
        </div>
        <p style="color:rgba(255,255,255,0.4);font-size:.85rem;margin-bottom:20px;">
            This will reset ALL data to defaults. This action cannot be undone!
        </p>
        <form method="POST" action="/admin/reset"
              onsubmit="return confirm('⚠️ Are you sure? This will reset EVERYTHING to defaults!')">
            <button type="submit" class="submit-btn" style="background:linear-gradient(135deg,#ff0000,#cc0000)">
                <i class="fas fa-trash-alt"></i> Reset All Data
            </button>
        </form>
    </div>

    <!-- FOOTER -->
    <div style="text-align:center;padding:30px;font-size:.7rem;color:rgba(255,255,255,0.2);letter-spacing:2px;">
        RuhibioQNR Admin Panel • Built with 💖
    </div>
</div>

<script>
    // Smooth scroll for sidebar links
    document.querySelectorAll('.sidebar-menu a[href^="#"]').forEach(a=>{
        a.addEventListener('click',function(e){
            e.preventDefault();
            const target=document.querySelector(this.getAttribute('href'));
            if(target){
                target.scrollIntoView({behavior:'smooth',block:'start'});
                // Update active
                document.querySelectorAll('.sidebar-menu a').forEach(l=>l.classList.remove('active'));
                this.classList.add('active');
                // Close mobile sidebar
                document.querySelector('.sidebar').classList.remove('open');
            }
        });
    });

    // Auto-hide flash messages
    setTimeout(()=>{
        document.querySelectorAll('.flash-msg').forEach(m=>{
            m.style.transition='opacity 0.5s';
            m.style.opacity='0';
            setTimeout(()=>m.remove(),500);
        });
    },4000);
</script>
</body>
</html>
'''

# ============================================================
# RUN THE APPLICATION
# ============================================================

if __name__ == '__main__':
    print(r"""
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║   💖  RuhibioQNR - Bio Link Portfolio Server  💖     ║
    ║                                                      ║
    ║   🌸 Bio Page:    http://RuhibioQNR:5000             ║
    ║   🔐 Admin Panel: http://RuhibioQNR:5000/admin       ║
    ║                                                      ║
    ║   📧 Admin Email:    RUHIVIG@BIO.COM                 ║
    ║   🔑 Admin Password: RUHIVIGQNR                     ║
    ║                                                      ║
    ║   Press CTRL+C to quit                               ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)

    # Try to set custom server name display
    # The app runs on 0.0.0.0:5000 but we print custom branding
    print(" * Running on all addresses (0.0.0.0)")
    print(" * Running on http://RuhibioQNR:5000")
    print(" * Running on http://localhost:5000")
    print(" * Admin Panel: http://localhost:5000/admin/login")
    print("")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )