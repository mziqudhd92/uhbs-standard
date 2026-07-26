import { useEffect, useState, useRef } from "react";
import { motion, useInView, type Variants } from "framer-motion";
import {
  Shield,
  Activity,
  Zap,
  Code,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Terminal,
  Server,
  Box,
  Globe,
  Cpu,
  ArrowRight,
  GitCommit,
  Layers,
  Check,
} from "lucide-react";

const fadeUpVariant: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
};

const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const AnimatedNumber = ({ value, duration = 2 }: { value: number, duration?: number }) => {
  const [current, setCurrent] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (!isInView) return;

    let start = 0;
    const end = value;
    const stepTime = Math.abs(Math.floor((duration * 1000) / end));
    
    const timer = setInterval(() => {
      start += 1;
      setCurrent(start);
      if (start >= Math.floor(end)) {
        clearInterval(timer);
        setCurrent(value);
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [isInView, value, duration]);

  return <span ref={ref}>{current.toFixed(1)}</span>;
};

// Section 1: Hero
const Hero = () => {
  return (
    <section className="relative min-h-[90vh] flex flex-col justify-center pt-24 pb-16 overflow-hidden">
      {/* Decorative background grid elements handled by global CSS background */}
      
      <motion.div 
        className="container mx-auto px-6 relative z-10"
        initial="hidden"
        animate="visible"
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="flex items-center gap-3 mb-8">
          <div className="h-px w-12 bg-primary"></div>
          <span className="font-mono text-primary uppercase tracking-widest text-sm font-semibold">Standard Reference</span>
        </motion.div>
        
        <motion.h1 variants={fadeUpVariant} className="text-5xl md:text-7xl font-bold leading-tight mb-6 max-w-4xl text-foreground font-sans tracking-tight">
          Universal Honeypot Benchmarking Standard <br className="hidden md:block"/>
          <span className="text-muted-foreground font-mono text-4xl md:text-6xl tracking-tighter">(UHBS) v4.0 <span className="text-primary/70">· 2026</span></span>
        </motion.h1>
        
        <motion.p variants={fadeUpVariant} className="text-xl md:text-2xl text-secondary-foreground max-w-3xl mb-12 font-light leading-relaxed">
          An objective, repeatable, and quantitative methodology for benchmarking honeypots, decoys, and deception technology across enterprise and academic environments.
        </motion.p>
        
        <motion.div variants={fadeUpVariant} className="flex flex-wrap gap-4 mt-8">
          {[
            { label: "Protocol-Agnostic", icon: Globe },
            { label: "Quantitative Scoring 0–100", icon: Activity },
            { label: "Six Evaluation Modules", icon: Layers },
            { label: "Production Baseline Standard", icon: Shield }
          ].map((badge, i) => (
            <div key={i} className="flex items-center gap-2 bg-card border border-border px-4 py-2.5 rounded-sm terminal-card">
              <badge.icon className="w-4 h-4 text-primary" />
              <span className="font-mono text-sm text-foreground">{badge.label}</span>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </section>
  );
};

// Section 2: Scope & Applicability
const ScopeAndApplicability = () => {
  return (
    <section id="scope" className="py-24 border-t border-border/50 relative bg-background/50">
      <motion.div 
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          <motion.div variants={fadeUpVariant}>
            <h2 className="text-3xl font-bold mb-6 font-sans flex items-center gap-3">
              <Code className="text-primary w-8 h-8" />
              Purpose & Scope
            </h2>
            <div className="prose prose-invert prose-lg text-secondary-foreground font-light leading-relaxed">
              <p>
                The UHBS v4.0 framework provides a rigorous technical foundation for evaluating the efficacy, safety, and realism of deception assets prior to deployment.
              </p>
              <p className="mt-4">
                Historically, deception technology has been evaluated subjectively. This draft framework introduces a verifiable, deterministic mathematical model designed to expose flaws in protocol state machines, containment boundaries, and behavioral realism.
              </p>
            </div>
            
            <div className="mt-8 bg-primary/5 border-l-4 border-primary/50 p-6">
              <div className="flex items-start gap-4">
                <Shield className="w-6 h-6 text-primary shrink-0 mt-1" />
                <div>
                  <h4 className="text-primary font-semibold font-mono mb-2 uppercase tracking-wide text-sm">Draft Evaluation Framework</h4>
                  <p className="text-secondary-foreground text-sm">
                    UHBS v4.0 is a personal open-source project: a vendor-neutral, mathematically reproducible draft framework for comparing and grading honeypots and deception technology by class and protocol — not a consortium or multi-party standards body.
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6 border border-danger/40 bg-danger/5 p-5 flex gap-4 items-start">
              <AlertTriangle className="w-6 h-6 text-danger shrink-0 mt-0.5" />
              <div>
                <h4 className="font-mono text-danger text-xs uppercase tracking-wider mb-2">Suggested Production Baseline</h4>
                <p className="text-sm text-secondary-foreground leading-relaxed">
                  Organizations <span className="text-foreground font-semibold">MAY</span> use UHBS as an internal evaluation gate. It is <span className="text-foreground font-semibold">RECOMMENDED</span> that active decoys meet <span className="text-foreground font-semibold">UHQS &gt; 80</span> with a passing Safety Gate before production deployment — a draft recommendation, not a mandate from any standards body. Failure to meet that baseline can increase lateral-movement risk from compromised containment shells.
                </p>
              </div>
            </div>
          </motion.div>
          
          <motion.div variants={fadeUpVariant}>
            <h3 className="text-xl font-mono mb-8 text-foreground/80 border-b border-border pb-4">Universal Applicability Matrix</h3>
            
            <div className="space-y-6">
              {[
                { title: "Standard IT Services", desc: "SSH, Telnet, HTTP/S, RDP, SMB, FTP, DB RPCs", icon: Server },
                { title: "Industrial OT/ICS", desc: "Modbus TCP, DNP3, EtherNet/IP, BACnet, S7comm", icon: Cpu },
                { title: "Next-Gen AI & Generative Decoys", desc: "LLM-backed shells, dynamic synthetic filesystems", icon: Box },
                { title: "Cloud & SaaS Control Planes", desc: "Public-cloud control-plane APIs, container orchestration, OAuth / identity", icon: Globe }
              ].map((cat, i) => (
                <div key={i} className="flex gap-4 items-center bg-card p-4 border border-border/50 hover:border-primary/50 transition-colors group">
                  <div className="w-12 h-12 bg-background flex items-center justify-center border border-border group-hover:border-primary transition-colors">
                    <cat.icon className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-foreground">{cat.title}</h4>
                    <p className="font-mono text-xs text-muted-foreground mt-1">{cat.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
};

// Section 3: Core Architecture
const CoreArchitecture = () => {
  return (
    <section id="architecture" className="py-24 border-t border-border/50">
      <motion.div 
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4">Dual-Plane Audit Philosophy</h2>
          <p className="text-secondary-foreground max-w-2xl mx-auto">Evaluating deception technology requires orthogonal approaches: inspecting the static blueprint and attacking the running instance.</p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <motion.div variants={fadeUpVariant} className="bg-card border border-border p-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Code className="w-32 h-32 text-primary" />
            </div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30 text-primary font-mono text-sm">1</div>
              <h3 className="text-2xl font-bold">White-Box Static Audit</h3>
            </div>
            <p className="text-secondary-foreground mb-6 h-20">Deep codebase and configuration analysis before deployment to identify intrinsic vulnerabilities.</p>
            <ul className="space-y-3 font-mono text-sm text-foreground/80">
              <li className="flex items-center gap-2"><Check className="w-4 h-4 text-success" /> Static Credentials Detection</li>
              <li className="flex items-center gap-2"><Check className="w-4 h-4 text-success" /> State Machine Logic Flaws</li>
              <li className="flex items-center gap-2"><Check className="w-4 h-4 text-success" /> GenAI Prompt Extraction Risks</li>
              <li className="flex items-center gap-2"><Check className="w-4 h-4 text-success" /> Dependency Vulnerabilities</li>
            </ul>
          </motion.div>
          
          <motion.div variants={fadeUpVariant} className="bg-card border border-border p-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Zap className="w-32 h-32 text-danger" />
            </div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-full bg-danger/20 flex items-center justify-center border border-danger/30 text-danger font-mono text-sm">2</div>
              <h3 className="text-2xl font-bold">Dynamic Adversarial Probing</h3>
            </div>
            <p className="text-secondary-foreground mb-6 h-20">Live-fire testing of the honeypot in an isolated sandbox simulating advanced persistent threat behaviors.</p>
            <ul className="space-y-3 font-mono text-sm text-foreground/80">
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-danger" /> Network-Level Header Anomalies</li>
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-danger" /> Protocol-Level Stress Fuzzing</li>
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-danger" /> Execution-Level Escape Attempts</li>
              <li className="flex items-center gap-2"><ArrowRight className="w-4 h-4 text-danger" /> Out-of-Band Egress Sweeps</li>
            </ul>
          </motion.div>
        </div>
        
        <motion.div variants={fadeUpVariant} className="border border-border/50 bg-background p-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <span className="font-mono text-sm text-muted-foreground uppercase tracking-wider">Prerequisite Environments</span>
          <div className="flex flex-wrap gap-4">
            <span className="px-3 py-1 bg-secondary text-secondary-foreground text-xs font-mono border border-border/50">Air-Gapped Sandbox</span>
            <span className="px-3 py-1 bg-secondary text-secondary-foreground text-xs font-mono border border-border/50">Gold Baseline System</span>
            <span className="px-3 py-1 bg-secondary text-secondary-foreground text-xs font-mono border border-border/50">Target Profile Specification (TPS)</span>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
};

// Section 4: Six Evaluation Modules
const EvaluationModules = () => {
  const modules = [
    {
      letter: "A", name: "Protocol & Syntax Fidelity", color: "text-cyan", border: "border-cyan/30",
      obj: "Measure protocol header parity and state machine correctness.",
      steps: ["FSM inspection", "Header parity comparison", "Statistical side-channel analysis"]
    },
    {
      letter: "B", name: "Behavioral & Stateful Realism", color: "text-blue-400", border: "border-blue-400/30",
      obj: "Evaluate how closely the decoy mimics persistent complex interactions.",
      steps: ["Cross-session state persistence", "Payload handling depth", "Input stress fuzzing"]
    },
    {
      letter: "C", name: "Telemetry Quality & Resilience", color: "text-indigo-400", border: "border-indigo-400/30",
      obj: "Ensure high-signal alert generation and pipeline integrity.",
      steps: ["STIX 2.1 / ECS schema conformance", "Log injection resistance", "Event correlation latency"]
    },
    {
      letter: "D", name: "Safety, Containment & Boundary", color: "text-danger", border: "border-danger",
      obj: "Verify isolation controls and prevent adversarial leverage.",
      steps: ["OOB egress sweeps", "Container escape / LPE checks", "GenAI prompt injection audit"],
      alert: "Critical Safety Gate"
    },
    {
      letter: "E", name: "Scalability & Latency Stress", color: "text-warning", border: "border-warning/30",
      obj: "Determine performance degradation under heavy adversarial probing.",
      steps: ["Connection saturation", "Resource exhaustion tests", "P95 Latency profiling (<150ms)"]
    },
    {
      letter: "F", name: "White-Box Static Code Audit", color: "text-success", border: "border-success/30",
      obj: "Identify intrinsic code flaws before deployment.",
      steps: ["SAST tool scanning (static analysis)", "Hardcoded key detection", "Code coverage & logic review"]
    }
  ];

  return (
    <section id="modules" className="py-24 border-t border-border/50 bg-[#0f1629]">
      <motion.div 
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4 flex items-center gap-3">
            <Layers className="text-primary w-8 h-8" />
            Six Evaluation Modules
          </h2>
          <p className="text-secondary-foreground">The modular assessment framework for computing the final UHQS score.</p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {modules.map((m, i) => (
            <motion.div key={i} variants={fadeUpVariant} className={`bg-background border ${m.border} p-6 flex flex-col h-full hover:-translate-y-1 transition-transform duration-300 relative`}>
              {m.alert && (
                <div className="absolute top-0 right-0 bg-danger text-danger-foreground text-xs font-bold px-3 py-1 uppercase tracking-wider font-mono">
                  {m.alert}
                </div>
              )}
              
              <div className="flex items-baseline gap-4 mb-4">
                <span className={`text-5xl font-bold font-mono opacity-20 ${m.color}`}>{m.letter}</span>
                <h3 className="text-lg font-bold leading-tight flex-1 pt-2">{m.name}</h3>
              </div>
              
              <p className="text-sm text-secondary-foreground mb-6 flex-1 min-h-[40px]">{m.obj}</p>
              
              <div className="space-y-2 mt-auto border-t border-border/50 pt-4">
                {m.steps.map((step, idx) => (
                  <div key={idx} className="flex gap-2 items-start text-xs font-mono text-muted-foreground">
                    <span className="text-primary opacity-50 mt-0.5">›</span>
                    <span>{step}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </section>
  );
};

// Section 5: 5-Dimension Framework Comparison
const FiveDimensionComparison = () => {
  const mappingRows = [
    {
      dim: "Fingerprinting Resistance",
      module: "Module A",
      moduleName: "Protocol & Syntax Fidelity",
      color: "text-cyan-400",
      expansion: "Adds statistical Inter-Arrival Time (IAT) side-channel testing via Kolmogorov-Smirnov distribution test and strict finite state machine (FSM) validation.",
    },
    {
      dim: "Interaction",
      module: "Module B",
      moduleName: "Behavioral & Stateful Realism",
      color: "text-blue-400",
      expansion: "Evaluates dynamic cross-session state persistence (100% state modification retention) and non-UTF8 binary fuzzing.",
    },
    {
      dim: "Data Quality",
      module: "Module C",
      moduleName: "Telemetry Quality & Pipeline Resilience",
      color: "text-indigo-400",
      expansion: "Enforces 100% schema compliance against STIX 2.1, OpenTelemetry, and ECS standards, and tests SIEM log-parser injection resistance.",
    },
    {
      dim: "Stealth & Containment",
      module: "Module D",
      moduleName: "Safety, Containment & Boundary Controls",
      color: "text-danger",
      expansion: "Upgraded from a simple score into a Non-Linear Safety Gate (δ_C) with out-of-bound egress sweeps and exponential penalty on breach.",
    },
    {
      dim: "Resource Efficiency",
      module: "Module E",
      moduleName: "Scalability, Latency & Stress Performance",
      color: "text-warning",
      expansion: "Enforces strict response percentile cutoffs (P95 < 150ms) under load and tests circuit-breaker recovery under memory flooding.",
    },
    {
      dim: "— Not Covered —",
      module: "Module F",
      moduleName: "White-Box Static Code Audit",
      color: "text-success",
      expansion: "New in UHBS v4.0: Scans repository code, container build manifests, and system prompts for SAST flaws, default keys, and unhandled command stubs.",
      isNew: true,
    },
  ];

  const differences = [
    {
      num: "01",
      title: "Dual-Plane Audit vs. Runtime-Only",
      left: { label: "5-Dimension Framework", text: "Functions purely as an operational runtime framework, observing honeypot behavior during active exposure." },
      right: { label: "UHBS v4.0", text: "Employs a Dual-Plane Audit Philosophy — requires pre-deployment static code analysis (Module F) to catch hardcoded SSH keys, static seeds, or vulnerable command wrappers before dynamic sandbox probing begins." },
    },
    {
      num: "02",
      title: "Non-Linear Safety Gate vs. Linear Averaging",
      left: { label: "5-Dimension Framework", text: "Aggregates metrics using simple linear weighted averages. A high interaction score can mask a serious containment flaw, allowing dangerous decoys to pass evaluation." },
      right: { label: "UHBS v4.0", text: "Implements a strict Safety Gate Multiplier (δ_C). If Module D containment drops below 95/100, an exponential penalty degrades the entire UHQS score regardless of performance elsewhere." },
    },
    {
      num: "03",
      title: "Profile-Adaptive Context (TPS) vs. Static Metrics",
      left: { label: "5-Dimension Framework", text: "Applies identical static metric weights across all honeypot classes — a SCADA PLC and an SSH shell are evaluated with the same emphasis." },
      right: { label: "UHBS v4.0", text: "Mandatory Target Profile Specification (profile.yaml) dynamically adjusts evaluation weights. Industrial/OT profiles weight protocol fidelity at w_A = 0.35, while POSIX shells emphasize state behavior at w_B = 0.25." },
    },
    {
      num: "04",
      title: "GenAI & Cloud Coverage vs. Traditional IT Only",
      left: { label: "5-Dimension Framework", text: "Designed around traditional IT OS and network service emulators — SSH servers, HTTP endpoints, and network stacks." },
      right: { label: "UHBS v4.0", text: "Explicitly tests next-generation decoys: indirect prompt injections, system prompt leaks, context exhaustion attacks, and cloud API boundary breaches across public-cloud control planes and container orchestration surfaces." },
    },
  ];

  return (
    <section id="compare" className="py-24 border-t border-border/50 bg-[#0a0e1a]">
      <motion.div
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="mb-4 flex items-center gap-3">
          <div className="h-px w-8 bg-primary"></div>
          <span className="font-mono text-primary uppercase tracking-widest text-xs">Framework Analysis</span>
        </motion.div>
        <motion.div variants={fadeUpVariant} className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4 flex items-center gap-3">
            <GitCommit className="text-primary w-8 h-8" />
            UHBS v4.0 vs. 5-Dimension Framework
          </h2>
          <p className="text-secondary-foreground max-w-3xl">
            The standard 5-Dimension Framework evaluates honeypots across Interaction, Data Quality, Resource Efficiency, Stealth, and Fingerprinting Resistance. UHBS v4.0 absorbs all five dimensions and restructures them into a production-grade standard with pre-deployment auditing, non-linear safety gates, and coverage for modern decoy architectures.
          </p>
        </motion.div>

        {/* Mapping Table */}
        <motion.div variants={fadeUpVariant} className="mb-16 overflow-x-auto">
          <div className="font-mono text-xs text-muted-foreground uppercase tracking-wider mb-4">Direct Dimension Mapping</div>
          <table className="w-full text-left text-sm font-mono border-collapse">
            <thead>
              <tr className="border-b border-border text-muted-foreground">
                <th className="py-3 pr-6 font-normal w-1/4">5-Dimension Metric</th>
                <th className="py-3 pr-6 font-normal w-1/5">UHBS v4.0 Module</th>
                <th className="py-3 font-normal">Key Expansion in UHBS v4.0</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/30">
              {mappingRows.map((row, i) => (
                <tr key={i} className="hover:bg-card/50 transition-colors group">
                  <td className="py-4 pr-6 align-top">
                    <div className="flex items-center gap-2">
                      {row.isNew && (
                        <span className="text-[10px] bg-success/20 text-success border border-success/30 px-1.5 py-0.5 rounded-sm uppercase tracking-wider">New</span>
                      )}
                      <span className={row.isNew ? "text-muted-foreground italic" : "text-foreground"}>{row.dim}</span>
                    </div>
                  </td>
                  <td className="py-4 pr-6 align-top">
                    <div>
                      <span className={`font-bold ${row.color}`}>{row.module}</span>
                      <div className="text-muted-foreground text-xs mt-0.5 leading-relaxed">{row.moduleName}</div>
                    </div>
                  </td>
                  <td className="py-4 text-secondary-foreground text-xs leading-relaxed align-top">{row.expansion}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>

        {/* Architectural Differences */}
        <motion.div variants={fadeUpVariant} className="mb-8">
          <div className="font-mono text-xs text-muted-foreground uppercase tracking-wider mb-8">Key Architectural Differences</div>
          <div className="space-y-4">
            {differences.map((diff, i) => (
              <motion.div key={i} variants={fadeUpVariant} className="border border-border/50 bg-card overflow-hidden">
                <div className="bg-[#0f1629] border-b border-border/50 px-6 py-3 flex items-center gap-4">
                  <span className="font-mono text-muted-foreground text-sm">{diff.num}</span>
                  <h4 className="font-bold text-foreground text-sm">{diff.title}</h4>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-border/50">
                  {/* Left: 5-Dimension */}
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-3">
                      <XCircle className="w-4 h-4 text-muted-foreground shrink-0" />
                      <span className="font-mono text-xs text-muted-foreground uppercase tracking-wider">{diff.left.label}</span>
                    </div>
                    <p className="text-sm text-secondary-foreground leading-relaxed">{diff.left.text}</p>
                  </div>
                  {/* Right: UHBS v4.0 */}
                  <div className="p-6 bg-[#0f1629]/50">
                    <div className="flex items-center gap-2 mb-3">
                      <CheckCircle className="w-4 h-4 text-primary shrink-0" />
                      <span className="font-mono text-xs text-primary uppercase tracking-wider">{diff.right.label}</span>
                    </div>
                    <p className="text-sm text-secondary-foreground leading-relaxed">{diff.right.text}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Summary callout */}
        <motion.div variants={fadeUpVariant} className="border border-primary/30 bg-primary/5 p-6 flex gap-4 items-start">
          <Shield className="w-6 h-6 text-primary shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-primary font-mono text-sm uppercase tracking-wide mb-2">Bottom Line for Security Leadership</h4>
            <p className="text-sm text-secondary-foreground leading-relaxed">
              The 5-Dimension Framework provides a useful conceptual lens for categorizing honeypot quality. UHBS v4.0 operationalizes every dimension into a mathematically rigorous, machine-verifiable standard — adding a pre-deployment code audit plane (Module F), a non-linear safety gate that makes containment failures non-maskable, and explicit support for GenAI and OT/ICS decoy classes that the 5-Dimension model was never designed to assess.
            </p>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
};

// Section 6: Scoring Methodology
const ScoringMethodology = () => {
  return (
    <section id="scoring" className="py-24 border-t border-border/50">
      <motion.div 
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4 flex items-center gap-3">
            <Activity className="text-primary w-8 h-8" />
            Scoring Methodology
          </h2>
          <p className="text-secondary-foreground">Computing the Universal Honeypot Quality Score (UHQS).</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <motion.div variants={fadeUpVariant} className="lg:col-span-7 bg-card border border-border p-8">
            <h3 className="font-mono text-primary text-sm uppercase tracking-wider mb-6">The UHQS 4.0 Formula</h3>
            
            <div className="bg-background border border-border/50 p-6 flex justify-center items-center overflow-x-auto mb-8 py-10">
              <div className="font-serif text-2xl md:text-3xl text-foreground whitespace-nowrap">
                UHQS = <span className="text-danger">δ<sub>C</sub></span> · (
                  <span className="text-muted-foreground">w<sub>A</sub></span>S<sub>A</sub> + 
                  <span className="text-muted-foreground">w<sub>B</sub></span>S<sub>B</sub> + 
                  <span className="text-muted-foreground">w<sub>C</sub></span>S<sub>C</sub> + 
                  <span className="text-muted-foreground">w<sub>E</sub></span>S<sub>E</sub> + 
                  <span className="text-muted-foreground">w<sub>F</sub></span>S<sub>F</sub>
                )
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 font-mono text-sm text-secondary-foreground">
              <div><span className="text-primary">δ<sub>C</sub></span> : Safety Gate Multiplier (Module D)</div>
              <div><span className="text-foreground">S<sub>x</sub></span> : Score for Module X (0-100)</div>
              <div><span className="text-muted-foreground">w<sub>x</sub></span> : Profile-Adaptive Weight</div>
            </div>
            
            <div className="mt-8 pt-8 border-t border-border/50">
              <h4 className="font-mono text-foreground mb-4">Profile-Adaptive Weights (w<sub>x</sub>)</h4>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm font-mono border-collapse">
                  <thead>
                    <tr className="border-b border-border/50 text-muted-foreground">
                      <th className="py-2 font-normal">Target Profile</th>
                      <th className="py-2 font-normal text-right">w<sub>A</sub></th>
                      <th className="py-2 font-normal text-right">w<sub>B</sub></th>
                      <th className="py-2 font-normal text-right">w<sub>C</sub></th>
                      <th className="py-2 font-normal text-right">w<sub>E</sub></th>
                      <th className="py-2 font-normal text-right">w<sub>F</sub></th>
                    </tr>
                  </thead>
                  <tbody className="text-secondary-foreground divide-y divide-border/20">
                    <tr>
                      <td className="py-2 text-foreground">POSIX Shell</td>
                      <td className="py-2 text-right">0.20</td>
                      <td className="py-2 text-right text-primary">0.25</td>
                      <td className="py-2 text-right">0.20</td>
                      <td className="py-2 text-right">0.15</td>
                      <td className="py-2 text-right">0.20</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-foreground">Low-Interaction</td>
                      <td className="py-2 text-right text-primary">0.30</td>
                      <td className="py-2 text-right">0.15</td>
                      <td className="py-2 text-right">0.25</td>
                      <td className="py-2 text-right">0.10</td>
                      <td className="py-2 text-right">0.20</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-foreground">Industrial OT</td>
                      <td className="py-2 text-right text-primary">0.35</td>
                      <td className="py-2 text-right">0.20</td>
                      <td className="py-2 text-right">0.15</td>
                      <td className="py-2 text-right">0.10</td>
                      <td className="py-2 text-right">0.20</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-foreground">Web & Cloud API</td>
                      <td className="py-2 text-right text-primary">0.25</td>
                      <td className="py-2 text-right">0.20</td>
                      <td className="py-2 text-right">0.20</td>
                      <td className="py-2 text-right">0.15</td>
                      <td className="py-2 text-right">0.20</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </motion.div>
          
          <motion.div variants={fadeUpVariant} className="lg:col-span-5 bg-card border border-border p-8 flex flex-col">
            <h3 className="font-mono text-danger text-sm uppercase tracking-wider mb-6 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" /> Safety Gate Multiplier (δ<sub>C</sub>)
            </h3>
            <p className="text-sm text-secondary-foreground mb-6">
              A Module D score below 95 triggers exponential degradation of the entire UHQS score. A honeypot that leaks data or allows lateral movement is mathematically rendered useless regardless of realism.
            </p>
            
            <div className="flex-1 overflow-x-auto">
              <table className="w-full text-left font-mono border-collapse">
                <thead>
                  <tr className="border-b border-border/50 text-muted-foreground text-sm">
                    <th className="py-3 font-normal">Module D Score</th>
                    <th className="py-3 font-normal text-right">δ<sub>C</sub> Value</th>
                    <th className="py-3 font-normal text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/20 text-sm">
                  <tr>
                    <td className="py-3 text-foreground">95 – 100</td>
                    <td className="py-3 text-right">1.00</td>
                    <td className="py-3 text-right text-success flex justify-end items-center gap-1"><CheckCircle className="w-3 h-3"/> PASS</td>
                  </tr>
                  <tr>
                    <td className="py-3 text-foreground">90 – 94</td>
                    <td className="py-3 text-right">0.81 <span className="text-muted-foreground text-xs">(-19%)</span></td>
                    <td className="py-3 text-right text-warning">WARN</td>
                  </tr>
                  <tr>
                    <td className="py-3 text-foreground">85 – 89</td>
                    <td className="py-3 text-right">0.72 <span className="text-muted-foreground text-xs">(-28%)</span></td>
                    <td className="py-3 text-right text-warning">WARN</td>
                  </tr>
                  <tr>
                    <td className="py-3 text-foreground">75 – 84</td>
                    <td className="py-3 text-right">0.56 <span className="text-muted-foreground text-xs">(-44%)</span></td>
                    <td className="py-3 text-right text-danger">FAIL</td>
                  </tr>
                  <tr>
                    <td className="py-3 text-danger">&lt; 75</td>
                    <td className="py-3 text-right text-danger">0.49 <span className="text-danger/50 text-xs">(-51%)</span></td>
                    <td className="py-3 text-right text-danger flex justify-end items-center gap-1"><XCircle className="w-3 h-3"/> CRIT</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
};

// Section 6: Audit Workflow
const AuditWorkflow = () => {
  const steps = [
    { num: 1, title: "Profile Setup", desc: "Define Target Profile Specification (TPS)" },
    { num: 2, title: "Static Audit", desc: "Execute Module F White-Box Scans" },
    { num: 3, title: "Provisioning", desc: "Deploy Sandbox & Gold Baseline" },
    { num: 4, title: "Live Execution", desc: "Adversarial Probing (Modules A-E)" },
    { num: 5, title: "Computation", desc: "Compute UHQS & Final Report" }
  ];

  return (
    <section className="py-24 border-t border-border/50 bg-[#0f1629]/50">
      <motion.div 
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.h2 variants={fadeUpVariant} className="text-3xl font-bold font-sans mb-12 text-center">Standard Audit Workflow</motion.h2>
        
        <div className="relative">
          {/* Connecting Line */}
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-px bg-border -translate-y-1/2 z-0"></div>
          
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6 relative z-10">
            {steps.map((step, i) => (
              <motion.div key={i} variants={fadeUpVariant} className="flex flex-row md:flex-col items-center md:text-center gap-4 group">
                <div className="w-12 h-12 rounded-full bg-background border-2 border-border flex items-center justify-center font-mono text-lg font-bold group-hover:border-primary transition-colors shrink-0">
                  {step.num}
                </div>
                <div>
                  <h4 className="font-bold text-foreground text-sm mb-1">{step.title}</h4>
                  <p className="text-xs font-mono text-muted-foreground">{step.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </section>
  );
};

// Section 7: Sample Scorecard
const SampleScorecard = () => {
  return (
    <section className="py-24 border-t border-border/50">
      <motion.div 
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="mb-12">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4 flex items-center gap-3">
            <Terminal className="text-primary w-8 h-8" />
            Live Benchmark Artifact
          </h2>
          <p className="text-secondary-foreground">Example scorecard for a compliant high-interaction decoy.</p>
        </motion.div>

        <motion.div variants={fadeUpVariant} className="bg-[#050810] border border-[#1e2d4d] rounded-sm overflow-hidden terminal-card shadow-2xl font-mono">
          <div className="bg-[#0f1629] border-b border-[#1e2d4d] p-4 flex items-center justify-between">
            <div className="flex items-center gap-2 text-[#94a3b8] text-xs">
              <span className="w-3 h-3 rounded-full bg-danger/80"></span>
              <span className="w-3 h-3 rounded-full bg-warning/80"></span>
              <span className="w-3 h-3 rounded-full bg-success/80"></span>
              <span className="ml-4 font-mono tracking-widest uppercase">UHBS_v4_0_Scorecard_Artifact.out</span>
            </div>
            <div className="text-[#00d4ff] text-xs">2026-07-26 14:02:44 UTC</div>
          </div>
          
          <div className="p-6 md:p-8">
            <div className="mb-8 border-b border-[#1e2d4d] pb-6">
              <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4">
                <div>
                  <div className="text-[#94a3b8] text-sm uppercase tracking-wider mb-1">Target Assessment Profile</div>
                  <h3 className="text-xl md:text-2xl text-[#e2e8f0] font-bold">High-Interaction Decoy System</h3>
                  <div className="text-[#00d4ff] mt-1 text-sm">POSIX-Shell / GenAI-Augmented</div>
                </div>
                <div className="text-right">
                  <div className="text-[#94a3b8] text-sm uppercase tracking-wider mb-1">Run ID</div>
                  <div className="text-[#e2e8f0] font-mono">UHBS-2026-9A8F-01</div>
                </div>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm mb-8">
                <thead>
                  <tr className="text-[#94a3b8] border-b border-[#1e2d4d]">
                    <th className="py-3 font-normal uppercase tracking-wider">Evaluation Module</th>
                    <th className="py-3 font-normal uppercase tracking-wider">Score</th>
                    <th className="py-3 font-normal uppercase tracking-wider">Weight</th>
                    <th className="py-3 font-normal uppercase tracking-wider text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1e2d4d]/50 text-[#e2e8f0]">
                  <tr>
                    <td className="py-3">Module A: Protocol Fidelity</td>
                    <td className="py-3">88/100</td>
                    <td className="py-3 text-[#94a3b8]">0.20</td>
                    <td className="py-3 text-right text-success">PASSED</td>
                  </tr>
                  <tr>
                    <td className="py-3">Module B: Behavioral Realism</td>
                    <td className="py-3">94/100</td>
                    <td className="py-3 text-[#94a3b8]">0.25</td>
                    <td className="py-3 text-right text-success">PASSED</td>
                  </tr>
                  <tr>
                    <td className="py-3">Module C: Telemetry Quality</td>
                    <td className="py-3">98/100</td>
                    <td className="py-3 text-[#94a3b8]">0.20</td>
                    <td className="py-3 text-right text-success">PASSED</td>
                  </tr>
                  <tr className="bg-[#141d35]/50">
                    <td className="py-3 font-bold text-danger">Module D: Safety & Containment</td>
                    <td className="py-3 font-bold">97/100</td>
                    <td className="py-3 text-danger font-bold">GATE</td>
                    <td className="py-3 text-right text-success font-bold">PASSED (0 Leaks)</td>
                  </tr>
                  <tr>
                    <td className="py-3">Module E: Scalability & Latency</td>
                    <td className="py-3">88/100</td>
                    <td className="py-3 text-[#94a3b8]">0.15</td>
                    <td className="py-3 text-right text-success">PASSED (P95: 110ms)</td>
                  </tr>
                  <tr>
                    <td className="py-3">Module F: Static Code Audit</td>
                    <td className="py-3">91/100</td>
                    <td className="py-3 text-[#94a3b8]">0.20</td>
                    <td className="py-3 text-right text-success">PASSED (0 Critical)</td>
                  </tr>
                  <tr className="border-t-2 border-[#1e2d4d]">
                    <td className="py-4 text-[#94a3b8]">Safety Gate Applied (δ<sub>C</sub>)</td>
                    <td className="py-4">1.0</td>
                    <td className="py-4 text-[#94a3b8]">(C=97≥95)</td>
                    <td className="py-4 text-right">—</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="bg-[#0f1629] border border-[#00d4ff]/30 p-6 flex flex-col md:flex-row items-center justify-between gap-6 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-[#00d4ff]/5 blur-[100px] rounded-full pointer-events-none"></div>
              
              <div>
                <div className="text-[#94a3b8] text-sm uppercase tracking-wider mb-2">Final Benchmark Evaluation</div>
                <div className="text-3xl md:text-5xl font-bold text-[#e2e8f0] flex items-baseline gap-2">
                  <span className="text-[#00d4ff]"><AnimatedNumber value={92.1} duration={2} /></span>
                  <span className="text-xl text-[#94a3b8]">/100</span>
                </div>
              </div>
              
              <div className="flex items-center gap-4 bg-[#00c471]/10 border border-[#00c471]/30 px-6 py-4">
                <Shield className="w-8 h-8 text-[#00c471]" />
                <div>
                  <div className="text-[#00c471] font-bold text-xl uppercase tracking-wider">Grade A</div>
                  <div className="text-[#94a3b8] text-xs uppercase tracking-wider">Enterprise Grade</div>
                </div>
              </div>
            </div>
            
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
};

// Footer
const Footer = () => {
  return (
    <footer className="py-12 border-t border-border bg-background">
      <div className="container mx-auto px-6 text-center">
        <div className="flex justify-center items-center gap-2 mb-6 text-primary">
          <Shield className="w-6 h-6" />
        </div>
        <div className="font-mono text-sm text-secondary-foreground mb-4">
          Universal Honeypot Benchmarking Standard <span className="text-primary/70">·</span> v4.0 <span className="text-primary/70">·</span> 2026
        </div>
        <p className="text-xs text-muted-foreground max-w-lg mx-auto mb-6">
          An objective, repeatable, quantitative methodology for deception technology evaluation — providing cybersecurity professionals with a non-biased baseline for comparing and grading honeypots and decoy systems.
        </p>
        <div className="flex justify-center gap-6 font-mono text-xs text-muted-foreground">
          <a href="specification/" className="hover:text-primary transition-colors">Specification</a>
          <a href="https://github.com/mziqudhd92/uhbs-standard" className="hover:text-primary transition-colors">GitHub</a>
          <a href="#scoring" className="hover:text-primary transition-colors">UHQS &gt; 80 Production Gate</a>
        </div>
      </div>
    </footer>
  );
};

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30 selection:text-primary">
      <div className="noise-overlay"></div>
      
      {/* Top Navbar */}
      <nav className="fixed top-0 left-0 w-full z-40 bg-background/80 backdrop-blur-md border-b border-border/50">
        <div className="container mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 font-mono font-bold text-lg">
            <Shield className="text-primary w-5 h-5" />
            <a href="/uhbs-standard/" className="hover:text-primary transition-colors">
              UHBS<span className="text-primary/70 font-light">v4</span>
            </a>
          </div>
          <div className="hidden md:flex items-center gap-6 font-mono text-xs text-secondary-foreground">
            <a href="#scope" className="hover:text-primary transition-colors">Scope</a>
            <a href="#architecture" className="hover:text-primary transition-colors">Architecture</a>
            <a href="#modules" className="hover:text-primary transition-colors">Modules</a>
            <a href="#compare" className="hover:text-primary transition-colors text-primary/80">Compare</a>
            <a href="#scoring" className="hover:text-primary transition-colors">Scoring</a>
          </div>
        </div>
      </nav>

      <main>
        <Hero />
        <ScopeAndApplicability />
        <CoreArchitecture />
        <EvaluationModules />
        <FiveDimensionComparison />
        <ScoringMethodology />
        <AuditWorkflow />
        <SampleScorecard />
      </main>

      <Footer />
    </div>
  );
}
