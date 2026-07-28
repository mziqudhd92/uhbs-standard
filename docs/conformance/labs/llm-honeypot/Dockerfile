# Optional: bake overlays into cowrie/cowrie.
# Prefer runtime bind-mounts (see TUTORIAL.md) — distroless VOLUME on /etc
# hides files COPY'd into etc/ unless they are remounted at run time.
FROM cowrie/cowrie:latest
COPY --chown=cowrie:cowrie configs/whoami.py /cowrie/cowrie-git/src/cowrie/commands/whoami.py
COPY --chown=cowrie:cowrie configs/llm_prompts.py /cowrie/cowrie-git/src/cowrie/commands/llm_prompts.py
USER cowrie
EXPOSE 2222
