"""Snake mode."""

from __future__ import annotations

import hashlib
import random
from pathlib import Path
from typing import Any

from readme_arcade.github import counts_from_calendar
from readme_arcade.grid_svg import base_grid, layout, write_theme_svgs
from readme_arcade.modes.lifegrid import FONT_5X7
from readme_arcade.themes import THEMES


Position = tuple[int, int]


SNAKE_COLORS = {
    "dark": {
        "head": "#ff4d8d",
        "jaw": "#facc15",
        "body": "#58a6ff",
        "tail": "#1f6feb",
    },
    "light": {
        "head": "#d6336c",
        "jaw": "#ca8a04",
        "body": "#0969da",
        "tail": "#54aeff",
    },
}


WORM_COLORS = {
    "dark": {
        "head": "#ff9f1c",
        "jaw": "#d2a8ff",
        "body": "#a371f7",
        "tail": "#8957e5",
    },
    "light": {
        "head": "#bf8700",
        "jaw": "#8250df",
        "body": "#8250df",
        "tail": "#a475f9",
    },
}


FOOD_LEVELS = {
    1: "level1",
    2: "level2",
    3: "level3",
    4: "level4",
}


def stable_rng(user: str, salt: str = "") -> random.Random:
    digest = hashlib.sha256(f"{user}:{salt}".encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def stable_byte(user: str, salt: str) -> int:
    return hashlib.sha256(f"{user}:{salt}".encode("utf-8")).digest()[0]


def manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def name_food(user: str, width: int, height: int) -> dict[Position, int]:
    cells: dict[Position, int] = {}
    text = "".join(ch for ch in user.upper() if ch in FONT_5X7)[:8] or "README"
    text_width = (len(text) * 6) - 1
    if text_width > width:
        text = text[: max(1, (width + 1) // 6)]
        text_width = (len(text) * 6) - 1

    x0 = max(0, (width - text_width) // 2)
    y0 = max(0, (height - 7) // 2)
    for index, char in enumerate(text):
        glyph = FONT_5X7[char]
        gx = x0 + index * 6
        for y, row in enumerate(glyph):
            gy = y0 + y
            if gy >= height:
                continue
            for dx, value in enumerate(row):
                x = gx + dx
                if value == "1" and 0 <= x < width:
                    level = 1 + ((stable_byte(user, f"name:{index}:{dx}:{y}") + x + gy) % 4)
                    cells[(x, gy)] = level

    return cells


def name_grid(user: str, width: int, height: int, theme: dict[str, str]) -> list[list[str]]:
    grid = base_grid(theme, width, height)
    for (x, y), level in name_food(user, width, height).items():
        grid[y][x] = theme[f"level{level}"]

    return grid


def neighbor_positions(pos: Position) -> list[Position]:
    x, y = pos
    return [(x + 1, y), (x, y + 1), (x, y - 1), (x - 1, y)]


def body_from_head(
    head: Position,
    length: int,
    width: int,
    height: int,
    blocked: set[Position] | None = None,
    facing: int = 1,
) -> list[Position]:
    hx, hy = head
    occupied = blocked or set()
    horizontal = [(-offset, 0) for offset in range(length)]
    opposite = [(offset, 0) for offset in range(length)]
    if facing < 0:
        horizontal, opposite = opposite, horizontal
    trails = (horizontal, [(0, -offset) for offset in range(length)], [(0, offset) for offset in range(length)], opposite)

    for offsets in trails:
        body = [(hx + dx, hy + dy) for dx, dy in offsets]
        if (
            len(set(body)) == length
            and all(0 <= x < width and 0 <= y < height for x, y in body)
            and not occupied.intersection(body)
        ):
            return body

    return initial_body(width, height, length, hy, hx)


def body_from_name_cells(
    user: str,
    cells: dict[Position, int],
    actor: str,
    length: int,
    width: int,
    height: int,
    used: set[Position] | None = None,
) -> list[Position]:
    blocked = used or set()
    cell_set = set(cells)
    target_x = width // 3 if actor == "snake" else (width * 2) // 3
    target_y = min(height - 1, (height // 2) + 1) if actor == "snake" else max(0, (height // 2) - 2)
    candidates = [pos for pos in cell_set if pos not in blocked]
    candidates.sort(
        key=lambda pos: (
            manhattan(pos, (target_x, target_y)),
            stable_byte(user, f"{actor}:name-path-head:{pos[0]}:{pos[1]}"),
        )
    )

    def ordered_neighbors(pos: Position, path: list[Position]) -> list[Position]:
        options = [neighbor for neighbor in neighbor_positions(pos) if neighbor in cell_set and neighbor not in blocked and neighbor not in path]
        return sorted(
            options,
            key=lambda neighbor: (
                0 if (actor == "snake" and neighbor[0] <= pos[0]) or (actor == "worm" and neighbor[0] >= pos[0]) else 1,
                stable_byte(user, f"{actor}:name-path:{pos[0]}:{pos[1]}:{neighbor[0]}:{neighbor[1]}"),
            ),
        )

    def walk(path: list[Position]) -> list[Position] | None:
        if len(path) == length:
            return path[:]
        for neighbor in ordered_neighbors(path[-1], path):
            path.append(neighbor)
            result = walk(path)
            if result:
                return result
            path.pop()
        return None

    for head in candidates:
        result = walk([head])
        if result:
            return result

    fallback = choose_name_head(user, list(cells), actor, width, height, blocked)
    return body_from_head(fallback, length, width, height, blocked, facing=-1 if actor == "worm" else 1)


def choose_name_head(
    user: str,
    cells: list[Position],
    actor: str,
    width: int,
    height: int,
    used: set[Position] | None = None,
) -> Position:
    blocked = used or set()
    candidates = [pos for pos in cells if pos not in blocked]
    if not candidates:
        return (min(width - 2, max(1, width // 3)), height // 2)

    target_x = width // 3 if actor == "snake" else (width * 2) // 3
    target_y = min(height - 1, (height // 2) + 1) if actor == "snake" else max(0, (height // 2) - 2)
    return min(
        candidates,
        key=lambda pos: (
            manhattan(pos, (target_x, target_y)),
            stable_byte(user, f"{actor}:name-head:{pos[0]}:{pos[1]}"),
        ),
    )


def initial_body(
    width: int,
    height: int,
    length: int,
    row: int | None = None,
    head_x: int | None = None,
    direction: int = 1,
) -> list[Position]:
    y = height // 2 if row is None else min(max(0, row), height - 1)
    if head_x is None:
        head_x = min(width - 3, max(length + 2, 9))
    head_x = min(max(0, head_x), width - 1)
    step = -1 if direction >= 0 else 1
    return [(min(max(0, head_x + offset * step), width - 1), y) for offset in range(length)]


def build_food(user: str, width: int, height: int, calendar: dict | None, blocked: set[Position]) -> dict[Position, int]:
    counts, _total = counts_from_calendar(calendar, width, height)
    food: dict[Position, int] = {}

    for y in range(height):
        for x in range(width):
            pos = (x, y)
            if pos in blocked:
                continue

            count = counts[y][x]
            roll = stable_byte(user, f"snake-food:{x}:{y}")
            if count <= 0 and roll > 76:
                continue

            if count >= 10:
                level = 4
            elif count >= 5:
                level = 3
            elif count >= 2:
                level = 2
            elif count == 1:
                level = 1
            elif roll < 46:
                level = 1
            elif roll < 82:
                level = 2
            elif roll < 106:
                level = 3
            else:
                level = 4

            food[pos] = level

    # Ensure enough dark food exists, so the "eat darkest first" behavior is visible.
    rng = stable_rng(user, "snake-dark-food")
    dark_cells = [pos for pos, level in food.items() if level == 1]
    attempts = 0
    while len(dark_cells) < 18 and attempts < width * height * 2:
        attempts += 1
        pos = (rng.randrange(0, width), rng.randrange(0, height))
        if pos in blocked:
            continue
        food[pos] = 1
        if pos not in dark_cells:
            dark_cells.append(pos)

    return food


def reveal_field_food(
    user: str,
    food: dict[Position, int],
    field_food: dict[Position, int],
    frame: int,
    reveal_frames: int,
    blocked: set[Position],
) -> None:
    threshold = reveal_threshold(frame, reveal_frames)
    for pos, level in field_food.items():
        if pos in blocked or pos in food:
            continue
        if stable_byte(user, f"snake-field:{pos[0]}:{pos[1]}") <= threshold:
            food[pos] = level


def reveal_threshold(frame: int, reveal_frames: int) -> int:
    if reveal_frames <= 0:
        return 255
    return min(255, int(((frame + 1) / reveal_frames) * 255))


def actor_lane_priority(pos: Position, width: int, height: int, actor: str) -> tuple[int, int]:
    x, y = pos
    if actor == "worm":
        zone = 0 if x >= width // 2 else 1
        lane = abs(y - max(0, height // 3))
    else:
        zone = 0 if x < width // 2 else 1
        lane = abs(y - min(height - 1, (height * 2) // 3))
    return zone, lane


def edge_run_target(
    head: Position,
    food: dict[Position, int],
    actor: str,
    width: int,
    height: int,
    frame: int,
    delay: int,
    run_frames: int,
) -> Position | None:
    if run_frames <= 0 or frame < delay or frame >= delay + run_frames:
        return None

    row = 0 if actor == "snake" else height - 1
    row_food = [pos for pos in food if pos[1] == row]
    if len(row_food) < 3:
        return None

    direction = 1 if actor == "snake" else -1
    if head[1] == row:
        next_pos = (head[0] + direction, row)
        if next_pos in food:
            return next_pos

    if actor == "snake":
        forward = [pos for pos in row_food if pos[0] > head[0]]
        candidates = forward or row_food
        return min(candidates, key=lambda pos: (abs(pos[0] - head[0]), pos[0]))

    forward = [pos for pos in row_food if pos[0] < head[0]]
    candidates = forward or row_food
    return min(candidates, key=lambda pos: (abs(pos[0] - head[0]), -pos[0]))


def edge_run_active(frame: int, delay: int, run_frames: int) -> bool:
    return run_frames > 0 and delay <= frame < delay + run_frames


def feed_next_edge_cell(
    user: str,
    food: dict[Position, int],
    body: list[Position],
    actor: str,
    width: int,
    height: int,
    frame: int,
    delay: int,
    run_frames: int,
    blocked: set[Position],
) -> None:
    if not edge_run_active(frame, delay, run_frames):
        return

    head = body[0]
    row = 0 if actor == "snake" else height - 1
    if head[1] != row:
        return

    direction = 1 if actor == "snake" else -1
    pos = (head[0] + direction, row)
    if 0 <= pos[0] < width and pos not in blocked:
        food.setdefault(pos, 1 + (stable_byte(user, f"{actor}:edge-step-food:{pos[0]}:{pos[1]}") % 4))


def choose_target(
    user: str,
    head: Position,
    food: dict[Position, int],
    theme_name: str,
    actor: str,
    width: int,
    height: int,
    frame: int,
    edge_run_delay: int,
    edge_run_frames: int,
) -> Position | None:
    if not food:
        return None

    target = edge_run_target(head, food, actor, width, height, frame, edge_run_delay, edge_run_frames)
    if target:
        return target

    def darkness_priority(level: int) -> int:
        return level if theme_name == "dark" else 5 - level

    return min(
        food,
        key=lambda pos: (
            darkness_priority(food[pos]),
            *actor_lane_priority(pos, width, height, actor),
            manhattan(head, pos),
            stable_byte(user, f"{actor}:target:{pos[0]}:{pos[1]}"),
        ),
    )


def choose_step(
    user: str,
    frame: int,
    actor: str,
    head: Position,
    target: Position | None,
    body: list[Position],
    width: int,
    height: int,
    blocked: set[Position] | None = None,
    last_direction: tuple[int, int] | None = None,
    direction_run: int = 0,
) -> Position:
    if target is None:
        target = ((head[0] + 7) % width, (head[1] + 3) % height)

    current_dir = (head[0] - body[1][0], head[1] - body[1][1]) if len(body) > 1 else (1, 0)
    straight_run = straight_run_length(body)
    directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    body_block = set(body[:-1])
    if blocked:
        body_block.update(blocked)
    candidates: list[tuple[tuple[int, int, int, int, int, int], Position]] = []
    current_distance = manhattan(head, target)
    phase_size = 2 if actor == "worm" else 3
    phase = frame // phase_size
    turn_window = stable_byte(user, f"{actor}:turn-window:{phase}:{head[0]}:{head[1]}") < (205 if actor == "worm" else 185)
    weave_y = stable_byte(user, f"{actor}:weave-y:{phase}") % height
    weave_x = stable_byte(user, f"{actor}:weave-x:{phase}") % width

    edge_target = target[1] in (0, height - 1)
    if current_distance <= 2 or edge_target:
        steering_target = target
    elif actor == "worm":
        steering_target = (max(width // 2, weave_x), weave_y)
    else:
        steering_target = (min((width // 2) - 1, weave_x), weave_y)

    for dx, dy in directions:
        nx = head[0] + dx
        ny = head[1] + dy
        if not (0 <= nx < width and 0 <= ny < height):
            continue
        pos = (nx, ny)
        if pos in body_block:
            continue

        next_distance = manhattan(pos, target)
        progress_penalty = 0 if next_distance <= current_distance else 2
        if edge_target and next_distance > current_distance:
            progress_penalty += 8
        turn_penalty = 4 if (dx, dy) == current_dir else 0
        if not turn_window:
            turn_penalty = 0 if (dx, dy) == current_dir else 2
        if straight_run >= 3 and (dx, dy) == current_dir:
            turn_penalty += 14
        if last_direction and direction_run >= 4 and (dx, dy) == last_direction:
            progress_penalty += 8
            turn_penalty += 18
        edge_penalty = 3 if nx in (0, width - 1) or ny in (0, height - 1) else 0
        weave_score = manhattan(pos, steering_target)
        wiggle = stable_byte(user, f"{actor}:move:{frame}:{nx}:{ny}") % 5
        candidates.append(((progress_penalty, turn_penalty, weave_score, next_distance // 2, edge_penalty, wiggle), pos))

    if candidates:
        return min(candidates, key=lambda item: item[0])[1]

    # Last-resort fallback keeps the animation alive even if the snake boxes itself in.
    for dx, dy in directions:
        nx = head[0] + dx
        ny = head[1] + dy
        if 0 <= nx < width and 0 <= ny < height:
            return (nx, ny)

    return head


def straight_run_length(body: list[Position]) -> int:
    if len(body) < 3:
        return 1

    direction = (body[0][0] - body[1][0], body[0][1] - body[1][1])
    run = 1
    for index in range(1, min(len(body) - 1, 5)):
        step = (body[index - 1][0] - body[index][0], body[index - 1][1] - body[index][1])
        if step != direction:
            break
        run += 1
    return run


def advance_actor(
    user: str,
    actor: str,
    frame: int,
    body: list[Position],
    food: dict[Position, int],
    width: int,
    height: int,
    theme_name: str,
    max_length: int,
    grow_per_food: int,
    growth: int,
    blocked: set[Position] | None = None,
    last_direction: tuple[int, int] | None = None,
    direction_run: int = 0,
    edge_run_frame: int = 0,
    edge_run_delay: int = 0,
    edge_run_frames: int = 0,
) -> tuple[int, tuple[int, int], int]:
    target = choose_target(user, body[0], food, theme_name, actor, width, height, edge_run_frame, edge_run_delay, edge_run_frames)
    previous_head = body[0]
    next_head = choose_step(
        user,
        frame,
        actor,
        previous_head,
        target,
        body,
        width,
        height,
        blocked,
        last_direction,
        direction_run,
    )
    next_direction = (next_head[0] - previous_head[0], next_head[1] - previous_head[1])
    next_run = direction_run + 1 if last_direction == next_direction else 1
    body.insert(0, next_head)

    if next_head in food:
        del food[next_head]
        growth += grow_per_food

    if growth > 0 and len(body) <= max_length:
        growth -= 1
    else:
        body.pop()

    del body[max_length:]
    return growth, next_direction, next_run


def paint_actor(grid: list[list[str]], colors: dict[str, str], body: list[Position]) -> None:
    for offset, (x, y) in enumerate(reversed(body)):
        grid[y][x] = colors["tail"]
        if offset > len(body) // 3:
            grid[y][x] = colors["body"]

    if len(body) > 1:
        nx, ny = body[1]
        grid[ny][nx] = colors["jaw"]

    hx, hy = body[0]
    grid[hy][hx] = colors["head"]


def paint_actor_partial(grid: list[list[str]], colors: dict[str, str], body: list[Position], visible: int) -> None:
    visible = min(max(0, visible), len(body))
    if visible <= 0:
        return

    visible_cells = list(reversed(body))[:visible]
    for offset, (x, y) in enumerate(visible_cells):
        grid[y][x] = colors["tail"]
        if offset > max(0, len(body) // 3):
            grid[y][x] = colors["body"]

    if len(body) > 1 and body[1] in visible_cells:
        nx, ny = body[1]
        grid[ny][nx] = colors["jaw"]

    if body[0] in visible_cells:
        hx, hy = body[0]
        grid[hy][hx] = colors["head"]


def render_game_frame(
    theme: dict[str, str],
    actors: list[tuple[dict[str, str], list[Position]]],
    width: int,
    height: int,
    food: dict[Position, int],
) -> list[list[str]]:
    grid = base_grid(theme, width, height)

    for (x, y), level in food.items():
        grid[y][x] = theme[FOOD_LEVELS[level]]

    for colors, body in actors:
        paint_actor(grid, colors, body)

    return grid


def render_birth_frame(
    user: str,
    theme: dict[str, str],
    actors: list[tuple[dict[str, str], list[Position], float]],
    width: int,
    height: int,
    food: dict[Position, int],
    frame: int,
    total_frames: int,
) -> list[list[str]]:
    grid = name_grid(user, width, height, theme)
    progress = (frame + 1) / max(1, total_frames)

    for (x, y), level in food.items():
        if grid[y][x] == theme["level0"]:
            grid[y][x] = theme[FOOD_LEVELS[level]]

    for colors, body, delay in actors:
        local_progress = max(0.0, min(1.0, (progress - delay) / max(0.01, 1.0 - delay)))
        visible = int(round(local_progress * len(body)))
        paint_actor_partial(grid, colors, body, visible)

    return grid


def build_frames(user: str, options: dict[str, Any], calendar: dict | None, theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    snake_colors = dict(SNAKE_COLORS[theme_name])
    worm_colors = dict(WORM_COLORS[theme_name])
    if theme_name == "dark" and options.get("headColorDark"):
        snake_colors["head"] = str(options["headColorDark"])
    if theme_name == "light" and options.get("headColorLight"):
        snake_colors["head"] = str(options["headColorLight"])

    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 120))
    intro_frames = min(max(1, int(options.get("holdFrames", 12))), frames - 1)
    birth_frames = min(max(0, int(options.get("birthFrames", options.get("transitionFrames", 14)))), frames - intro_frames - 1)
    field_reveal_frames = max(1, int(options.get("fieldRevealFrames", 14)))
    edge_run_delay = max(0, int(options.get("edgeRunDelay", 8)))
    edge_run_frames = max(0, int(options.get("edgeRunFrames", 28)))
    start_length = min(max(4, int(options.get("length", 6))), max(4, width - 4))
    max_length = max(start_length, int(options.get("maxLength", 7)))
    grow_per_food = max(0, int(options.get("growPerFood", 0)))
    worm_enabled = bool(options.get("worm", True))
    worm_length = min(max(3, int(options.get("wormLength", 5))), max(3, width - 4))
    worm_max_length = max(worm_length, int(options.get("wormMaxLength", 5)))
    worm_speed = min(max(1, int(options.get("wormSpeed", 2))), 4)
    worm_grow_per_food = max(0, int(options.get("wormGrowPerFood", 0)))

    letter_food = name_food(user, width, height)
    body = body_from_name_cells(user, letter_food, "snake", start_length, width, height)
    worm_body: list[Position] = []
    if worm_enabled:
        worm_body = body_from_name_cells(user, letter_food, "worm", worm_length, width, height, set(body))

    blocked = set(body) | set(worm_body)
    field_food = build_food(user, width, height, calendar, blocked | set(letter_food))
    food = {pos: level for pos, level in letter_food.items() if pos not in blocked}

    rendered: list[list[list[str]]] = [name_grid(user, width, height, theme) for _ in range(intro_frames)]
    birth_actors = [(snake_colors, body, 0.0)]
    if worm_enabled:
        birth_actors.insert(0, (worm_colors, worm_body, 0.18))
    for frame in range(birth_frames):
        reveal_step = min(frame, field_reveal_frames - 1)
        reveal_field_food(user, food, field_food, reveal_step, field_reveal_frames, set(body) | set(worm_body))
        rendered.append(render_birth_frame(user, theme, birth_actors, width, height, food, frame, birth_frames))

    growth = 0
    worm_growth = 0
    snake_direction: tuple[int, int] | None = None
    snake_run = 0
    worm_direction: tuple[int, int] | None = None
    worm_run = 0

    for frame in range(frames - len(rendered)):
        reveal_step = min(birth_frames + frame, field_reveal_frames - 1)
        reveal_field_food(user, food, field_food, reveal_step, field_reveal_frames, set(body) | set(worm_body))
        feed_next_edge_cell(user, food, body, "snake", width, height, frame, edge_run_delay, edge_run_frames, set(worm_body))
        if worm_enabled:
            feed_next_edge_cell(user, food, worm_body, "worm", width, height, frame, edge_run_delay, edge_run_frames, set(body))

        actors = [(worm_colors, worm_body), (snake_colors, body)] if worm_enabled else [(snake_colors, body)]
        rendered.append(render_game_frame(theme, actors, width, height, food))

        before_food = set(food)
        growth, snake_direction, snake_run = advance_actor(
            user,
            "snake",
            frame,
            body,
            food,
            width,
            height,
            theme_name,
            max_length,
            grow_per_food,
            growth,
            set(worm_body),
            snake_direction,
            snake_run,
            frame,
            edge_run_delay,
            edge_run_frames,
        )
        for consumed in before_food - set(food):
            field_food.pop(consumed, None)

        if worm_enabled:
            active_edge_run = edge_run_active(frame, edge_run_delay, edge_run_frames)
            current_worm_speed = 1 if active_edge_run else worm_speed
            for substep in range(current_worm_speed):
                before_food = set(food)
                worm_growth, worm_direction, worm_run = advance_actor(
                    user,
                    "worm",
                    (frame * worm_speed) + substep,
                    worm_body,
                    food,
                    width,
                    height,
                    theme_name,
                    worm_max_length,
                    worm_grow_per_food,
                    worm_growth,
                    set(body),
                    worm_direction,
                    worm_run,
                    frame,
                    edge_run_delay,
                    edge_run_frames,
                )
                for consumed in before_food - set(food):
                    field_food.pop(consumed, None)

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    options = dict(config.get("snake", {}))
    options.setdefault("titleLeft", "SNAKE")
    options.setdefault("titleRight", "")
    options.setdefault("duration", "40s")
    options.setdefault("frames", 120)
    options.setdefault("holdFrames", 12)
    options.setdefault("transitionFrames", 14)
    options.setdefault("birthFrames", 14)
    options.setdefault("fieldRevealFrames", 14)
    options.setdefault("edgeRunDelay", 8)
    options.setdefault("edgeRunFrames", 28)
    options.setdefault("length", 6)
    options.setdefault("maxLength", 7)
    options.setdefault("growPerFood", 0)
    options.setdefault("worm", True)
    options.setdefault("wormLength", 5)
    options.setdefault("wormMaxLength", 5)
    options.setdefault("wormSpeed", 2)
    options.setdefault("wormGrowPerFood", 0)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, calendar, "dark"),
        "light": build_frames(user, options, calendar, "light"),
    }
    return write_theme_svgs(config, "snake", options, user, calendar, out_dir, frames_by_theme)
