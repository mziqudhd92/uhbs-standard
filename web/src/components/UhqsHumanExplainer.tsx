import { useCallback, useEffect, useId, useState } from "react";
import { createPortal } from "react-dom";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowLeft, ArrowRight, Sparkles, X } from "lucide-react";
import { KatexMath } from "./KatexMath";

type Step = {
  id: string;
  eyebrow: string;
  title: string;
  plain: string;
  detail: string;
  tex?: string;
  accent?: "primary" | "danger" | "success";
};

const STEPS: Step[] = [
  {
    id: "what",
    eyebrow: "Step 1 · The big picture",
    title: "UHQS is a quality score from 0 to 100",
    plain:
      "Think of it like a report card for a honeypot (a fake system meant to attract attackers). Higher is better. The goal is a number you can compare across products — not marketing claims.",
    detail:
      "At the end you also get a letter grade (A–F). Organizations often treat UHQS above 80 with a passing safety gate as a practical production baseline.",
    tex: "\\mathrm{UHQS} \\in [0, 100]",
    accent: "primary",
  },
  {
    id: "scores",
    eyebrow: "Step 2 · Grade each area",
    title: "Five skill scores, each from 0 to 100",
    plain:
      "We test the honeypot in separate areas — protocol realism, behavior, logging, speed under load, and code quality. Each area gets its own score S.",
    detail:
      "A = protocol fidelity · B = behavioral realism · C = telemetry · E = scalability · F = static code audit. Module D is special — it shows up next as a safety multiplier, not another addend.",
    tex: "S_{A},\\; S_{B},\\; S_{C},\\; S_{E},\\; S_{F}",
    accent: "primary",
  },
  {
    id: "weights",
    eyebrow: "Step 3 · Decide what matters most",
    title: "Weights say how important each skill is",
    plain:
      "Not every honeypot is judged the same way. An industrial decoy cares more about protocol accuracy; a shell decoy cares more about realistic behavior. Weights (w) are percentages that always add up to 100%.",
    detail:
      "Example: Low-Interaction profiles put more weight on protocol (w_A = 0.30) and less on behavior (w_B = 0.15).",
    tex: "w_{A}+w_{B}+w_{C}+w_{E}+w_{F} = 1",
    accent: "primary",
  },
  {
    id: "blend",
    eyebrow: "Step 4 · Mix the report card",
    title: "Blend scores with those weights",
    plain:
      "Multiply each score by its weight, then add them up. That gives one “everyday quality” number before safety is applied — like a weighted average of the skill grades.",
    detail:
      "If protocol scored 80 with weight 0.30, that part contributes 24 points to the blend. Do that for every module in the parentheses.",
    tex: "\\textit{blend} = w_{A}S_{A}+w_{B}S_{B}+w_{C}S_{C}+w_{E}S_{E}+w_{F}S_{F}",
    accent: "primary",
  },
  {
    id: "gate",
    eyebrow: "Step 5 · The safety gate",
    title: "Containment can shrink (or keep) everything",
    plain:
      "Module D asks: does this honeypot stay sealed? If containment is strong (score ≥ 95), the safety multiplier is 1 — full credit. If it leaks or can be escaped, the multiplier drops below 1 and can cut the score harshly.",
    detail:
      "Below 95, δ_C = (C/100)². Example: C = 90 → 0.81 (−19%). A beautiful but unsafe decoy should not look “good” on paper.",
    tex: "\\delta_{C} = \\begin{cases} 1 & C \\ge 95 \\\\ (C/100)^{2} & C < 95 \\end{cases}",
    accent: "danger",
  },
  {
    id: "result",
    eyebrow: "Step 6 · The result",
    title: "Multiply — that is the final UHQS",
    plain:
      "Take the blended skill score and multiply by the safety gate. Safe and realistic → high UHQS. Unsafe → the number falls, even if other modules looked great.",
    detail:
      "UHQS is rounded to two decimals, then mapped to a letter grade. That single number is what the Results cards show.",
    tex: "\\mathrm{UHQS} = \\delta_{C} \\times \\textit{blend}",
    accent: "success",
  },
];

const ease = [0.22, 1, 0.36, 1] as const;

type Props = {
  open: boolean;
  onClose: () => void;
};

export function UhqsHumanExplainerModal({ open, onClose }: Props) {
  const titleId = useId();
  const [step, setStep] = useState(0);
  const current = STEPS[step];
  const isLast = step === STEPS.length - 1;

  useEffect(() => {
    if (!open) return;
    setStep(0);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight") setStep((s) => Math.min(STEPS.length - 1, s + 1));
      if (e.key === "ArrowLeft") setStep((s) => Math.max(0, s - 1));
    };
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener("keydown", onKey);
    };
  }, [open, onClose]);

  const next = useCallback(() => {
    if (isLast) onClose();
    else setStep((s) => s + 1);
  }, [isLast, onClose]);

  const back = useCallback(() => setStep((s) => Math.max(0, s - 1)), []);

  if (typeof document === "undefined") return null;

  return createPortal(
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-0 sm:p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.28 }}
        >
          <motion.button
            type="button"
            aria-label="Close explanation"
            className="absolute inset-0 bg-[#05070f]/75 backdrop-blur-[2px]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          <motion.div
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            className="relative z-10 w-full sm:max-w-xl max-h-[92vh] overflow-hidden border border-border bg-card shadow-2xl sm:rounded-sm flex flex-col"
            initial={{ opacity: 0, y: 28, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 16, scale: 0.98 }}
            transition={{ duration: 0.4, ease }}
          >
            <div className="flex items-start justify-between gap-4 px-5 pt-5 pb-3 border-b border-border/60">
              <div>
                <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-primary mb-1.5">
                  Explanation for humans
                </div>
                <h2 id={titleId} className="text-lg font-semibold text-foreground leading-snug">
                  How UHQS quality is built
                </h2>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="shrink-0 p-2 text-muted-foreground hover:text-foreground border border-transparent hover:border-border transition-colors"
                aria-label="Close"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Progress */}
            <div className="px-5 pt-4">
              <div className="flex gap-1.5" aria-hidden>
                {STEPS.map((s, i) => (
                  <motion.div
                    key={s.id}
                    className="h-0.5 flex-1 rounded-full bg-border/80 overflow-hidden"
                  >
                    <motion.div
                      className={
                        current.accent === "danger"
                          ? "h-full bg-danger"
                          : current.accent === "success"
                            ? "h-full bg-success"
                            : "h-full bg-primary"
                      }
                      initial={false}
                      animate={{ width: i <= step ? "100%" : "0%" }}
                      transition={{ duration: 0.45, ease }}
                    />
                  </motion.div>
                ))}
              </div>
              <div className="mt-2 font-mono text-[10px] text-muted-foreground tracking-wide">
                {step + 1} / {STEPS.length}
              </div>
            </div>

            <div className="px-5 py-5 flex-1 overflow-y-auto min-h-[280px]">
              <AnimatePresence mode="wait">
                <motion.div
                  key={current.id}
                  initial={{ opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.38, ease }}
                  className="space-y-4"
                >
                  <motion.p
                    className="font-mono text-[11px] uppercase tracking-wider text-muted-foreground"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.05, duration: 0.35 }}
                  >
                    {current.eyebrow}
                  </motion.p>

                  <motion.h3
                    className="text-xl sm:text-2xl font-semibold text-foreground leading-tight"
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.12, duration: 0.4, ease }}
                  >
                    {current.title}
                  </motion.h3>

                  <motion.p
                    className="text-sm sm:text-[15px] text-secondary-foreground leading-relaxed"
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.22, duration: 0.42, ease }}
                  >
                    {current.plain}
                  </motion.p>

                  {current.tex && (
                    <motion.div
                      className={`uhqs-katex uhqs-katex-display ${
                        current.accent === "danger"
                          ? "uhqs-katex-danger border-danger/30"
                          : current.accent === "success"
                            ? "border-success/30"
                            : ""
                      }`}
                      initial={{ opacity: 0, scale: 0.97 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.34, duration: 0.45, ease }}
                    >
                      <KatexMath display className="block" tex={current.tex} label={current.title} />
                    </motion.div>
                  )}

                  <motion.p
                    className="text-xs text-muted-foreground leading-relaxed border-l-2 border-border pl-3"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.48, duration: 0.4 }}
                  >
                    {current.detail}
                  </motion.p>

                  {isLast && (
                    <motion.div
                      className="mt-2 rounded-sm border border-primary/25 bg-primary/5 px-4 py-3"
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.55, duration: 0.4, ease }}
                    >
                      <p className="text-sm text-foreground leading-relaxed">
                        Safe × skilled = high quality. Unsafe × anything = the score tells you to fix containment first.
                      </p>
                    </motion.div>
                  )}
                </motion.div>
              </AnimatePresence>
            </div>

            <div className="px-5 py-4 border-t border-border/60 flex items-center justify-between gap-3 bg-background/40">
              <button
                type="button"
                onClick={back}
                disabled={step === 0}
                className="inline-flex items-center gap-1.5 font-mono text-xs px-3 py-2 border border-border text-secondary-foreground disabled:opacity-30 hover:border-primary/40 hover:text-primary transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" /> Back
              </button>
              <button
                type="button"
                onClick={next}
                className="inline-flex items-center gap-1.5 font-mono text-xs px-4 py-2 border border-primary bg-primary/15 text-primary hover:bg-primary/25 transition-colors"
              >
                {isLast ? "Done" : "Next"}
                {!isLast && <ArrowRight className="w-3.5 h-3.5" />}
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body,
  );
}

export function UhqsHumanExplainerTrigger() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-wider px-2.5 py-1 border border-primary/40 bg-primary/10 text-primary hover:bg-primary/20 hover:border-primary/60 transition-colors"
      >
        <Sparkles className="w-3 h-3" aria-hidden />
        Explanation for Humans
      </button>
      <UhqsHumanExplainerModal open={open} onClose={() => setOpen(false)} />
    </>
  );
}
