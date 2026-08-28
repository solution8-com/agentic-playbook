#!/bin/bash
# Statusline script for Claude Code
# Row 1: model | 📁 folder:branch | 5h | 7d | +/- lines | worktree
# Row 2: dumb-zone context bar

# Read JSON input from stdin
input=$(cat)

# Extract values using jq
MODEL=$(echo "$input" | jq -r '.model.display_name // "Claude"')
# Trim context-window suffix: "Opus 4.8 (1M context)" / "Opus 4.8 [1m]" -> "Opus 4.8"
MODEL=$(printf '%s' "$MODEL" | sed -E 's/ *[([].*$//')
CONTEXT_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
CONTEXT_USAGE=$(echo "$input" | jq '.context_window.current_usage')

# --- ANSI / color helpers ---
green='\033[0;32m'
yellow='\033[0;33m'
red='\033[0;31m'
reset='\033[0m'
dim='\033[2m'
bold='\033[1m'
cyan='\033[0;36m'
magenta='\033[0;35m'

# --- DUMB-ZONE palette (256-color) ---
# Model quality drops in stages as context fills. Thresholds = % of the window
# at which each stage begins.
CTX_SMART_MAX=40    # below -> SMART   (green)  full capability
CTX_DUMB_MAX=60     # below -> DUMB    (yellow) quality starts to slip
CTX_DANGER_MAX=80   # below -> DANGER  (orange) significant quality loss
#                     >=80  -> COMPACT (red)    near auto-compaction
z_smart='\033[38;5;78m'
z_dumb='\033[38;5;221m'
z_danger='\033[38;5;208m'
z_compact='\033[38;5;196m'

RATE_BLOCKS=6   # width of the 5h / 7d zone bars

# Old-style plain N-block bar: sbar <pct> <blocks>  ->  [■■□□]
sbar() {
    local pct=$1 blocks=${2:-4}
    [ "$pct" -gt 100 ] && pct=100
    [ "$pct" -lt 0 ] && pct=0
    local filled=$(( (pct * blocks + 50) / 100 ))
    [ "$filled" -gt "$blocks" ] && filled=$blocks
    local empty=$(( blocks - filled )) out="[" i
    for ((i=0; i<filled; i++)); do out+="■"; done
    for ((i=0; i<empty;  i++)); do out+="□"; done
    out+="]"
    echo -n "$out"
}

# fmt_tokens <int> — 412000 -> "412k", 1000000 -> "1.0M"
fmt_tokens() {
    local t="${1:-0}"
    if   [ "$t" -ge 1000000 ]; then awk "BEGIN{printf \"%.1fM\", $t/1000000}"
    elif [ "$t" -ge 1000 ];    then awk "BEGIN{printf \"%dk\", $t/1000}"
    else                            printf '%d' "$t"
    fi
}

# zone_color <percentage-start>
zone_color() {
    local p="${1:-0}"
    if   [ "$p" -lt "$CTX_SMART_MAX" ];  then printf '%s' "$z_smart"
    elif [ "$p" -lt "$CTX_DUMB_MAX" ];   then printf '%s' "$z_dumb"
    elif [ "$p" -lt "$CTX_DANGER_MAX" ]; then printf '%s' "$z_danger"
    else                                      printf '%s' "$z_compact"
    fi
}

# zone_label <percentage>
zone_label() {
    local ipct
    ipct=$(printf '%.0f' "${1:-0}")
    if   [ "$ipct" -lt "$CTX_SMART_MAX" ];  then printf '%bSMART%b'   "$z_smart"   "$reset"
    elif [ "$ipct" -lt "$CTX_DUMB_MAX" ];   then printf '%bDUMB%b'    "$z_dumb"    "$reset"
    elif [ "$ipct" -lt "$CTX_DANGER_MAX" ]; then printf '%bDANGER%b'  "$z_danger"  "$reset"
    else                                         printf '%bCOMPACT%b' "$z_compact" "$reset"
    fi
}

# build_zone_bar <percentage> <cells> — zoned bar (solid █ filled / faint ░ empty),
# each cell tinted by its dumb-zone, with │ borders and ┊ boundary markers at 40/60/80.
build_zone_bar() {
    local pct="${1:-0}" total="${2:-25}" filled g start zc
    filled=$(awk "BEGIN{printf \"%d\", ($pct/100)*$total + 0.5}")
    [ "$filled" -gt "$total" ] && filled=$total
    [ "$filled" -lt 0 ] && filled=0
    local out="\033[2m\xe2\x94\x82\033[0m"   # dim left border │
    for (( g=0; g<total; g++ )); do
        start=$(( g * 100 / total ))
        if [ "$start" = "$CTX_SMART_MAX" ] || [ "$start" = "$CTX_DUMB_MAX" ] || [ "$start" = "$CTX_DANGER_MAX" ]; then
            out="${out}\033[2m\xe2\x94\x8a\033[0m"   # faint ┊ boundary
        fi
        zc=$(zone_color "$start")
        if [ "$g" -lt "$filled" ]; then
            out="${out}${zc}\xe2\x96\x88\033[0m"       # solid █
        else
            out="${out}\033[2m${zc}\xe2\x96\x91\033[0m"  # faint ░
        fi
    done
    out="${out}\033[2m\xe2\x94\x82\033[0m"        # dim right border │
    printf '%b' "$out"
}

# --- Row 2: dumb-zone context bar ---
if [ "$CONTEXT_USAGE" != "null" ]; then
    INPUT_TOKENS=$(echo "$CONTEXT_USAGE" | jq -r '.input_tokens // 0')
    CACHE_CREATION=$(echo "$CONTEXT_USAGE" | jq -r '.cache_creation_input_tokens // 0')
    CACHE_READ=$(echo "$CONTEXT_USAGE" | jq -r '.cache_read_input_tokens // 0')
    CURRENT_TOKENS=$((INPUT_TOKENS + CACHE_CREATION + CACHE_READ))
    PERCENT_USED=$((CURRENT_TOKENS * 100 / CONTEXT_SIZE))

    # % number uses the same dumb-zone scale/color as the SMART/DUMB/... label
    CTX_COLOR=$(zone_color "$PERCENT_USED")

    CTX_BAR=$(build_zone_bar "$PERCENT_USED" 25)
    CTX_ZLABEL=$(zone_label "$PERCENT_USED")
    CONTEXT_LINE2="${bold}${cyan}ctx${reset} ${CTX_BAR} ${CTX_COLOR}${PERCENT_USED}%${reset} ${CTX_ZLABEL} ${dim}$(fmt_tokens "$CURRENT_TOKENS")/$(fmt_tokens "$CONTEXT_SIZE")${reset}"
else
    CONTEXT_LINE2="${bold}${cyan}ctx${reset} $(build_zone_bar 0 25) 0%"
fi

# --- Rate-limit segments (Pro/Max only, absent until first API response) ---
rate_segment() {
    local label="$1" raw_pct="$2" resets_at="$3" style="${4:-zone}"
    [ -z "$raw_pct" ] && return
    local pct=${raw_pct%.*} color
    if [ "$pct" -lt 50 ]; then color="\033[0;32m"
    elif [ "$pct" -lt 80 ]; then color="\033[0;33m"
    else color="\033[0;31m"; fi
    local reset_str=""
    if [ -n "$resets_at" ] && [ "$resets_at" != "null" ]; then
        local delta=$((resets_at - $(date +%s)))
        if [ "$delta" -gt 0 ]; then
            local days=$((delta / 86400)) hours=$(( (delta % 86400) / 3600 )) mins=$(( (delta % 3600) / 60 ))
            if [ "$days" -gt 0 ]; then reset_str="${days}d ${hours}h"
            elif [ "$hours" -gt 0 ]; then reset_str="${hours}h ${mins}m"
            else reset_str="${mins}m"; fi
        fi
    fi
    if [ "$style" = "blocks" ]; then
        # Old style: label + plain [■□] bar + % all in one value-color
        printf " | %s%s %s %d%%\033[0m" "$color" "$label" "$(sbar $pct 4)" "$pct"
    else
        # New style: zoned █/░ bar with │ borders
        printf " | %s%s\033[0m %s %s%d%%\033[0m" "$color" "$label" "$(build_zone_bar $pct $RATE_BLOCKS)" "$color" "$pct"
    fi
    [ -n "$reset_str" ] && printf "\033[2m · %s\033[0m" "$reset_str"
}

SESSION_5H_PCT=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
SESSION_5H_RESET=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
SESSION_7D_PCT=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
SESSION_7D_RESET=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')
SESSION_5H_DISPLAY=$(rate_segment "5h" "$SESSION_5H_PCT" "$SESSION_5H_RESET" "blocks")
SESSION_7D_DISPLAY=$(rate_segment "7d" "$SESSION_7D_PCT" "$SESSION_7D_RESET" "blocks")

# --- Folder + git branch — dim folder, magenta branch ---
CWD=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
BRANCH=""
if [ -n "$CWD" ] && git -C "$CWD" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    BRANCH=$(git -C "$CWD" symbolic-ref --short HEAD 2>/dev/null \
             || git -C "$CWD" rev-parse --short HEAD 2>/dev/null)
fi
DIR_DISPLAY=""
if [ -n "$CWD" ]; then
    if [ -n "$BRANCH" ]; then
        DIR_DISPLAY=" | 📁 $(basename "$CWD")${dim}:${reset}${magenta}${BRANCH}${reset}"
    else
        DIR_DISPLAY=" | 📁 $(basename "$CWD")"
    fi
fi

# --- Lines added/removed this session ---
LINES_ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // empty')
LINES_REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // empty')
LINES_DISPLAY=""
if [ -n "$LINES_ADDED" ] || [ -n "$LINES_REMOVED" ]; then
    LINES_DISPLAY=" | ${green}+${LINES_ADDED:-0}${reset} ${red}-${LINES_REMOVED:-0}${reset}"
fi

# --- Worktree indicator — flags base branch / mismatched worktree ---
WORKTREE=$(echo "$input" | jq -r '.workspace.git_worktree // empty')
WT_DISPLAY=""
if [ -n "$WORKTREE" ]; then
    wt_num=$(printf '%s' "$WORKTREE" | grep -oE '[0-9]+' | head -1)
    br_num=$(printf '%s' "$BRANCH" | grep -oE '[0-9]+' | head -1)
    if printf '%s' "$BRANCH" | grep -qiE '^(main|master|M[0-9])'; then
        WT_DISPLAY=" | ${bold}${red}wt:$(basename "$WORKTREE") BASE!${reset}"
    elif [ -n "$wt_num" ] && [ "$wt_num" = "$br_num" ]; then
        WT_DISPLAY=" | ${bold}${green}wt:$(basename "$WORKTREE") ok${reset}"
    else
        WT_DISPLAY=" | ${bold}${yellow}wt:$(basename "$WORKTREE") ?${reset}"
    fi
fi

# --- Terminal width (row-1 wrapping) ---
_COLS_CACHE="$HOME/.claude/.statusline-cols-cache"
COLS_NOW=$COLUMNS
if [ "$COLS_NOW" -ge 60 ] 2>/dev/null; then
    echo "$COLS_NOW" > "$_COLS_CACHE" 2>/dev/null
else
    COLS_NOW=$(cat "$_COLS_CACHE" 2>/dev/null)
    [ "$COLS_NOW" -ge 60 ] 2>/dev/null || COLS_NOW=180
fi

visible_len() {
    printf '%s' "$1" \
      | sed -E $'s/\x1B\\[[0-9;]*m//g' \
      | sed -E 's/\\033\[[0-9;]*m//g' \
      | sed -E 's/\\e\[[0-9;]*m//g' \
      | LC_ALL=en_US.UTF-8 wc -m | tr -d ' \n'
}

# --- Row 1: model | folder:branch | 5h | 7d | +/- | worktree ---
MODEL_DISPLAY="\033[1;36m${MODEL}\033[0m"
ROW1="${MODEL_DISPLAY}${DIR_DISPLAY}${SESSION_5H_DISPLAY}${SESSION_7D_DISPLAY}${LINES_DISPLAY}${WT_DISPLAY}"

# Wrap ROW1 on " | " boundaries only when it exceeds COLS_NOW.
ROW1_WIDTH=$COLS_NOW
_cur_line=""; _cur_len=0
_IFS_SAVE=$IFS
_segments=$(printf '%s' "$ROW1" | sed 's/ | /\x1f/g')
IFS=$'\x1f'
read -ra _SEG_ARR <<< "$_segments"
IFS=$_IFS_SAVE
for _seg in "${_SEG_ARR[@]}"; do
    _seg_len=$(visible_len "$_seg")
    if [ -z "$_cur_line" ]; then
        _cur_line="$_seg"; _cur_len=$_seg_len
    elif [ "$((_cur_len + 3 + _seg_len))" -le "$ROW1_WIDTH" ]; then
        _cur_line="${_cur_line} | ${_seg}"; _cur_len=$((_cur_len + 3 + _seg_len))
    else
        printf '%b\n' "$_cur_line"; _cur_line="$_seg"; _cur_len=$_seg_len
    fi
done
[ -n "$_cur_line" ] && printf '%b\n' "$_cur_line"

# --- Spacer line between row 1 and row 2 ---
printf '⠀\n'

# --- Row 2: dumb-zone context bar ---
printf '%b\n' "$CONTEXT_LINE2"

# Trailing blank line to separate from the harness indicator
printf "⠀\n"
