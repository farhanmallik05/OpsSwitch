#!/usr/bin/env python3
"""
Asset Generation Script for Flip the Switch Hackathon Milestone 4 Deliverables.
Generates:
1. assets/blog-cover.png (1000x420)
2. assets/social/post1_sre_warroom_architecture.png
3. assets/social/post2_wispr_flow_voice_engineering.png
4. assets/social/post3_live_incident_resolution_demo.png
5. assets/social/post4_opensource_core_contributions.png
6. assets/social/post5_hackathon_submission_celebration.png
and mirrors social assets to plan/05_SOCIAL_MEDIA_KEYBOARD_TRACK/assets/
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(r"d:\AI-Lab\Hackathon\wemakedev hackathon\Switch Hackathon")
ASSETS_DIR = BASE_DIR / "assets"
SOCIAL_DIR = ASSETS_DIR / "social"
PLAN_SOCIAL_ASSETS = BASE_DIR / "plan" / "05_SOCIAL_MEDIA_KEYBOARD_TRACK" / "assets"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)
SOCIAL_DIR.mkdir(parents=True, exist_ok=True)
PLAN_SOCIAL_ASSETS.mkdir(parents=True, exist_ok=True)

BRAIN_DIR = Path(r"C:\Users\farhan\.gemini\antigravity\brain\336d6acd-112c-45f5-8c7c-22aad496cde3")

RAW_BG = BRAIN_DIR / "blog_cover_bg_1793793767103.jpg"
RAW_POST1 = BRAIN_DIR / "social_post1_opsswitch_1793793822915.jpg"
RAW_POST2 = BRAIN_DIR / "social_post2_wispr_voice_1793793863761.jpg"
RAW_POST3 = BRAIN_DIR / "social_post3_livedemo_1793793961471.jpg"
RAW_POST4 = BRAIN_DIR / "social_post4_opensource_pr_1793793890815.jpg"
RAW_POST5 = BRAIN_DIR / "social_post5_celebration_1793793918131.jpg"

def create_blog_cover():
    target_w, target_h = 1000, 420
    
    if RAW_BG.exists():
        im = Image.open(RAW_BG)
        # Center crop to aspect ratio 1000:420
        im_ratio = im.width / im.height
        target_ratio = target_w / target_h
        
        if im_ratio > target_ratio:
            # Image is wider than needed
            new_w = int(im.height * target_ratio)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        else:
            # Image is taller than needed
            new_h = int(im.width / target_ratio)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
            
        im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    else:
        # Fallback dark background
        im = Image.new("RGB", (target_w, target_h), (15, 23, 42))

    # Convert to RGBA
    im = im.convert("RGBA")
    
    # Create dark gradient overlay for text readability
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    d_overlay = ImageDraw.Draw(overlay)
    
    # Radial/vertical dark slate wash
    for y in range(target_h):
        # Darker at top and bottom, semi-transparent in middle
        alpha = int(120 + 90 * (1.0 - (abs(y - 210) / 210.0)))
        # Make the central band slightly darker for strong typography contrast
        alpha = min(220, alpha + 60)
        d_overlay.line([(0, y), (target_w, y)], fill=(15, 23, 42, alpha))
    
    im = Image.alpha_composite(im, overlay)
    draw = ImageDraw.Draw(im)
    
    # Load fonts
    font_bold = "segoeuib.ttf"
    font_semi = "segoeui.ttf"
    
    try:
        title_font = ImageFont.truetype(font_bold, 44)
        subtitle_font = ImageFont.truetype(font_semi, 20)
        badge_font = ImageFont.truetype(font_bold, 13)
        pill_font = ImageFont.truetype(font_bold, 14)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
        pill_font = ImageFont.load_default()

    # Draw Top Hackathon Badge Pill
    badge_text = "FLIP THE SWITCH HACKATHON 2026  |  WeMakeDevs × Switch"
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    
    bx = (target_w - bw) // 2
    by = 48
    pad_x, pad_y = 18, 7
    draw.rounded_rectangle(
        [(bx - pad_x, by - pad_y), (bx + bw + pad_x, by + bh + pad_y + 2)],
        radius=14,
        fill=(30, 41, 59, 210),
        outline=(255, 137, 94, 200),
        width=1
    )
    draw.text((bx, by), badge_text, font=badge_font, fill=(255, 180, 150))
    
    # Draw Main Title: "Putting AI Agents on Call"
    title_part1 = "Putting AI Agents "
    title_part2 = "on Call"
    
    bb1 = draw.textbbox((0, 0), title_part1, font=title_font)
    bb2 = draw.textbbox((0, 0), title_part2, font=title_font)
    w1 = bb1[2] - bb1[0]
    w2 = bb2[2] - bb2[0]
    total_title_w = w1 + w2
    
    tx = (target_w - total_title_w) // 2
    ty = 120
    
    # Subtle drop shadow
    draw.text((tx + 2, ty + 2), title_part1, font=title_font, fill=(0, 0, 0, 200))
    draw.text((tx + w1 + 2, ty + 2), title_part2, font=title_font, fill=(0, 0, 0, 200))
    
    # Main title text
    draw.text((tx, ty), title_part1, font=title_font, fill=(255, 255, 255))
    draw.text((tx + w1, ty), title_part2, font=title_font, fill=(255, 137, 94)) # Switch Coral

    # Draw Subtitle
    subtitle = "Autonomous SRE War Room in Slack with Switch & Wispr Flow Voice"
    s_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sw = s_bbox[2] - s_bbox[0]
    sx = (target_w - sw) // 2
    sy = 185
    draw.text((sx + 1, sy + 1), subtitle, font=subtitle_font, fill=(0, 0, 0, 180))
    draw.text((sx, sy), subtitle, font=subtitle_font, fill=(203, 213, 225)) # Slate 300

    # Draw Tech Tags Pill Row
    tags = [
        ("• Switch Dual-Room Linking", (255, 137, 94)),
        ("• Wispr Flow Voice Dictation", (180, 130, 255)),
        ("• Zero-Leakage MCP Broker", (56, 189, 248)),
        ("• Human-in-the-Loop Sign-Off", (74, 222, 128))
    ]
    
    total_pills_w = 0
    pill_widths = []
    for tag_text, _ in tags:
        t_box = draw.textbbox((0, 0), tag_text, font=pill_font)
        pw = (t_box[2] - t_box[0]) + 24
        pill_widths.append(pw)
        total_pills_w += pw
    
    spacing = 12
    total_row_w = total_pills_w + spacing * (len(tags) - 1)
    px = (target_w - total_row_w) // 2
    py = 250
    
    for i, (tag_text, col) in enumerate(tags):
        pw = pill_widths[i]
        draw.rounded_rectangle(
            [(px, py), (px + pw, py + 34)],
            radius=8,
            fill=(15, 23, 42, 230),
            outline=col,
            width=1
        )
        t_box = draw.textbbox((0, 0), tag_text, font=pill_font)
        tw = t_box[2] - t_box[0]
        th = t_box[3] - t_box[1]
        text_x = px + (pw - tw) // 2
        text_y = py + (34 - th) // 2 - 2
        draw.text((text_x, text_y), tag_text, font=pill_font, fill=(241, 245, 249))
        px += pw + spacing

    # Bottom Footer branding bar
    footer_text = "Track 01 Flagship: OpsSwitch  |  Team: Algo Alchemist  |  dev.to/farhanmallik"
    f_box = draw.textbbox((0, 0), footer_text, font=badge_font)
    fw = f_box[2] - f_box[0]
    fx = (target_w - fw) // 2
    fy = 360
    draw.text((fx, fy), footer_text, font=badge_font, fill=(148, 163, 184))

    # Accent borders top and bottom
    draw.line([(0, 0), (target_w, 0)], fill=(255, 137, 94), width=3) # Switch Coral accent
    draw.line([(0, target_h - 2), (target_w, target_h - 2)], fill=(138, 43, 226), width=3) # Wispr Purple accent

    # Convert to RGB and save
    final_img = im.convert("RGB")
    out_path = ASSETS_DIR / "blog-cover.png"
    final_img.save(out_path, format="PNG", optimize=True)
    print(f"Saved: {out_path} ({final_img.size})")

def process_social_card(src_path, filename):
    if not src_path.exists():
        print(f"Warning: {src_path} not found")
        return
    im = Image.open(src_path)
    
    # Save to assets/social/
    dest1 = SOCIAL_DIR / filename
    im.save(dest1, format="PNG", optimize=True)
    
    # Mirror to plan/05_SOCIAL_MEDIA_KEYBOARD_TRACK/assets/
    dest2 = PLAN_SOCIAL_ASSETS / filename
    im.save(dest2, format="PNG", optimize=True)
    print(f"Saved social asset: {dest1} & {dest2}")

if __name__ == "__main__":
    create_blog_cover()
    process_social_card(RAW_POST1, "post1_sre_warroom_architecture.png")
    process_social_card(RAW_POST2, "post2_wispr_flow_voice_engineering.png")
    process_social_card(RAW_POST3, "post3_live_incident_resolution_demo.png")
    process_social_card(RAW_POST4, "post4_opensource_core_contributions.png")
    process_social_card(RAW_POST5, "post5_hackathon_submission_celebration.png")
    print("All visual assets successfully generated and synchronized!")
