# claudex-sessions

A tiny CLI for [Claude Code](https://claude.com/claude-code) and
[Codex](https://github.com/openai/codex) that lists your sessions, live and
past, and lets you jump to one by typing a few letters.

![claudex-sessions picker](docs/screenshot.png)


`●` green: running (yellow while busy). `○` grey: past session, revivable.
Bold names are ones you set with `/rename`; otherwise the session ID is shown
with Claude's auto-generated title as a hint. Codex threads are tagged `codex`
and show their thread name.

## Install

Requires Python 3.8+ on macOS or Linux. No dependencies.

```sh
git clone https://github.com/galilei-labs/claude-sessions.git
cd claude-sessions
ln -sf "$PWD/claudex-sessions" ~/.local/bin/cs
```

Make sure `~/.local/bin` is on your `PATH`. Use any name you like for the link.

## Usage

```
cs                  interactive picker
cs api              picker with the filter pre-filled
cs -r               pick a past session and revive it (claude --resume / codex resume, in its cwd)
cs -R               same, skipping permissions (--dangerously-skip-permissions /
                    --dangerously-bypass-approvals-and-sandbox)
cs -r -- FLAGS...   anything after -- is passed through to claude / codex
cs --claude         Claude Code sessions only
cs --codex          Codex sessions only (or just type "codex" in the filter)
cs -l               plain list, no interaction
cs --live           running sessions only
cs -n 20            only the 20 most recent past sessions
cs --cwd [QUERY]    print the chosen session's directory
cs --json [QUERY]   sessions as JSON
```

In the picker: type to filter, `↑`/`↓` to move, `Enter` to select, `Esc` to
quit. Every word you type must match, as a substring of the name, title, path
or ID, or as a subsequence of one word (`rfct` finds `refactor`).

**Enter on a live session** brings its Terminal.app or iTerm2 tab to the
front. **Enter on a past session** prints its ID, so it composes:

```sh
claude --resume "$(cs)"
cd "$(cs --cwd)"
```

Focusing is skipped when stdout is captured like this; force it with `-f`.
`-r`/`-R` on a live session focuses it too, since a running session cannot be
resumed twice.

## How it works

Live sessions come from the registry Claude Code keeps in
`~/.claude/sessions/<pid>.json`, filtered to processes that are still alive.
Past sessions come from the transcripts in `~/.claude/projects/`; a small
index in `~/.cache/claudex-sessions/` keeps repeat runs under 0.1 s.

Codex threads come from `~/.codex/state_*.sqlite` (read-only). A thread is
live while a `codex` process holds its lock in `~/.codex/thread-writer-locks/`;
it is matched to its terminal by the working directory of the `codex` process.
