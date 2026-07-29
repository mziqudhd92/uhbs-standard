# Methodology: ssh-honeypotd UHBS lab

**UHBS:** 4.2.2 · Graded **SSH** Low-Interaction auth-logging decoy.  
Runtime: `wildwildangel/ssh-honeypotd:latest`; host inventory maps `127.0.0.1:12023` → container `:22`. Auth always fails (by design) → Module B/E stay low vs session-accepting honeypots.

Quick **44.38 / F**, full **44.38 / F**.
