import re
from datetime import datetime

from .urls import get_html

URL = "https://www.fut.gg/evolutions/"


def _extract_blocks(html):
    """Extract individual evolution blocks from the SSR-dehydrated HTML."""
    pattern = r'\{id:\d+,game:"26",eaId:\d+,url:"/evolutions/'
    starts = [m.start() for m in re.finditer(pattern, html)]
    blocks = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else start + 20000
        blocks.append(html[start:end])
    return blocks


def _extract_name(block):
    m = re.search(r'name:"([^"]+)"', block)
    return m.group(1) if m else "Unknown"


def _extract_price(block):
    coins = re.search(r'coinsCost:(\d+)', block)
    points = re.search(r'pointsCost:(\d+)', block)
    coins_val = int(coins.group(1)) if coins else 0
    points_val = int(points.group(1)) if points else 0
    if coins_val == 0 and points_val == 0:
        return "FREE"
    parts = []
    if coins_val > 0:
        parts.append(f"{coins_val:,} Coins")
    if points_val > 0:
        parts.append(f"{points_val:,} Points")
    return " / ".join(parts)


def _extract_requirements(block):
    """Extract non-null requirement fields from the requirements block."""
    reqs = {}
    # The requirements block starts with requirements:$R[N]={ and is very large.
    # We search for specific fields within the block.
    req_start = re.search(r'requirements:\$R\[\d+\]=\{', block)
    if not req_start:
        return reqs

    # Get a large enough section from requirements start
    req_text = block[req_start.start():req_start.start() + 5000]

    field_map = {
        "maxOverall": "Max Overall",
        "minOverall": "Min Overall",
        "maxPlaystyles": "Max Playstyles",
        "maxPlaystylesPlus": "Max Playstyles+",
    }
    for field, label in field_map.items():
        m = re.search(rf'{field}:(\d+)', req_text)
        if m:
            reqs[label] = m.group(1)
    return reqs


def _extract_upgrades(block):
    """Extract upgrade labels and max values from totalUpgradesText."""
    upgrades = {}
    # Find the last totalUpgradesText occurrence in the block
    all_total = list(re.finditer(r'totalUpgradesText:\$R\[\d+\]=\[', block))
    if all_total:
        last = all_total[-1]
        # Extract section until the closing of the array
        section = block[last.start():last.start() + 3000]
        entries = re.findall(
            r'label:"([^"]+)",value:"([^"]*)",maxValue:"([^"]*)"', section
        )
        for label, value, max_value in entries:
            display = max_value if max_value else value
            if display:
                upgrades[label] = display
    return upgrades


def _extract_expiration(block):
    m = re.search(r'endTime:"([^"]+)"', block)
    if m:
        dt_str = m.group(1)
        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return dt_str
    return "-"


def _extract_levels(block):
    levels = re.findall(r'idx:\d+,game:"26",challenges:', block)
    return str(len(levels)) if levels else "0"


def _extract_players(block):
    m = re.search(r'numberOfPlayers:(\d+)', block)
    return m.group(1) if m else "0"


def get_evolution_items():
    """Fetch and parse evolution items from SSR-dehydrated HTML."""
    html = get_html(URL)
    if not html:
        return []

    blocks = _extract_blocks(html)
    evolutions = []

    for block in blocks:
        evolutions.append({
            "Name": _extract_name(block),
            "Price": _extract_price(block),
            "Requirements": _extract_requirements(block),
            "Upgrades": _extract_upgrades(block),
            "Expiration": _extract_expiration(block),
            "Levels": _extract_levels(block),
            "Players": _extract_players(block),
        })

    return evolutions
