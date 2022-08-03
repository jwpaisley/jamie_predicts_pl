import os, sys
import requests
import random
from datetime import datetime
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

dirname = os.path.dirname(__file__)

colors = {
    "white": "#ffffff",
    "grey": "#ebecf0",
    "dark_grey": "#222222",
    "green": "#00bf00",
    "red": "#c23b22"
}

def add_date(base, draw):
    font = ImageFont.truetype(os.path.join(dirname, "font.ttf"), 50)
    date = datetime.utcnow().strftime("%Y-%m-%d")
    draw.text((640, 135), date, colors["white"], font=font)

def add_stats(base, draw):
    font = ImageFont.truetype(os.path.join(dirname, "font.ttf"), 50)
    draw.text((1230, 285), "Starting Balance:", colors["grey"], font=font)
    draw.text((1730, 285), "$1171.10", colors["white"], font=font)

    draw.text((1230, 355), "Return:", colors["grey"], font=font)
    draw.text((1707, 355), "+$322.81", colors["green"], font=font)

    draw.text((1230, 425), "Ending Balance:", colors["grey"], font=font)
    draw.text((1730, 425), "$1493.91", colors["white"], font=font)

    draw.text((1230, 495), "Return Percentage:", colors["grey"], font=font)
    draw.text((1707, 495), "+27.5%", colors["green"], font=font)

    draw.text((1230, 635), "Result Accuracy:", colors["grey"], font=font)
    draw.text((1230, 705), "Score Accuracy:", colors["grey"], font=font)
    draw.text((1230, 775), ":", colors["grey"], font=font)
    draw.text((1230, 845), "Return Percentage:", colors["grey"], font=font)
    draw.text((1230, 915), "Return Percentage:", colors["grey"], font=font)
    draw.text((1230, 985), "Return Percentage:", colors["grey"], font=font)
    draw.text((1230, 1055), "Return Percentage:", colors["grey"], font=font)
    draw.text((1230, 1125), "Return Percentage:", colors["grey"], font=font)
    draw.text((1230, 1195), "Return Percentage:", colors["grey"], font=font)

def add_table(base, draw):
    table_row_colors = [colors["white"], colors["grey"]]
    for idx in range(10):
        draw.rectangle([(100, 465 + (idx * 80)), (1050, 545 + (idx * 80))], fill=table_row_colors[idx % 2])

def add_fixtures(base, draw):
    for idx in range(10):
        # open team crests and paste into final scoreline prediction positions
        home_team_crest = requests.get('https://media.api-sports.io/football/teams/40.png')
        away_team_crest = requests.get('https://media.api-sports.io/football/teams/47.png')
        home_img = Image.open(BytesIO(home_team_crest.content)).convert("RGBA")
        away_img = Image.open(BytesIO(away_team_crest.content)).convert("RGBA")
        home_img = home_img.resize((50, 50), Image.ANTIALIAS)
        away_img = away_img.resize((50, 50), Image.ANTIALIAS)
        
        base.paste(home_img, (120, 480 + (idx * 80)), mask=home_img)
        base.paste(away_img, (380, 480 + (idx * 80)), mask=away_img)

        font = ImageFont.truetype(os.path.join(dirname, "font.ttf"), 25)
        offset = (200 - font.getsize("LIV vs. TOT")[0]) / 2
        draw.text((180 + offset, 490 + (idx * 80)), "LIV vs. TOT", colors["dark_grey"], font=font)

def add_table_data(base, draw):
    for idx in range(10):
        font = ImageFont.truetype(os.path.join(dirname, "font.ttf"), 25)

        offset = (200 - font.getsize("LIV, 3-1")[0]) / 2
        draw.text((430 + offset, 490 + (idx * 80)), "LIV, 3-1", colors["dark_grey"], font=font)

        offset = (200 - font.getsize("LIV, 4-0")[0]) / 2
        draw.text((630 + offset, 490 + (idx * 80)), "LIV, 4-0", colors["dark_grey"], font=font)

        offset = (200 - font.getsize("+$113.37")[0]) / 2
        draw.text((820 + offset, 490 + (idx * 80)), "+$113.37", colors["green"], font=font)

def add_correctness_indicators(base, draw):
    star = Image.open(os.path.join(dirname, "img/star.png")).convert("RGBA")
    star = star.resize((50, 50), Image.ANTIALIAS)

    check = Image.open(os.path.join(dirname, "img/check.png")).convert("RGBA")
    check = check.resize((50, 50), Image.ANTIALIAS)

    x = Image.open(os.path.join(dirname, "img/x.png")).convert("RGBA")
    x = x.resize((50, 50), Image.ANTIALIAS)

    indicators = [star, check, x]
    for idx in range(10):
        correct = random.randrange(0, 3)
        base.paste(indicators[correct], (990, 480 + (idx * 80)), mask=indicators[correct])

def build_results():
    base = Image.open(os.path.join(dirname, "img/results_base.png")).convert("RGBA")
    draw = ImageDraw.Draw(base)

    add_date(base, draw)
    add_table(base, draw)
    add_fixtures(base, draw)
    add_table_data(base, draw)
    add_correctness_indicators(base, draw)
    add_stats(base, draw)
    base.save(os.path.join(dirname, "img/results.png"))

build_results()