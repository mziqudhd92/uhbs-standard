import { useEffect, useId, useState } from "react";
import { createPortal } from "react-dom";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { Sparkles, X } from "lucide-react";

/**
 * Plain-language autoplay walkthrough of UHQS.
 * Best practice 2026: for product explainers, prefer Motion timelines + concrete
 * metaphors over Manim/Elucim (those shine for graphs/LaTeX, not non-academic UX).
 */

const SKILLS = [
  { label: "Looks real", hint: "Speaks the protocol correctly" },
  { label: "Acts real", hint: "Behaves like a real system" },
  { label: "Logs well", hint: "Useful, clean alerts" },
  { label: "Stays fast", hint: "Holds up under load" },
  { label: "Clean code", hint: "Safe defaults in the source" },
] as const;

const STEP_MS = 5200;
const ease = [0.22, 1, 0.36, 1] as const;

type StepId = "score" | "skills" | "importance" | "mix" | "safety" | "result";

const STEPS: { id: StepId; title: string; line: string }[] = [
  {
    id: "score",
    title: "One quality number",
    line: "UHQS is a simple score from 0 to 100 for how good a honeypot is. Higher means better.",
  },
  {
    id: "skills",
    title: "We check five everyday skills",
    line: "Each skill gets its own grade. No jargon — just how convincing, useful, and solid the decoy feels.",
  },
  {
    id: "importance",
    title: "Some skills matter more",
    line: "Depending on the honeypot type, we care more about some skills than others — like adjusting volume knobs.",
  },
  {
    id: "mix",
    title: "Those grades become one number",
    line: "We mix the five grades into a single “everyday quality” score before safety is applied.",
  },
  {
    id: "safety",
    title: "Safety can cut the score",
    line: "If the honeypot can leak or be escaped, the whole score shrinks — even if it looked realistic.",
  },
  {
    id: "result",
    title: "That final number is UHQS",
    line: "Safe and skilled → high score. Unsafe → low score, so you fix containment first.",
  },
];

function SceneScore({ reduce }: { reduce: boolean }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-4">
      <motion.div
        className="font-mono text-6xl sm:text-7xl font-bold text-primary tabular-nums"
        initial={reduce ? false : { opacity: 0, scale: 0.85 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.7, ease }}
      >
        <motion.span
          initial={reduce ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          0
        </motion.span>
        <span className="text-muted-foreground mx-2 text-3xl font-normal">→</span>
        <motion.span
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: reduce ? 0 : 0.35, duration: 0.6, ease }}
        >
          100
        </motion.span>
      </motion.div>
      <motion.p
        className="text-sm text-secondary-foreground"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: reduce ? 0 : 0.55 }}
      >
        Like a report card for a fake system meant to attract attackers
      </motion.p>
    </div>
  );
}

function SceneSkills({ reduce }: { reduce: boolean }) {
  return (
    <div className="grid gap-2.5 py-2">
      {SKILLS.map((s, i) => (
        <motion.div
          key={s.label}
          className="flex items-center justify-between gap-3 border border-border/70 bg-background/60 px-3 py-2.5"
          initial={reduce ? false : { opacity: 0, x: -16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: reduce ? 0 : 0.12 + i * 0.28, duration: 0.45, ease }}
        >
          <div>
            <div className="text-sm font-semibold text-foreground">{s.label}</div>
            <div className="text-[11px] text-muted-foreground mt-0.5">{s.hint}</div>
          </div>
          <motion.div
            className="h-1.5 w-20 sm:w-28 rounded-full bg-border overflow-hidden"
            initial={false}
          >
            <motion.div
              className="h-full bg-primary"
              initial={reduce ? { width: "72%" } : { width: "0%" }}
              animate={{ width: `${55 + i * 8}%` }}
              transition={{ delay: reduce ? 0 : 0.3 + i * 0.28, duration: 0.7, ease }}
            />
          </motion.div>
        </motion.div>
      ))}
    </div>
  );
}

function SceneImportance({ reduce }: { reduce: boolean }) {
  const knobs = [
    { label: "Looks real", level: 0.9 },
    { label: "Acts real", level: 0.45 },
    { label: "Logs well", level: 0.7 },
    { label: "Stays fast", level: 0.35 },
    { label: "Clean code", level: 0.55 },
  ];
  return (
    <div className="space-y-3 py-2">
      <p className="text-xs text-muted-foreground font-mono uppercase tracking-wider">
        Example · this honeypot type
      </p>
      {knobs.map((k, i) => (
        <motion.div
          key={k.label}
          className="space-y-1"
          initial={reduce ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: reduce ? 0 : 0.15 + i * 0.2 }}
        >
          <div className="flex justify-between text-xs text-secondary-foreground">
            <span>{k.label}</span>
            <span className="text-primary font-mono">{k.level >= 0.7 ? "matters a lot" : k.level >= 0.5 ? "matters" : "matters less"}</span>
          </div>
          <div className="h-2 rounded-full bg-border overflow-hidden">
            <motion.div
              className="h-full bg-primary/80"
              initial={reduce ? { width: `${k.level * 100}%` } : { width: "8%" }}
              animate={{ width: `${k.level * 100}%` }}
              transition={{ delay: reduce ? 0 : 0.25 + i * 0.2, duration: 0.75, ease }}
            />
          </div>
        </motion.div>
      ))}
    </div>
  );
}

function SceneMix({ reduce }: { reduce: boolean }) {
  return (
    <div className="flex flex-col items-center gap-5 py-6">
      <div className="flex flex-wrap justify-center gap-2">
        {SKILLS.map((s, i) => (
          <motion.span
            key={s.label}
            className="font-mono text-[11px] px-2 py-1 border border-border text-secondary-foreground"
            initial={reduce ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0, scale: [1, 0.92, 1] }}
            transition={{
              delay: reduce ? 0 : 0.1 + i * 0.15,
              duration: 0.7,
              ease,
            }}
          >
            {s.label}
          </motion.span>
        ))}
      </div>
      <motion.div
        className="text-muted-foreground text-sm"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: reduce ? 0 : 1.1 }}
      >
        mix together
      </motion.div>
      <motion.div
        className="border border-primary/40 bg-primary/10 px-8 py-4 text-center"
        initial={reduce ? false : { opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: reduce ? 0 : 1.35, duration: 0.55, ease }}
      >
        <div className="font-mono text-[10px] uppercase tracking-wider text-primary mb-1">Everyday quality</div>
        <div className="text-4xl font-bold text-foreground tabular-nums">72</div>
      </motion.div>
    </div>
  );
}

function SceneSafety({ reduce }: { reduce: boolean }) {
  return (
    <div className="flex flex-col items-center gap-6 py-4">
      <div className="text-center space-y-3">
        <div className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
          Everyday quality
        </div>
        <div className="relative h-16 flex items-center justify-center">
          <motion.div
            className="absolute text-5xl font-bold tabular-nums text-foreground"
            initial={false}
            animate={
              reduce
                ? { opacity: 0 }
                : { opacity: [1, 1, 0], scale: [1, 1, 0.9] }
            }
            transition={{ duration: 1.8, times: [0, 0.55, 1], ease }}
          >
            72
          </motion.div>
          <motion.div
            className="absolute text-5xl font-bold tabular-nums text-danger"
            initial={reduce ? { opacity: 1 } : { opacity: 0, scale: 1.08 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: reduce ? 0 : 1.0, duration: 0.55, ease }}
          >
            58
          </motion.div>
        </div>
      </div>
      <motion.div
        className="max-w-sm text-center text-sm text-secondary-foreground border border-danger/30 bg-danger/5 px-4 py-3"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: reduce ? 0 : 1.25 }}
      >
        Leak or escape risk? The score drops — realism cannot hide a safety problem.
      </motion.div>
    </div>
  );
}

function SceneResult({ reduce }: { reduce: boolean }) {
  return (
    <div className="flex flex-col items-center gap-4 py-6">
      <motion.div
        className="text-center border border-primary/35 bg-primary/10 px-10 py-6"
        initial={reduce ? false : { opacity: 0, scale: 0.92 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, ease }}
      >
        <div className="font-mono text-[10px] uppercase tracking-[0.2em] text-primary mb-2">Final UHQS</div>
        <div className="text-5xl sm:text-6xl font-bold text-foreground tabular-nums">58.00</div>
        <div className="mt-2 font-mono text-sm text-secondary-foreground">Grade D</div>
      </motion.div>
      <motion.p
        className="text-sm text-secondary-foreground text-center max-w-sm leading-relaxed"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: reduce ? 0 : 0.4 }}
      >
        That is the number on the Results cards — one comparable quality signal, with safety baked in.
      </motion.p>
    </div>
  );
}

function StepScene({ id, reduce }: { id: StepId; reduce: boolean }) {
  switch (id) {
    case "score":
      return <SceneScore reduce={reduce} />;
    case "skills":
      return <SceneSkills reduce={reduce} />;
    case "importance":
      return <SceneImportance reduce={reduce} />;
    case "mix":
      return <SceneMix reduce={reduce} />;
    case "safety":
      return <SceneSafety reduce={reduce} />;
    case "result":
      return <SceneResult reduce={reduce} />;
  }
}

type ModalProps = {
  open: boolean;
  onClose: () => void;
};

export function UhqsHumanExplainerModal({ open, onClose }: ModalProps) {
  const titleId = useId();
  const reduce = useReducedMotion() ?? false;
  const [step, setStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const current = STEPS[step];
  const dwell = reduce ? 2200 : STEP_MS;

  useEffect(() => {
    if (!open) return;
    setStep(0);
    setProgress(0);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener("keydown", onKey);
    };
  }, [open, onClose]);

  // Auto-advance — no Next/Back
  useEffect(() => {
    if (!open) return;
    setProgress(0);
    const start = performance.now();
    let raf = 0;
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / dwell);
      setProgress(t);
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    const timer = window.setTimeout(() => {
      if (step >= STEPS.length - 1) {
        onClose();
      } else {
        setStep((s) => s + 1);
      }
    }, dwell);

    return () => {
      cancelAnimationFrame(raf);
      window.clearTimeout(timer);
    };
  }, [open, step, dwell, onClose]);

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
          <button
            type="button"
            aria-label="Close explanation"
            className="absolute inset-0 bg-[#05070f]/80 backdrop-blur-[2px]"
            onClick={onClose}
          />

          <motion.div
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            aria-live="polite"
            className="relative z-10 w-full sm:max-w-lg max-h-[92vh] overflow-hidden border border-border bg-card shadow-2xl sm:rounded-sm flex flex-col"
            initial={{ opacity: 0, y: 24, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 12, scale: 0.98 }}
            transition={{ duration: 0.4, ease }}
          >
            <div className="flex items-start justify-between gap-4 px-5 pt-5 pb-3">
              <div>
                <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-primary mb-1.5">
                  Explanation for humans
                </div>
                <h2 id={titleId} className="text-lg font-semibold text-foreground leading-snug">
                  How the quality score works
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

            <div className="px-5">
              <div className="h-0.5 w-full rounded-full bg-border/80 overflow-hidden" aria-hidden>
                <motion.div
                  className="h-full bg-primary origin-left"
                  style={{ scaleX: (step + progress) / STEPS.length }}
                />
              </div>
              <div className="mt-2 font-mono text-[10px] text-muted-foreground tracking-wide">
                Playing · {step + 1} of {STEPS.length}
              </div>
            </div>

            <div className="px-5 py-5 flex-1 overflow-y-auto min-h-[320px]">
              <AnimatePresence mode="wait">
                <motion.div
                  key={current.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  transition={{ duration: 0.35, ease }}
                  className="space-y-3"
                >
                  <h3 className="text-xl font-semibold text-foreground leading-tight">{current.title}</h3>
                  <p className="text-sm text-secondary-foreground leading-relaxed">{current.line}</p>
                  <StepScene id={current.id} reduce={reduce} />
                </motion.div>
              </AnimatePresence>
            </div>

            <div className="px-5 py-3 border-t border-border/50 bg-background/30">
              <p className="font-mono text-[10px] text-muted-foreground text-center tracking-wide">
                Auto-playing · Esc or ✕ to close
              </p>
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
