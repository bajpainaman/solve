# Routing

Every request goes through [skills/skill-router/SKILL.md](skills/skill-router/SKILL.md) first. It picks one lead skill and at most two lenses from its table and overlap rules, holds a one-line catalog of every subskill, and names the next skill to offer when the work is done. Then read only the lead skill's `SKILL.md`; each skill does its own detailed routing after that.

`PLUGIN_ROOT` is the directory that contains this file. All skills sit under `PLUGIN_ROOT/skills/`.

For a quick check from the shell: `"$PLUGIN_ROOT/skills/cdpi/bin/cdpi" route "<request>"` names the cdpi playbook, and `"$PLUGIN_ROOT/skills/solve/bin/templates" match "<request>" --portable` names a solve page template.
