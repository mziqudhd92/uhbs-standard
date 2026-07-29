# Methodology: ssh-auth-logger UHBS lab

**UHBS:** 4.2.2 · Graded **SSH** Low/zero-Interaction auth logger.  
Runtime: `justinazoff/ssh-auth-logger:latest` (`SSHD_BIND=:2222`). Host inventory maps `127.0.0.1:12024`. Auth always fails; elevated `SSHD_RATE` avoids tarpit-like banner stalls under 1000-sample Module A.

Quick **44.38 / F**, full **44.38 / F**.
