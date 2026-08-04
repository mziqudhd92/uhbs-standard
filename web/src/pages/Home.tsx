import { useEffect, useMemo, useState } from "react";
import { motion, type Variants } from "framer-motion";
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
  ChevronLeft,
  ChevronRight,
  LayoutGrid,
  List,
  ArrowUp,
  ArrowDown,
  ArrowUpDown,
  GitCommit,
  Layers,
  Check,
  Search,
} from "lucide-react";
import { KatexMath } from "../components/KatexMath";
import { UhqsHumanExplainerTrigger } from "../components/UhqsHumanExplainer";

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
          <span className="font-mono text-primary uppercase tracking-widest text-sm font-semibold">Beta Framework</span>
        </motion.div>
        
        <motion.h1 variants={fadeUpVariant} className="text-5xl md:text-7xl font-bold leading-tight mb-6 max-w-4xl text-foreground font-sans tracking-tight">
          Universal Honeypot Benchmarking Standard <br className="hidden md:block"/>
          <span className="text-muted-foreground font-mono text-4xl md:text-6xl tracking-tighter">(UHBS) v4.5.1 <span className="text-primary/70">· 2026</span></span>
        </motion.h1>
        
        <motion.p variants={fadeUpVariant} className="text-xl md:text-2xl text-secondary-foreground max-w-3xl mb-8 font-light leading-relaxed">
          An objective, repeatable, quantitative methodology for benchmarking honeypots, decoys, and deception technology — an open-source beta-status framework (not a consortium standard).
        </motion.p>

        <motion.div variants={fadeUpVariant} className="flex flex-wrap gap-3 mb-12">
          <a href="mkdocs/" className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-5 py-2.5 font-mono text-sm font-semibold hover:opacity-90 transition-opacity">
            Open docs <ArrowRight className="w-4 h-4" />
          </a>
          <a href="#results" className="inline-flex items-center gap-2 bg-card border border-border px-5 py-2.5 font-mono text-sm hover:border-primary/50 transition-colors">
            Results
          </a>
          <a href="#mcp" className="inline-flex items-center gap-2 bg-card border border-border px-5 py-2.5 font-mono text-sm hover:border-primary/50 transition-colors">
            MCP
          </a>
          <a href="https://github.com/uhbs/uhbs-standard" className="inline-flex items-center gap-2 bg-card border border-border px-5 py-2.5 font-mono text-sm hover:border-primary/50 transition-colors">
            GitHub
          </a>
        </motion.div>
        
        <motion.div variants={fadeUpVariant} className="flex flex-wrap gap-4 mt-2 mb-12">
          {[
            { label: "Protocol-Agnostic", icon: Globe },
            { label: "Quantitative Scoring 0–100", icon: Activity },
            { label: "Six Evaluation Modules", icon: Layers },
            { label: "Beta Production Baseline", icon: Shield }
          ].map((badge, i) => (
            <div key={i} className="flex items-center gap-2 bg-card border border-border px-4 py-2.5 rounded-sm terminal-card">
              <badge.icon className="w-4 h-4 text-primary" />
              <span className="font-mono text-sm text-foreground">{badge.label}</span>
            </div>
          ))}
        </motion.div>

        <motion.div variants={fadeUpVariant} className="max-w-4xl">
          <div className="flex items-center justify-between gap-4 mb-3">
            <p className="font-mono text-xs uppercase tracking-widest text-primary">
              Demo · install + full UHQS
            </p>
            <a
              href="https://github.com/uhbs/uhbs-standard/blob/main/docs/assets/uhbs-lab-demo.cast"
              className="font-mono text-xs text-secondary-foreground hover:text-primary transition-colors"
            >
              asciinema cast →
            </a>
          </div>
          <div className="border border-border bg-card/40 overflow-hidden terminal-card">
            <img
              src={`${import.meta.env.BASE_URL}assets/uhbs-lab-demo.gif`}
              alt="UHBS lab demo: install Cowrie and Conpot, start decoys, full UHQS grades for Cowrie, Conpot, and HellPot"
              className="w-full h-auto block"
              loading="lazy"
            />
          </div>
          <p className="mt-3 font-mono text-xs text-secondary-foreground leading-relaxed max-w-3xl">
            Pip-install Cowrie &amp; Conpot, bring up live surfaces, then run full
            UHQS (modules A–F) — Cowrie SSH · Conpot Modbus · HellPot HTTP.
          </p>
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
                The UHBS v4.5.1 framework provides a rigorous technical foundation for evaluating the efficacy, safety, and realism of deception assets prior to deployment.
              </p>
              <p className="mt-4">
                Historically, deception technology has been evaluated subjectively. UHBS introduces a verifiable, deterministic mathematical model designed to expose flaws in protocol state machines, containment boundaries, and behavioral realism.
              </p>
            </div>
            
            <div className="mt-8 bg-primary/5 border-l-4 border-primary/50 p-6">
              <div className="flex items-start gap-4">
                <Shield className="w-6 h-6 text-primary shrink-0 mt-1" />
                <div>
                  <h4 className="text-primary font-semibold font-mono mb-2 uppercase tracking-wide text-sm">Vendor-Neutral Beta Baseline</h4>
                  <p className="text-secondary-foreground text-sm">
                    UHBS v4.5.1 is an open-source beta-status framework for comparing and grading honeypots by class and protocol — mathematically reproducible, not a consortium or adopted industry standard.
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6 border border-warning/40 bg-warning/5 p-5 flex gap-4 items-start">
              <AlertTriangle className="w-6 h-6 text-warning shrink-0 mt-0.5" />
              <div>
                <h4 className="font-mono text-warning text-xs uppercase tracking-wider mb-2">Beta Production Baseline</h4>
                <p className="text-sm text-secondary-foreground leading-relaxed">
                  Organizations <span className="text-foreground font-semibold">MAY</span> use UHBS as an internal gate. It is <span className="text-foreground font-semibold">RECOMMENDED</span> that active decoys meet <span className="text-foreground font-semibold">UHQS &gt; 80</span> with a passing Safety Gate before production deployment. See the docs for status and limitations.
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
      expansion: "Module F (white-box): Scans repository code, container build manifests, and system prompts for SAST flaws, default keys, and unhandled command stubs.",
      isNew: true,
    },
  ];

  const differences = [
    {
      num: "01",
      title: "Dual-Plane Audit vs. Runtime-Only",
      left: { label: "5-Dimension Framework", text: "Functions purely as an operational runtime framework, observing honeypot behavior during active exposure." },
      right: { label: "UHBS v4.5.1", text: "Employs a Dual-Plane Audit Philosophy — requires pre-deployment static code analysis (Module F) to catch hardcoded SSH keys, static seeds, or vulnerable command wrappers before dynamic sandbox probing begins." },
    },
    {
      num: "02",
      title: "Non-Linear Safety Gate vs. Linear Averaging",
      left: { label: "5-Dimension Framework", text: "Aggregates metrics using simple linear weighted averages. A high interaction score can mask a serious containment flaw, allowing dangerous decoys to pass evaluation." },
      right: { label: "UHBS v4.5.1", text: "Implements a strict Safety Gate Multiplier (δ_C). If Module D containment drops below 95/100, an exponential penalty degrades the entire UHQS score regardless of performance elsewhere." },
    },
    {
      num: "03",
      title: "Profile-Adaptive Context (TPS) vs. Static Metrics",
      left: { label: "5-Dimension Framework", text: "Applies identical static metric weights across all honeypot classes — a SCADA PLC and an SSH shell are evaluated with the same emphasis." },
      right: { label: "UHBS v4.5.1", text: "Target Profile Specification (profile.yaml) adjusts evaluation weights. ICS-SCADA weights protocol fidelity at w_A = 0.35, while POSIX shells emphasize state behavior at w_B = 0.25." },
    },
    {
      num: "04",
      title: "GenAI & Cloud Coverage vs. Traditional IT Only",
      left: { label: "5-Dimension Framework", text: "Designed around traditional IT OS and network service emulators — SSH servers, HTTP endpoints, and network stacks." },
      right: { label: "UHBS v4.5.1", text: "Explicitly tests next-generation decoys: indirect prompt injections, system prompt leaks, context exhaustion attacks, and cloud API boundary breaches across public-cloud control planes and container orchestration surfaces." },
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
            UHBS v4.5.1 vs. 5-Dimension Framework
          </h2>
          <p className="text-secondary-foreground max-w-3xl">
            Proposed five-dimension honeypot metrics (interaction, data quality, resource efficiency, stealth, fingerprinting resistance) are a useful conceptual lens—not an adopted industry standard. UHBS v4.5.1 operationalizes overlapping axes with dual-plane auditing, a non-linear Safety Gate, and coverage for modern decoy classes. For the full evidence-graded comparison against fourteen framework/model families, see the{" "}
            <a href="mkdocs/mappings/related-frameworks/" className="text-primary hover:underline">
              related frameworks
            </a>{" "}
            mapping.
          </p>
        </motion.div>

        {/* Mapping Table */}
        <motion.div variants={fadeUpVariant} className="mb-16 overflow-x-auto">
          <div className="font-mono text-xs text-muted-foreground uppercase tracking-wider mb-4">Direct Dimension Mapping</div>
          <table className="w-full text-left text-sm font-mono border-collapse">
            <thead>
              <tr className="border-b border-border text-muted-foreground">
                <th className="py-3 pr-6 font-normal w-1/4">5-Dimension Metric</th>
                <th className="py-3 pr-6 font-normal w-1/5">UHBS v4.5.1 Module</th>
                <th className="py-3 font-normal">Key Expansion in UHBS v4.5.1</th>
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
                  {/* Right: UHBS v4.5.1 */}
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
              Five-dimension proposals provide a useful conceptual lens for categorizing honeypot quality. UHBS v4.5.1 turns overlapping concerns into a machine-verifiable evaluation — adding a pre-deployment code audit plane (Module F), a non-linear safety gate that makes containment failures non-maskable, and explicit support for GenAI and OT/ICS decoy classes. See the{" "}
              <a href="mkdocs/mappings/related-frameworks/" className="text-primary hover:underline">
                evidence-based framework comparison
              </a>{" "}
              for CDMM, game-theoretic models, Honeyval, ICS research, and more.
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
          <motion.div variants={fadeUpVariant} className="lg:col-span-7 bg-card border border-border p-4 md:p-6">
            <div className="flex flex-wrap items-center justify-between gap-3 mb-4 px-2">
              <h3 className="font-mono text-primary text-sm uppercase tracking-wider">The UHQS 4.5.1 Formula</h3>
              <UhqsHumanExplainerTrigger />
            </div>
            <div className="uhqs-katex uhqs-katex-display space-y-4">
              <KatexMath
                display
                className="block"
                label="UHQS equals delta-C times the weighted sum of modules A, B, C, E, and F"
                tex={`\\mathrm{UHQS} = \\delta_{C}\\cdot\\bigl(w_{A}S_{A}+w_{B}S_{B}+w_{C}S_{C}+w_{E}S_{E}+w_{F}S_{F}\\bigr)`}
              />
              <KatexMath
                display
                className="block uhqs-katex-danger"
                label="Safety Gate: delta-C is 1 when Module D is at least 95, otherwise C over 100 squared"
                tex={`\\delta_{C} = \\begin{cases} 1 & \\text{if } C \\ge 95 \\\\ \\bigl(C/100\\bigr)^{2} & \\text{if } C < 95 \\end{cases}`}
              />
            </div>
            <p className="mt-4 px-2 text-xs text-muted-foreground font-mono leading-relaxed">
              Module D is missing from the parentheses on purpose: containment becomes{" "}
              <KatexMath className="uhqs-katex uhqs-katex-accent inline" tex={`\\delta_{C}`} />{" "}
              and multiplies the whole score. Typeset with{" "}
              <a href="https://katex.org/" className="text-primary hover:underline" target="_blank" rel="noopener noreferrer">KaTeX</a>
              . Full normative detail:{" "}
              <a href="mkdocs/specification/scoring-formula/" className="text-primary hover:underline">scoring formula</a>.
            </p>

            <div className="grid grid-cols-2 gap-4 font-mono text-sm text-secondary-foreground mt-6 px-2">
              <div>
                <KatexMath className="uhqs-katex uhqs-katex-accent inline" tex={`\\delta_{C}`} /> : Safety Gate Multiplier (Module D)
              </div>
              <div>
                <KatexMath className="uhqs-katex inline" tex={`S_{x}`} /> : Score for Module X (0–100)
              </div>
              <div>
                <KatexMath className="uhqs-katex inline" tex={`w_{x}`} /> : Profile-Adaptive Weight
              </div>
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
                      <td className="py-2 text-foreground">ICS-SCADA</td>
                      <td className="py-2 text-right text-primary">0.35</td>
                      <td className="py-2 text-right">0.20</td>
                      <td className="py-2 text-right">0.15</td>
                      <td className="py-2 text-right">0.10</td>
                      <td className="py-2 text-right">0.20</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-foreground">Web-API</td>
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

// Optional Advanced Evidence Profile (does not change UHQS) — lab evaluation only
const AdvancedEvidenceProfile = () => {
  const values = [
    "Compare lab decoy behavior with a matched lab reference.",
    "Measure engagement and distinguishability with uncertainty.",
    "Analyze local evidence offline—never launch attacks.",
  ];

  const credits = [
    {
      cite: "Zhu (2019)",
      title: "Game Theory for Cyber Deception: A Tutorial",
      href: "https://doi.org/10.1145/3314058.3314067",
      note: "Signaling / dynamic-game vocabulary",
    },
    {
      cite: "Collins, Xu & Brown (2024)",
      title: "Game-Theoretic Cybersecurity…",
      href: "https://arxiv.org/abs/2401.13815",
      note: "Uncertainty & practicality discipline (preprint)",
    },
    {
      cite: "Ersok et al. (2022)",
      title: "Measuring Honeypots based on CTF game",
      href: "https://doi.org/10.1109/ICCC202255925.2022.9922853",
      note: "Controlled CTF / log validation patterns",
    },
    {
      cite: "Li et al. (2020)",
      title: "Anti-Honeypot Enabled Optimal Attack Strategy…",
      href: "https://doi.org/10.1109/OJCS.2020.3030825",
      note: "Attacker threat-model tiers (not a defender grade)",
    },
  ];

  return (
    <section id="advanced-evidence" className="py-24 border-t border-border/50 bg-[#0a0e1a]">
      <motion.div
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="mb-4 flex items-center gap-3">
          <div className="h-px w-8 bg-primary"></div>
          <span className="font-mono text-primary uppercase tracking-widest text-xs">Optional Lab Evidence Layer</span>
        </motion.div>
        <motion.div variants={fadeUpVariant} className="mb-8">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4 flex items-center gap-3">
            <Layers className="text-primary w-8 h-8" />
            Advanced Evidence Profile (optional)
          </h2>
          <p className="text-secondary-foreground max-w-3xl mb-4">
            UHQS remains the normative implementation-quality and safety grade from{" "}
            <span className="text-foreground font-medium">laboratory evaluation</span>. The optional Advanced Evidence
            Profile adds controlled lab evidence about adversarial perception, engagement, distinguishability, and cost
            under declared experimental conditions.{" "}
            <span className="text-foreground font-medium">AEP does not change UHQS.</span>
          </p>
          <p className="text-sm text-warning/90 max-w-3xl border border-warning/30 bg-warning/5 px-4 py-3 font-mono leading-relaxed">
            Lab / sandbox only — not real-world production testing. UHBS and AEP must not be aimed at production systems,
            customer environments, or unauthorized targets. A UHQS &gt; 80 “production baseline” is an internal gate{" "}
            <em>after</em> lab grading, not permission to test in the wild.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-10">
          <motion.div variants={fadeUpVariant} className="lg:col-span-5 border border-border bg-card p-6">
            <h3 className="font-mono text-xs text-muted-foreground uppercase tracking-wider mb-3">Core UHBS (lab)</h3>
            <p className="text-sm text-secondary-foreground leading-relaxed mb-4">
              Modules A–F, profile-adaptive weights, Safety Gate δ<sub>C</sub>, and a reproducible UHQS scorecard from
              isolated lab runs.
            </p>
            <ul className="text-sm font-mono text-foreground space-y-2">
              <li>UHQS 0–100 + letter grade</li>
              <li>Normative for UHBS-Core / UHBS-Lab</li>
              <li>Lab release / conformance gate</li>
            </ul>
          </motion.div>
          <motion.div variants={fadeUpVariant} className="lg:col-span-2 flex items-center justify-center">
            <ArrowRight className="w-8 h-8 text-primary rotate-90 lg:rotate-0" aria-hidden="true" />
          </motion.div>
          <motion.div variants={fadeUpVariant} className="lg:col-span-5 border border-primary/30 bg-primary/5 p-6">
            <h3 className="font-mono text-xs text-primary uppercase tracking-wider mb-3">Optional AEP (lab)</h3>
            <p className="text-sm text-secondary-foreground leading-relaxed mb-4">
              Controlled lab decoy vs matched lab reference (+ evaluator control). Status:{" "}
              <span className="font-mono text-foreground">valid | inconclusive | control_failed</span> — not grades.
            </p>
            <ul className="text-sm font-mono text-foreground space-y-2">
              <li>VoD · FSV · DTDR · EER</li>
              <li>Uncertainty + sample / censoring counts</li>
              <li>Separate ADVANCED-EVIDENCE addendum</li>
            </ul>
          </motion.div>
        </div>

        <motion.div variants={fadeUpVariant} className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
          {values.map((text) => (
            <div key={text} className="border border-border/50 bg-card/50 p-5 flex gap-3 items-start">
              <CheckCircle className="w-4 h-4 text-primary shrink-0 mt-0.5" aria-hidden="true" />
              <p className="text-sm text-secondary-foreground leading-relaxed">{text}</p>
            </div>
          ))}
        </motion.div>

        <motion.div variants={fadeUpVariant} className="mb-10 border border-border/50 bg-card/40 p-6">
          <h3 className="font-mono text-xs text-muted-foreground uppercase tracking-wider mb-3">
            Academic foundations (credited)
          </h3>
          <p className="text-sm text-secondary-foreground mb-4 max-w-3xl leading-relaxed">
            AEP’s experimental vocabulary and measurement discipline draw on published research. We credit these authors
            and venues; citation does <span className="text-foreground">not</span> mean they endorse UHBS or that UHBS
            implements their full models.
          </p>
          <ul className="space-y-3">
            {credits.map((c) => (
              <li key={c.href} className="text-sm leading-relaxed">
                <a
                  href={c.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline font-medium focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
                >
                  {c.cite}
                </a>
                <span className="text-secondary-foreground">
                  {" "}
                  — {c.title} · {c.note}
                </span>
              </li>
            ))}
          </ul>
          <p className="mt-4 text-xs font-mono text-muted-foreground">
            Full ledger:{" "}
            <a href="mkdocs/advanced-evidence/research-foundations/" className="text-primary hover:underline">
              Research foundations &amp; credits
            </a>
          </p>
        </motion.div>

        <motion.div
          variants={fadeUpVariant}
          id="aep-slm-alpha"
          className="mb-10 border border-border/60 bg-card/50 p-6"
        >
          <div className="flex flex-wrap items-center gap-3 mb-3">
            <span className="font-mono text-[10px] uppercase tracking-widest px-2 py-1 border border-warning/40 text-warning/90">
              Alpha · off by default
            </span>
            <h3 className="font-mono text-xs text-muted-foreground uppercase tracking-wider">
              Optional AEP SLM evaluator
            </h3>
          </div>
          <p className="text-sm text-secondary-foreground max-w-3xl leading-relaxed mb-4">
            An opt-in helper for labs that want a small / local language model (or a deterministic{" "}
            <span className="font-mono text-foreground">mock</span>) to draft{" "}
            <span className="text-foreground font-medium">AEP trial JSONL</span> for offline{" "}
            <span className="font-mono text-foreground">uhbs aep analyze</span>. Installing UHBS does{" "}
            <span className="text-foreground font-medium">not</span> turn it on — you must edit a local{" "}
            <span className="font-mono text-foreground">aep-slm.yaml</span> (enable flag, unlock phrase, and
            attestations). It never changes UHQS, never launches probes, and is not exposed over the AI-host MCP
            server.
          </p>
          <ul className="text-sm font-mono text-foreground space-y-2 mb-5">
            <li>
              <span className="text-primary">pip install &apos;uhbs[aep-slm]&apos;</span> →{" "}
              <span className="text-secondary-foreground">uhbs aep slm init|validate|status|generate</span>
            </li>
            <li>
              Providers: <span className="text-secondary-foreground">mock</span> (offline) ·{" "}
              <span className="text-secondary-foreground">recorded</span> · loopback-only{" "}
              <span className="text-secondary-foreground">openai_compatible</span>
            </li>
            <li className="text-secondary-foreground">
              Purpose: experiment dry-runs / local replay — not certification, not production testing
            </li>
          </ul>
          <div className="flex flex-wrap gap-3">
            <a
              href="mkdocs/advanced-evidence/slm-alpha/"
              className="inline-flex items-center gap-2 px-4 py-2 border border-primary/40 bg-primary/10 text-primary font-mono text-xs hover:bg-primary/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
            >
              How to use SLM (alpha) <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
            </a>
            <a
              href="mkdocs/advanced-evidence/cli/#aep-slm"
              className="inline-flex items-center gap-2 px-4 py-2 border border-border text-secondary-foreground font-mono text-xs hover:border-primary/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
            >
              CLI reference
            </a>
          </div>
        </motion.div>

        <motion.div variants={fadeUpVariant} className="flex flex-wrap gap-4">
          <a
            href="mkdocs/advanced-evidence/"
            className="inline-flex items-center gap-2 px-5 py-3 border border-primary/40 bg-primary/10 text-primary font-mono text-sm hover:bg-primary/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            AEP overview <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </a>
          <a
            href="mkdocs/advanced-evidence/slm-alpha/"
            className="inline-flex items-center gap-2 px-5 py-3 border border-border text-secondary-foreground font-mono text-sm hover:border-primary/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            SLM evaluator (alpha)
          </a>
          <a
            href="mkdocs/advanced-evidence/research-foundations/"
            className="inline-flex items-center gap-2 px-5 py-3 border border-border text-secondary-foreground font-mono text-sm hover:border-primary/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            Research credits
          </a>
          <a
            href="mkdocs/advanced-evidence/runbook/"
            className="inline-flex items-center gap-2 px-5 py-3 border border-border text-secondary-foreground font-mono text-sm hover:border-primary/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            Runbook
          </a>
        </motion.div>
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

// Section 7: Results — published tutorials, runs, scorecards
type LabResult = {
  name: string;
  classLabel: string;
  protocol: string;
  protocolLabel: string;
  repo: string;
  /** GitHub `pushed_at` date (YYYY-MM-DD) for the upstream repo */
  repoUpdated: string;
  uhqsQuick: number | null;
  uhqsFull: number | null;
  gradeQuick: string;
  gradeFull: string;
  hub: string;
  tutorial: string;
  methodology: string;
  scorecard: string;
  quick: string;
  full: string;
  quickCard: string;
  fullCard: string;
};

const PROTOCOL_FILTERS = [
  { id: "all", label: "All" },
  { id: "http", label: "HTTP" },
  { id: "ssh", label: "SSH" },
  { id: "ssh_tarpit", label: "SSH tarpit" },
  { id: "telnet", label: "Telnet" },
  { id: "ftp", label: "FTP" },
  { id: "redis", label: "Redis" },
  { id: "smb", label: "SMB" },
  { id: "sip", label: "SIP" },
  { id: "pjl", label: "PJL" },
  { id: "modbus", label: "Modbus" },
  { id: "mcp", label: "MCP" },
  { id: "smtp", label: "SMTP" },
  { id: "pop3", label: "POP3" },
  { id: "mysql", label: "MySQL" },
  { id: "postgres", label: "PostgreSQL" },
  { id: "rdp", label: "RDP" },
  { id: "generic", label: "Generic TCP" },
  { id: "vnc", label: "VNC" },
] as const;

const LAB_RESULTS: LabResult[] = [
  {
    name: "ESPot",
    classLabel: "Web-API · HTTP :9200",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/mycert/ESPot",
    repoUpdated: "2014-08-25",
    uhqsQuick: 49.34,
    uhqsFull: 63.33,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/espot/",
    tutorial: "mkdocs/conformance/reports/espot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/espot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/espot-web-api/",
    quick: "mkdocs/conformance/reports/espot/quick/",
    full: "mkdocs/conformance/reports/espot/full/",
    quickCard: "mkdocs/conformance/reports/espot/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/espot/full/SCORECARD.txt",
  },
  {
    name: "miniprint",
    classLabel: "Low-Interaction · PJL :9100",
    protocol: "pjl",
    protocolLabel: "PJL",
    repo: "https://github.com/sa7mon/miniprint",
    repoUpdated: "2023-07-09",
    uhqsQuick: 41.83,
    uhqsFull: 50.43,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/miniprint/",
    tutorial: "mkdocs/conformance/reports/miniprint/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/miniprint/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/miniprint-low-interaction/",
    quick: "mkdocs/conformance/reports/miniprint/quick/",
    full: "mkdocs/conformance/reports/miniprint/full/",
    quickCard: "mkdocs/conformance/reports/miniprint/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/miniprint/full/SCORECARD.txt",
  },
  {
    name: "Conpot",
    classLabel: "ICS-SCADA · Modbus :5020",
    protocol: "modbus",
    protocolLabel: "Modbus",
    repo: "https://github.com/mushorg/conpot",
    repoUpdated: "2026-07-25",
    uhqsQuick: 44.55,
    uhqsFull: 55.4,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/conpot/",
    tutorial: "mkdocs/conformance/reports/conpot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/conpot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/conpot-ics-scada/",
    quick: "mkdocs/conformance/reports/conpot/quick/",
    full: "mkdocs/conformance/reports/conpot/full/",
    quickCard: "mkdocs/conformance/reports/conpot/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/conpot/full/SCORECARD.txt",
  },
  {
    name: "Cowrie (SSH)",
    classLabel: "Low-Interaction · SSH :2222",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/cowrie/cowrie",
    repoUpdated: "2026-07-29",
    uhqsQuick: 82.76,
    uhqsFull: 61.37,
    gradeQuick: "B",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/cowrie/ssh/",
    tutorial: "mkdocs/conformance/reports/cowrie/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/cowrie/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/cowrie-ssh/",
    quick: "mkdocs/conformance/reports/cowrie/ssh/quick/",
    full: "mkdocs/conformance/reports/cowrie/ssh/full/",
    quickCard: "mkdocs/conformance/reports/cowrie/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/cowrie/ssh/full/SCORECARD.txt",
  },
  {
    name: "Cowrie (Telnet)",
    classLabel: "Low-Interaction · Telnet :2223",
    protocol: "telnet",
    protocolLabel: "Telnet",
    repo: "https://github.com/cowrie/cowrie",
    repoUpdated: "2026-07-29",
    uhqsQuick: 53.41,
    uhqsFull: 64.9,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/cowrie/telnet/",
    tutorial: "mkdocs/conformance/reports/cowrie/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/cowrie/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/cowrie-telnet/",
    quick: "mkdocs/conformance/reports/cowrie/telnet/quick/",
    full: "mkdocs/conformance/reports/cowrie/telnet/full/",
    quickCard: "mkdocs/conformance/reports/cowrie/telnet/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/cowrie/telnet/full/SCORECARD.txt",
  },
  {
    name: "LLM Honeypot (SSH)",
    classLabel: "Low-Interaction · SSH :2222",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/PalisadeResearch/llm-honeypot",
    repoUpdated: "2026-07-27",
    uhqsQuick: 67.94,
    uhqsFull: 61.17,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/llm-honeypot/ssh/",
    tutorial: "mkdocs/conformance/reports/llm-honeypot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/llm-honeypot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/llm-honeypot-ssh/",
    quick: "mkdocs/conformance/reports/llm-honeypot/ssh/quick/",
    full: "mkdocs/conformance/reports/llm-honeypot/ssh/full/",
    quickCard: "mkdocs/conformance/reports/llm-honeypot/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/llm-honeypot/ssh/full/SCORECARD.txt",
  },
  {
    name: "HoneyAgents (SSH)",
    classLabel: "Low-Interaction · SSH :2222",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/mrwadams/honeyagents",
    repoUpdated: "2024-01-05",
    uhqsQuick: 67.94,
    uhqsFull: 65.24,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/honeyagents/ssh/",
    tutorial: "mkdocs/conformance/reports/honeyagents/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/honeyagents/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/honeyagents-ssh/",
    quick: "mkdocs/conformance/reports/honeyagents/ssh/quick/",
    full: "mkdocs/conformance/reports/honeyagents/ssh/full/",
    quickCard: "mkdocs/conformance/reports/honeyagents/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/honeyagents/ssh/full/SCORECARD.txt",
  },
  {
    name: "GenAIPot (SMTP)",
    classLabel: "Low-Interaction · SMTP :25",
    protocol: "smtp",
    protocolLabel: "SMTP",
    repo: "https://github.com/ls1911/GenAIPot",
    repoUpdated: "2024-10-09",
    uhqsQuick: 30.9,
    uhqsFull: 30.78,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/genaipot/smtp/",
    tutorial: "mkdocs/conformance/reports/genaipot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/genaipot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/genaipot-smtp/",
    quick: "mkdocs/conformance/reports/genaipot/smtp/quick/",
    full: "mkdocs/conformance/reports/genaipot/smtp/full/",
    quickCard: "mkdocs/conformance/reports/genaipot/smtp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/genaipot/smtp/full/SCORECARD.txt",
  },
  {
    name: "GenAIPot (POP3)",
    classLabel: "Low-Interaction · POP3 :110",
    protocol: "pop3",
    protocolLabel: "POP3",
    repo: "https://github.com/ls1911/GenAIPot",
    repoUpdated: "2024-10-09",
    uhqsQuick: 44.24,
    uhqsFull: 44.13,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/genaipot/pop3/",
    tutorial: "mkdocs/conformance/reports/genaipot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/genaipot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/genaipot-pop3/",
    quick: "mkdocs/conformance/reports/genaipot/pop3/quick/",
    full: "mkdocs/conformance/reports/genaipot/pop3/full/",
    quickCard: "mkdocs/conformance/reports/genaipot/pop3/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/genaipot/pop3/full/SCORECARD.txt",
  },
  {
    name: "LLMPot (Modbus)",
    classLabel: "ICS-SCADA · Modbus :5020",
    protocol: "modbus",
    protocolLabel: "Modbus",
    repo: "https://github.com/momalab/LLMPot",
    repoUpdated: "2026-04-27",
    uhqsQuick: 38.48,
    uhqsFull: 55.24,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/llmpot/modbus/",
    tutorial: "mkdocs/conformance/reports/llmpot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/llmpot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/llmpot-modbus/",
    quick: "mkdocs/conformance/reports/llmpot/modbus/quick/",
    full: "mkdocs/conformance/reports/llmpot/modbus/full/",
    quickCard: "mkdocs/conformance/reports/llmpot/modbus/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/llmpot/modbus/full/SCORECARD.txt",
  },
  {
    name: "LLMPot (S7comm)",
    classLabel: "ICS-SCADA · S7comm :102",
    protocol: "s7comm",
    protocolLabel: "S7comm",
    repo: "https://github.com/momalab/LLMPot",
    repoUpdated: "2026-04-27",
    uhqsQuick: 45.53,
    uhqsFull: 65.41,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/llmpot/s7comm/",
    tutorial: "mkdocs/conformance/reports/llmpot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/llmpot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/llmpot-s7comm/",
    quick: "mkdocs/conformance/reports/llmpot/s7comm/quick/",
    full: "mkdocs/conformance/reports/llmpot/s7comm/full/",
    quickCard: "mkdocs/conformance/reports/llmpot/s7comm/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/llmpot/s7comm/full/SCORECARD.txt",
  },
  {
    name: "LLMPot (HTTP)",
    classLabel: "Web-API · HTTP :8080",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/momalab/LLMPot",
    repoUpdated: "2026-04-27",
    uhqsQuick: 45.84,
    uhqsFull: 63.11,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/llmpot/http/",
    tutorial: "mkdocs/conformance/reports/llmpot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/llmpot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/llmpot-http/",
    quick: "mkdocs/conformance/reports/llmpot/http/quick/",
    full: "mkdocs/conformance/reports/llmpot/http/full/",
    quickCard: "mkdocs/conformance/reports/llmpot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/llmpot/http/full/SCORECARD.txt",
  },
  {
    name: "DataTrap (SSH)",
    classLabel: "Low-Interaction · SSH :2222",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/ThalesGroup/dd-honeypot",
    repoUpdated: "2026-05-20",
    uhqsQuick: 59.88,
    uhqsFull: 55.61,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/datatrap/ssh/",
    tutorial: "mkdocs/conformance/reports/datatrap/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/datatrap/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/datatrap-ssh/",
    quick: "mkdocs/conformance/reports/datatrap/ssh/quick/",
    full: "mkdocs/conformance/reports/datatrap/ssh/full/",
    quickCard: "mkdocs/conformance/reports/datatrap/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/datatrap/ssh/full/SCORECARD.txt",
  },
  {
    name: "DataTrap (HTTP)",
    classLabel: "Web-API · HTTP :8080",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/ThalesGroup/dd-honeypot",
    repoUpdated: "2026-05-20",
    uhqsQuick: 45.84,
    uhqsFull: 65.85,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/datatrap/http/",
    tutorial: "mkdocs/conformance/reports/datatrap/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/datatrap/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/datatrap-http/",
    quick: "mkdocs/conformance/reports/datatrap/http/quick/",
    full: "mkdocs/conformance/reports/datatrap/http/full/",
    quickCard: "mkdocs/conformance/reports/datatrap/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/datatrap/http/full/SCORECARD.txt",
  },
  {
    name: "DataTrap (MySQL)",
    classLabel: "Low-Interaction · MySQL :3306",
    protocol: "mysql",
    protocolLabel: "MySQL",
    repo: "https://github.com/ThalesGroup/dd-honeypot",
    repoUpdated: "2026-05-20",
    uhqsQuick: 40.35,
    uhqsFull: 50.65,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/datatrap/mysql/",
    tutorial: "mkdocs/conformance/reports/datatrap/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/datatrap/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/datatrap-mysql/",
    quick: "mkdocs/conformance/reports/datatrap/mysql/quick/",
    full: "mkdocs/conformance/reports/datatrap/mysql/full/",
    quickCard: "mkdocs/conformance/reports/datatrap/mysql/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/datatrap/mysql/full/SCORECARD.txt",
  },
  {
    name: "DataTrap (PostgreSQL)",
    classLabel: "Low-Interaction · PostgreSQL :5432",
    protocol: "postgres",
    protocolLabel: "PostgreSQL",
    repo: "https://github.com/ThalesGroup/dd-honeypot",
    repoUpdated: "2026-05-20",
    uhqsQuick: 40.35,
    uhqsFull: 57.94,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/datatrap/postgres/",
    tutorial: "mkdocs/conformance/reports/datatrap/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/datatrap/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/datatrap-postgres/",
    quick: "mkdocs/conformance/reports/datatrap/postgres/quick/",
    full: "mkdocs/conformance/reports/datatrap/postgres/full/",
    quickCard: "mkdocs/conformance/reports/datatrap/postgres/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/datatrap/postgres/full/SCORECARD.txt",
  },
  {
    name: "DataTrap (Redis)",
    classLabel: "Low-Interaction · Redis :6379",
    protocol: "redis",
    protocolLabel: "Redis",
    repo: "https://github.com/ThalesGroup/dd-honeypot",
    repoUpdated: "2026-05-20",
    uhqsQuick: 42.37,
    uhqsFull: 60.85,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/datatrap/redis/",
    tutorial: "mkdocs/conformance/reports/datatrap/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/datatrap/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/datatrap-redis/",
    quick: "mkdocs/conformance/reports/datatrap/redis/quick/",
    full: "mkdocs/conformance/reports/datatrap/redis/full/",
    quickCard: "mkdocs/conformance/reports/datatrap/redis/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/datatrap/redis/full/SCORECARD.txt",
  },
  {
    name: "DataTrap (Telnet)",
    classLabel: "Low-Interaction · Telnet :2323",
    protocol: "telnet",
    protocolLabel: "Telnet",
    repo: "https://github.com/ThalesGroup/dd-honeypot",
    repoUpdated: "2026-05-20",
    uhqsQuick: 43.38,
    uhqsFull: 59.88,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/datatrap/telnet/",
    tutorial: "mkdocs/conformance/reports/datatrap/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/datatrap/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/datatrap-telnet/",
    quick: "mkdocs/conformance/reports/datatrap/telnet/quick/",
    full: "mkdocs/conformance/reports/datatrap/telnet/full/",
    quickCard: "mkdocs/conformance/reports/datatrap/telnet/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/datatrap/telnet/full/SCORECARD.txt",
  },
  {
    name: "Endlessh",
    classLabel: "Low-Interaction · ssh_tarpit :2222",
    protocol: "ssh_tarpit",
    protocolLabel: "SSH tarpit",
    repo: "https://github.com/skeeto/endlessh",
    repoUpdated: "2024-06-03",
    uhqsQuick: 46.55,
    uhqsFull: 54.07,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/endlessh/",
    tutorial: "mkdocs/conformance/reports/endlessh/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/endlessh/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/endlessh-ssh-tarpit/",
    quick: "mkdocs/conformance/reports/endlessh/quick/",
    full: "mkdocs/conformance/reports/endlessh/full/",
    quickCard: "mkdocs/conformance/reports/endlessh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/endlessh/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (HTTP)",
    classLabel: "Web-API · HTTP :80",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 52.34,
    uhqsFull: 66.02,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/http/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-web-api/",
    quick: "mkdocs/conformance/reports/opencanary/http/quick/",
    full: "mkdocs/conformance/reports/opencanary/http/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/http/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (FTP)",
    classLabel: "Low-Interaction · FTP :21",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 50.47,
    uhqsFull: 61.5,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/ftp/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-ftp/",
    quick: "mkdocs/conformance/reports/opencanary/ftp/quick/",
    full: "mkdocs/conformance/reports/opencanary/ftp/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/ftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/ftp/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (SSH)",
    classLabel: "Low-Interaction · SSH :2222",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 31.94,
    uhqsFull: 35.64,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/opencanary/ssh/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-ssh/",
    quick: "mkdocs/conformance/reports/opencanary/ssh/quick/",
    full: "mkdocs/conformance/reports/opencanary/ssh/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/ssh/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (Telnet)",
    classLabel: "Low-Interaction · Telnet :23",
    protocol: "telnet",
    protocolLabel: "Telnet",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 52.83,
    uhqsFull: 64.9,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/telnet/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-telnet/",
    quick: "mkdocs/conformance/reports/opencanary/telnet/quick/",
    full: "mkdocs/conformance/reports/opencanary/telnet/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/telnet/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/telnet/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (Redis)",
    classLabel: "Low-Interaction · Redis :6379",
    protocol: "redis",
    protocolLabel: "Redis",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 45.07,
    uhqsFull: 53.72,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/redis/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-redis/",
    quick: "mkdocs/conformance/reports/opencanary/redis/quick/",
    full: "mkdocs/conformance/reports/opencanary/redis/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/redis/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/redis/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (MySQL)",
    classLabel: "Low-Interaction · MySQL :3306",
    protocol: "mysql",
    protocolLabel: "MySQL",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 51.48,
    uhqsFull: 62.96,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/mysql/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-mysql/",
    quick: "mkdocs/conformance/reports/opencanary/mysql/quick/",
    full: "mkdocs/conformance/reports/opencanary/mysql/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/mysql/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/mysql/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (RDP)",
    classLabel: "Low-Interaction · RDP :3389",
    protocol: "rdp",
    protocolLabel: "RDP",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 50.13,
    uhqsFull: 61.01,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/rdp/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-rdp/",
    quick: "mkdocs/conformance/reports/opencanary/rdp/quick/",
    full: "mkdocs/conformance/reports/opencanary/rdp/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/rdp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/rdp/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (SIP)",
    classLabel: "Low-Interaction · SIP :5060",
    protocol: "sip",
    protocolLabel: "SIP",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 40.01,
    uhqsFull: 46.44,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/opencanary/sip/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-sip/",
    quick: "mkdocs/conformance/reports/opencanary/sip/quick/",
    full: "mkdocs/conformance/reports/opencanary/sip/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/sip/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/sip/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (SNMP)",
    classLabel: "Low-Interaction · SNMP :161",
    protocol: "snmp",
    protocolLabel: "SNMP",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 40.69,
    uhqsFull: 47.42,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/opencanary/snmp/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-snmp/",
    quick: "mkdocs/conformance/reports/opencanary/snmp/quick/",
    full: "mkdocs/conformance/reports/opencanary/snmp/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/snmp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/snmp/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (NTP)",
    classLabel: "Low-Interaction · NTP :123",
    protocol: "ntp",
    protocolLabel: "NTP",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 40.69,
    uhqsFull: 47.42,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/opencanary/ntp/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-ntp/",
    quick: "mkdocs/conformance/reports/opencanary/ntp/quick/",
    full: "mkdocs/conformance/reports/opencanary/ntp/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/ntp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/ntp/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (TFTP)",
    classLabel: "Low-Interaction · TFTP :69",
    protocol: "tftp",
    protocolLabel: "TFTP",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 40.69,
    uhqsFull: 47.42,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/opencanary/tftp/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-tftp/",
    quick: "mkdocs/conformance/reports/opencanary/tftp/quick/",
    full: "mkdocs/conformance/reports/opencanary/tftp/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/tftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/tftp/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (VNC)",
    classLabel: "Low-Interaction · VNC :5900",
    protocol: "vnc",
    protocolLabel: "VNC",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 50.81,
    uhqsFull: 61.99,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/vnc/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-vnc/",
    quick: "mkdocs/conformance/reports/opencanary/vnc/quick/",
    full: "mkdocs/conformance/reports/opencanary/vnc/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/vnc/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/vnc/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (Git)",
    classLabel: "Low-Interaction · Git :9418",
    protocol: "git",
    protocolLabel: "Git",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 51.48,
    uhqsFull: 62.96,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/git/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-git/",
    quick: "mkdocs/conformance/reports/opencanary/git/quick/",
    full: "mkdocs/conformance/reports/opencanary/git/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/git/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/git/full/SCORECARD.txt",
  },
  {
    name: "OpenCanary (SMB)",
    classLabel: "Low-Interaction · SMB :445",
    protocol: "smb",
    protocolLabel: "SMB",
    repo: "https://github.com/thinkst/opencanary",
    repoUpdated: "2026-07-22",
    uhqsQuick: 50.13,
    uhqsFull: 57.72,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/opencanary/smb/",
    tutorial: "mkdocs/conformance/reports/opencanary/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/opencanary/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/opencanary-smb/",
    quick: "mkdocs/conformance/reports/opencanary/smb/quick/",
    full: "mkdocs/conformance/reports/opencanary/smb/full/",
    quickCard: "mkdocs/conformance/reports/opencanary/smb/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/opencanary/smb/full/SCORECARD.txt",
  },
  {
    name: "Beelzebub (HTTP)",
    classLabel: "Web-API · HTTP :8080",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/beelzebub-labs/beelzebub",
    repoUpdated: "2026-07-29",
    uhqsQuick: 52.77,
    uhqsFull: 66.02,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/beelzebub/http/",
    tutorial: "mkdocs/conformance/reports/beelzebub/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/beelzebub/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/beelzebub-http/",
    quick: "mkdocs/conformance/reports/beelzebub/http/quick/",
    full: "mkdocs/conformance/reports/beelzebub/http/full/",
    quickCard: "mkdocs/conformance/reports/beelzebub/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/beelzebub/http/full/SCORECARD.txt",
  },
  {
    name: "Beelzebub (Redis)",
    classLabel: "Low-Interaction · Redis :6379",
    protocol: "redis",
    protocolLabel: "Redis",
    repo: "https://github.com/beelzebub-labs/beelzebub",
    repoUpdated: "2026-07-29",
    uhqsQuick: 50.56,
    uhqsFull: 61.01,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/beelzebub/redis/",
    tutorial: "mkdocs/conformance/reports/beelzebub/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/beelzebub/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/beelzebub-redis/",
    quick: "mkdocs/conformance/reports/beelzebub/redis/quick/",
    full: "mkdocs/conformance/reports/beelzebub/redis/full/",
    quickCard: "mkdocs/conformance/reports/beelzebub/redis/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/beelzebub/redis/full/SCORECARD.txt",
  },
  {
    name: "Beelzebub (SSH)",
    classLabel: "Low-Interaction · SSH :2222",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/beelzebub-labs/beelzebub",
    repoUpdated: "2026-07-29",
    uhqsQuick: 74.45,
    uhqsFull: 59.88,
    gradeQuick: "C",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/beelzebub/ssh/",
    tutorial: "mkdocs/conformance/reports/beelzebub/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/beelzebub/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/beelzebub-ssh/",
    quick: "mkdocs/conformance/reports/beelzebub/ssh/quick/",
    full: "mkdocs/conformance/reports/beelzebub/ssh/full/",
    quickCard: "mkdocs/conformance/reports/beelzebub/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/beelzebub/ssh/full/SCORECARD.txt",
  },
  {
    name: "Beelzebub (Telnet)",
    classLabel: "Low-Interaction · Telnet :23",
    protocol: "telnet",
    protocolLabel: "Telnet",
    repo: "https://github.com/beelzebub-labs/beelzebub",
    repoUpdated: "2026-07-29",
    uhqsQuick: 39.16,
    uhqsFull: 47.89,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/beelzebub/telnet/",
    tutorial: "mkdocs/conformance/reports/beelzebub/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/beelzebub/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/beelzebub-telnet/",
    quick: "mkdocs/conformance/reports/beelzebub/telnet/quick/",
    full: "mkdocs/conformance/reports/beelzebub/telnet/full/",
    quickCard: "mkdocs/conformance/reports/beelzebub/telnet/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/beelzebub/telnet/full/SCORECARD.txt",
  },
  {
    name: "Beelzebub (MCP)",
    classLabel: "Web-API (MCP v1) · :8000",
    protocol: "mcp",
    protocolLabel: "MCP",
    repo: "https://github.com/beelzebub-labs/beelzebub",
    repoUpdated: "2026-07-29",
    uhqsQuick: 43.04,
    uhqsFull: 42.93,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/beelzebub/mcp/",
    tutorial: "mkdocs/conformance/reports/beelzebub/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/beelzebub/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/beelzebub-mcp/",
    quick: "mkdocs/conformance/reports/beelzebub/mcp/quick/",
    full: "mkdocs/conformance/reports/beelzebub/mcp/full/",
    quickCard: "mkdocs/conformance/reports/beelzebub/mcp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/beelzebub/mcp/full/SCORECARD.txt",
  },
  {
    name: "HoneyMCP (MCP)",
    classLabel: "Web-API (MCP v1) · :8080",
    protocol: "mcp",
    protocolLabel: "MCP",
    repo: "https://github.com/kosiorkosa47/honeymcp",
    repoUpdated: "2026-07-19",
    uhqsQuick: 43.04,
    uhqsFull: 42.93,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/honeymcp/mcp/",
    tutorial: "mkdocs/conformance/reports/honeymcp/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/honeymcp/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/honeymcp-mcp/",
    quick: "mkdocs/conformance/reports/honeymcp/mcp/quick/",
    full: "mkdocs/conformance/reports/honeymcp/mcp/full/",
    quickCard: "mkdocs/conformance/reports/honeymcp/mcp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/honeymcp/mcp/full/SCORECARD.txt",
  },
  {
    name: "Trapster Community (FTP)",
    classLabel: "Low-Interaction · FTP :2121",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/0xBallpoint/trapster-community",
    repoUpdated: "2026-07-27",
    uhqsQuick: 43.37,
    uhqsFull: 51.78,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/trapster/ftp/",
    tutorial: "mkdocs/conformance/reports/trapster/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/trapster/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/trapster-ftp/",
    quick: "mkdocs/conformance/reports/trapster/ftp/quick/",
    full: "mkdocs/conformance/reports/trapster/ftp/full/",
    quickCard: "mkdocs/conformance/reports/trapster/ftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/trapster/ftp/full/SCORECARD.txt",
  },
  {
    name: "Trapster Community (HTTP)",
    classLabel: "Web-API · HTTP :8080",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/0xBallpoint/trapster-community",
    repoUpdated: "2026-07-27",
    uhqsQuick: 50.13,
    uhqsFull: 63.33,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/trapster/http/",
    tutorial: "mkdocs/conformance/reports/trapster/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/trapster/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/trapster-http/",
    quick: "mkdocs/conformance/reports/trapster/http/quick/",
    full: "mkdocs/conformance/reports/trapster/http/full/",
    quickCard: "mkdocs/conformance/reports/trapster/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/trapster/http/full/SCORECARD.txt",
  },
  {
    name: "Trapster Community (SSH)",
    classLabel: "Low-Interaction · SSH :2222",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/0xBallpoint/trapster-community",
    repoUpdated: "2026-07-27",
    uhqsQuick: 40.06,
    uhqsFull: 44.38,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/trapster/ssh/",
    tutorial: "mkdocs/conformance/reports/trapster/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/trapster/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/trapster-ssh/",
    quick: "mkdocs/conformance/reports/trapster/ssh/quick/",
    full: "mkdocs/conformance/reports/trapster/ssh/full/",
    quickCard: "mkdocs/conformance/reports/trapster/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/trapster/ssh/full/SCORECARD.txt",
  },
  {
    name: "Trapster Community (Telnet)",
    classLabel: "Low-Interaction · Telnet :2323",
    protocol: "telnet",
    protocolLabel: "Telnet",
    repo: "https://github.com/0xBallpoint/trapster-community",
    repoUpdated: "2026-07-27",
    uhqsQuick: 52.49,
    uhqsFull: 64.9,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/trapster/telnet/",
    tutorial: "mkdocs/conformance/reports/trapster/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/trapster/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/trapster-telnet/",
    quick: "mkdocs/conformance/reports/trapster/telnet/quick/",
    full: "mkdocs/conformance/reports/trapster/telnet/full/",
    quickCard: "mkdocs/conformance/reports/trapster/telnet/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/trapster/telnet/full/SCORECARD.txt",
  },
  {
    name: "Dionaea (FTP)",
    classLabel: "Low-Interaction · FTP :21",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/dinotools/dionaea",
    repoUpdated: "2024-08-01",
    uhqsQuick: 50.95,
    uhqsFull: 57.96,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/dionaea/ftp/",
    tutorial: "mkdocs/conformance/reports/dionaea/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/dionaea/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/dionaea-ftp/",
    quick: "mkdocs/conformance/reports/dionaea/ftp/quick/",
    full: "mkdocs/conformance/reports/dionaea/ftp/full/",
    quickCard: "mkdocs/conformance/reports/dionaea/ftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/dionaea/ftp/full/SCORECARD.txt",
  },
  {
    name: "Dionaea (HTTP)",
    classLabel: "Web-API · HTTP :80",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/dinotools/dionaea",
    repoUpdated: "2024-08-01",
    uhqsQuick: 46.21,
    uhqsFull: 51.14,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/dionaea/http/",
    tutorial: "mkdocs/conformance/reports/dionaea/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/dionaea/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/dionaea-http/",
    quick: "mkdocs/conformance/reports/dionaea/http/quick/",
    full: "mkdocs/conformance/reports/dionaea/http/full/",
    quickCard: "mkdocs/conformance/reports/dionaea/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/dionaea/http/full/SCORECARD.txt",
  },
  {
    name: "Dionaea (SMB)",
    classLabel: "Low-Interaction · SMB :445",
    protocol: "smb",
    protocolLabel: "SMB",
    repo: "https://github.com/dinotools/dionaea",
    repoUpdated: "2024-08-01",
    uhqsQuick: 48.25,
    uhqsFull: 54.07,
    gradeQuick: "F",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/dionaea/smb/",
    tutorial: "mkdocs/conformance/reports/dionaea/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/dionaea/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/dionaea-smb/",
    quick: "mkdocs/conformance/reports/dionaea/smb/quick/",
    full: "mkdocs/conformance/reports/dionaea/smb/full/",
    quickCard: "mkdocs/conformance/reports/dionaea/smb/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/dionaea/smb/full/SCORECARD.txt",
  },

  {
    name: "Elastichoney",
    classLabel: "Web-API · HTTP :9200",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/jordan-wright/elastichoney",
    repoUpdated: "2015-07-14",
    uhqsQuick: 45.84,
    uhqsFull: 45.73,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/elastichoney/http/",
    tutorial: "mkdocs/conformance/reports/elastichoney/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/elastichoney/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/elastichoney-http/",
    quick: "mkdocs/conformance/reports/elastichoney/http/quick/",
    full: "mkdocs/conformance/reports/elastichoney/http/full/",
    quickCard: "mkdocs/conformance/reports/elastichoney/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/elastichoney/http/full/SCORECARD.txt",
  },
  {
    name: "honeypot-ftp",
    classLabel: "Low-Interaction · FTP :21",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/alexbredo/honeypot-ftp",
    repoUpdated: "2024-01-22",
    uhqsQuick: 42.71,
    uhqsFull: 42.6,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/honeypot-ftp/ftp/",
    tutorial: "mkdocs/conformance/reports/honeypot-ftp/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/honeypot-ftp/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/honeypot-ftp/",
    quick: "mkdocs/conformance/reports/honeypot-ftp/ftp/quick/",
    full: "mkdocs/conformance/reports/honeypot-ftp/ftp/full/",
    quickCard: "mkdocs/conformance/reports/honeypot-ftp/ftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/honeypot-ftp/ftp/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (SSH)",
    classLabel: "Low-Interaction · SSH :19022",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 59.88,
    uhqsFull: 59.68,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/ssh/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-ssh/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/ssh/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/ssh/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/ssh/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (HTTP)",
    classLabel: "Web-API · HTTP :19080",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 45.84,
    uhqsFull: 45.73,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/http/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-http/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/http/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/http/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/http/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (FTP)",
    classLabel: "Low-Interaction · FTP :19021",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 42.71,
    uhqsFull: 40.31,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/ftp/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-ftp/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/ftp/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/ftp/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/ftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/ftp/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (Telnet)",
    classLabel: "Low-Interaction · Telnet :19023",
    protocol: "telnet",
    protocolLabel: "Telnet",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 29.88,
    uhqsFull: 29.77,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/telnet/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-telnet/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/telnet/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/telnet/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/telnet/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/telnet/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (SMTP)",
    classLabel: "Low-Interaction · SMTP :19025",
    protocol: "smtp",
    protocolLabel: "SMTP",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 30.9,
    uhqsFull: 30.78,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/smtp/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-smtp/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/smtp/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/smtp/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/smtp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/smtp/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (POP3)",
    classLabel: "Low-Interaction · POP3 :19110",
    protocol: "pop3",
    protocolLabel: "POP3",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 31.06,
    uhqsFull: 30.94,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/pop3/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-pop3/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/pop3/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/pop3/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/pop3/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/pop3/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (MySQL)",
    classLabel: "Database · MySQL :19306",
    protocol: "mysql",
    protocolLabel: "MySQL",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 34.38,
    uhqsFull: 34.27,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/mysql/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-mysql/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/mysql/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/mysql/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/mysql/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/mysql/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (PostgreSQL)",
    classLabel: "Database · PostgreSQL :19432",
    protocol: "postgres",
    protocolLabel: "PostgreSQL",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 34.38,
    uhqsFull: 34.27,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/postgres/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-postgres/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/postgres/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/postgres/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/postgres/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/postgres/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (Redis)",
    classLabel: "Low-Interaction · Redis :19637",
    protocol: "redis",
    protocolLabel: "Redis",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 34.61,
    uhqsFull: 34.5,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/redis/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-redis/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/redis/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/redis/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/redis/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/redis/full/SCORECARD.txt",
  },
  {
    name: "qeeqbox (VNC)",
    classLabel: "Low-Interaction · VNC :19900",
    protocol: "vnc",
    protocolLabel: "VNC",
    repo: "https://github.com/qeeqbox/honeypots",
    repoUpdated: "2025-12-03",
    uhqsQuick: 32.92,
    uhqsFull: 32.81,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/qeeqbox-honeypots/vnc/",
    tutorial: "mkdocs/conformance/reports/qeeqbox-honeypots/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/qeeqbox-honeypots/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/qeeqbox-vnc/",
    quick: "mkdocs/conformance/reports/qeeqbox-honeypots/vnc/quick/",
    full: "mkdocs/conformance/reports/qeeqbox-honeypots/vnc/full/",
    quickCard: "mkdocs/conformance/reports/qeeqbox-honeypots/vnc/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/qeeqbox-honeypots/vnc/full/SCORECARD.txt",
  },
  {
    name: "sshesame",
    classLabel: "Low-Interaction · SSH",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/jaksi/sshesame",
    repoUpdated: "2024-10-21",
    uhqsQuick: 65.13,
    uhqsFull: 61.06,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/sshesame/ssh/",
    tutorial: "mkdocs/conformance/reports/sshesame/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/sshesame/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/sshesame-ssh/",
    quick: "mkdocs/conformance/reports/sshesame/ssh/quick/",
    full: "mkdocs/conformance/reports/sshesame/ssh/full/",
    quickCard: "mkdocs/conformance/reports/sshesame/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/sshesame/ssh/full/SCORECARD.txt",
  },
  {
    name: "ssh-auth-logger",
    classLabel: "Low-Interaction · SSH",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/JustinAzoff/ssh-auth-logger",
    repoUpdated: "2026-05-29",
    uhqsQuick: 44.38,
    uhqsFull: 44.38,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/ssh-auth-logger/ssh/",
    tutorial: "mkdocs/conformance/reports/ssh-auth-logger/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/ssh-auth-logger/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/ssh-auth-logger-ssh/",
    quick: "mkdocs/conformance/reports/ssh-auth-logger/ssh/quick/",
    full: "mkdocs/conformance/reports/ssh-auth-logger/ssh/full/",
    quickCard: "mkdocs/conformance/reports/ssh-auth-logger/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/ssh-auth-logger/ssh/full/SCORECARD.txt",
  },
  {
    name: "ssh-honeypotd",
    classLabel: "Low-Interaction · SSH",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/sjinks/ssh-honeypotd",
    repoUpdated: "2026-07-28",
    uhqsQuick: 44.38,
    uhqsFull: 44.38,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/ssh-honeypotd/ssh/",
    tutorial: "mkdocs/conformance/reports/ssh-honeypotd/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/ssh-honeypotd/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/ssh-honeypotd-ssh/",
    quick: "mkdocs/conformance/reports/ssh-honeypotd/ssh/quick/",
    full: "mkdocs/conformance/reports/ssh-honeypotd/ssh/full/",
    quickCard: "mkdocs/conformance/reports/ssh-honeypotd/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/ssh-honeypotd/ssh/full/SCORECARD.txt",
  },
  {
    name: "HellPot",
    classLabel: "Web-API · HTTP tarpit",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/yunginnanet/HellPot",
    repoUpdated: "2025-12-19",
    uhqsQuick: 43.98,
    uhqsFull: 43.87,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/HellPot/http/",
    tutorial: "mkdocs/conformance/reports/HellPot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/HellPot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/hellpot-http/",
    quick: "mkdocs/conformance/reports/HellPot/http/quick/",
    full: "mkdocs/conformance/reports/HellPot/http/full/",
    quickCard: "mkdocs/conformance/reports/HellPot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/HellPot/http/full/SCORECARD.txt",
  },
  {
    name: "HoneyWire",
    classLabel: "Web-API · HTTP (WebRouterDecoy)",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/andreicscs/HoneyWire",
    repoUpdated: "2026-07-19",
    uhqsQuick: 45.84,
    uhqsFull: 45.84,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/HoneyWire/http/",
    tutorial: "mkdocs/conformance/reports/HoneyWire/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/HoneyWire/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/honeywire-http/",
    quick: "mkdocs/conformance/reports/HoneyWire/http/quick/",
    full: "mkdocs/conformance/reports/HoneyWire/http/full/",
    quickCard: "mkdocs/conformance/reports/HoneyWire/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/HoneyWire/http/full/SCORECARD.txt",
  },
  {
    name: "express-honeypot",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/christophe77/express-honeypot",
    repoUpdated: "2026-06-22",
    uhqsQuick: 45.84,
    uhqsFull: 45.73,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/express-honeypot/http/",
    tutorial: "mkdocs/conformance/reports/express-honeypot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/express-honeypot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/express-honeypot-http/",
    quick: "mkdocs/conformance/reports/express-honeypot/http/quick/",
    full: "mkdocs/conformance/reports/express-honeypot/http/full/",
    quickCard: "mkdocs/conformance/reports/express-honeypot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/express-honeypot/http/full/SCORECARD.txt",
  },
  {
    name: "mailoney",
    classLabel: "Low-Interaction · SMTP",
    protocol: "smtp",
    protocolLabel: "SMTP",
    repo: "https://github.com/phin3has/mailoney",
    repoUpdated: "2026-05-22",
    uhqsQuick: 38.8,
    uhqsFull: 38.69,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/mailoney/smtp/",
    tutorial: "mkdocs/conformance/reports/mailoney/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/mailoney/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/mailoney-smtp/",
    quick: "mkdocs/conformance/reports/mailoney/smtp/quick/",
    full: "mkdocs/conformance/reports/mailoney/smtp/full/",
    quickCard: "mkdocs/conformance/reports/mailoney/smtp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/mailoney/smtp/full/SCORECARD.txt",
  },
  {
    name: "pghoney",
    classLabel: "Low-Interaction · PostgreSQL",
    protocol: "postgres",
    protocolLabel: "PostgreSQL",
    repo: "https://github.com/betheroot/pghoney",
    repoUpdated: "2024-05-20",
    uhqsQuick: 43.72,
    uhqsFull: 43.61,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/pghoney/postgres/",
    tutorial: "mkdocs/conformance/reports/pghoney/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/pghoney/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/pghoney-postgres/",
    quick: "mkdocs/conformance/reports/pghoney/postgres/quick/",
    full: "mkdocs/conformance/reports/pghoney/postgres/full/",
    quickCard: "mkdocs/conformance/reports/pghoney/postgres/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/pghoney/postgres/full/SCORECARD.txt",
  },
  {
    name: "mysql-honeypotd",
    classLabel: "Low-Interaction · MySQL",
    protocol: "mysql",
    protocolLabel: "MySQL",
    repo: "https://github.com/sjinks/mysql-honeypotd",
    repoUpdated: "2026-07-28",
    uhqsQuick: 40.35,
    uhqsFull: 37.94,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/mysql-honeypotd/mysql/",
    tutorial: "mkdocs/conformance/reports/mysql-honeypotd/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/mysql-honeypotd/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/mysql-honeypotd-mysql/",
    quick: "mkdocs/conformance/reports/mysql-honeypotd/mysql/quick/",
    full: "mkdocs/conformance/reports/mysql-honeypotd/mysql/full/",
    quickCard: "mkdocs/conformance/reports/mysql-honeypotd/mysql/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/mysql-honeypotd/mysql/full/SCORECARD.txt",
  },
  {
    name: "Log4Pot",
    classLabel: "Web-API · HTTP Log4Shell",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/thomaspatzke/Log4Pot",
    repoUpdated: "2024-11-29",
    uhqsQuick: 41.71,
    uhqsFull: 38.0,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/Log4Pot/http/",
    tutorial: "mkdocs/conformance/reports/Log4Pot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/Log4Pot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/log4pot-http/",
    quick: "mkdocs/conformance/reports/Log4Pot/http/quick/",
    full: "mkdocs/conformance/reports/Log4Pot/http/full/",
    quickCard: "mkdocs/conformance/reports/Log4Pot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/Log4Pot/http/full/SCORECARD.txt",
  },
  {
    name: "node-ftp-honeypot",
    classLabel: "Low-Interaction · FTP",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/christophe77/node-ftp-honeypot",
    repoUpdated: "2026-06-22",
    uhqsQuick: 35.96,
    uhqsFull: 35.85,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/node-ftp-honeypot/ftp/",
    tutorial: "mkdocs/conformance/reports/node-ftp-honeypot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/node-ftp-honeypot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/node-ftp-honeypot-ftp/",
    quick: "mkdocs/conformance/reports/node-ftp-honeypot/ftp/quick/",
    full: "mkdocs/conformance/reports/node-ftp-honeypot/ftp/full/",
    quickCard: "mkdocs/conformance/reports/node-ftp-honeypot/ftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/node-ftp-honeypot/ftp/full/SCORECARD.txt",
  },
  {
    name: "sentrypeer",
    classLabel: "Low-Interaction · SIP",
    protocol: "sip",
    protocolLabel: "SIP",
    repo: "https://github.com/SentryPeer/SentryPeer",
    repoUpdated: "2026-07-27",
    uhqsQuick: 43.38,
    uhqsFull: 43.38,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/sentrypeer/sip/",
    tutorial: "mkdocs/conformance/reports/sentrypeer/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/sentrypeer/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/sentrypeer-sip/",
    quick: "mkdocs/conformance/reports/sentrypeer/sip/quick/",
    full: "mkdocs/conformance/reports/sentrypeer/sip/full/",
    quickCard: "mkdocs/conformance/reports/sentrypeer/sip/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/sentrypeer/sip/full/SCORECARD.txt",
  },
  {
    name: "wordpot",
    classLabel: "Web-API · WordPress HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/gbrindisi/wordpot",
    repoUpdated: "2023-02-07",
    uhqsQuick: 41.71,
    uhqsFull: 41.6,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/wordpot/http/",
    tutorial: "mkdocs/conformance/reports/wordpot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/wordpot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/wordpot-http/",
    quick: "mkdocs/conformance/reports/wordpot/http/quick/",
    full: "mkdocs/conformance/reports/wordpot/http/full/",
    quickCard: "mkdocs/conformance/reports/wordpot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/wordpot/http/full/SCORECARD.txt",
  },
  {
    name: "mockssh",
    classLabel: "Low-Interaction · SSH",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/ncouture/MockSSH",
    repoUpdated: "2026-07-09",
    uhqsQuick: 59.2,
    uhqsFull: 59.0,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/mockssh/ssh/",
    tutorial: "mkdocs/conformance/reports/mockssh/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/mockssh/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/mockssh-ssh/",
    quick: "mkdocs/conformance/reports/mockssh/ssh/quick/",
    full: "mkdocs/conformance/reports/mockssh/ssh/full/",
    quickCard: "mkdocs/conformance/reports/mockssh/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/mockssh/ssh/full/SCORECARD.txt",
  },
  {
    name: "heralding (SSH)",
    classLabel: "Low-Interaction · SSH",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/johnnykv/heralding",
    repoUpdated: "2024-05-21",
    uhqsQuick: 44.38,
    uhqsFull: 44.18,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/heralding/ssh/",
    tutorial: "mkdocs/conformance/reports/heralding/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/heralding/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/heralding-ssh/",
    quick: "mkdocs/conformance/reports/heralding/ssh/quick/",
    full: "mkdocs/conformance/reports/heralding/ssh/full/",
    quickCard: "mkdocs/conformance/reports/heralding/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/heralding/ssh/full/SCORECARD.txt",
  },
  {
    name: "heralding (FTP)",
    classLabel: "Low-Interaction · FTP",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/johnnykv/heralding",
    repoUpdated: "2024-05-21",
    uhqsQuick: 35.96,
    uhqsFull: 35.85,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/heralding/ftp/",
    tutorial: "mkdocs/conformance/reports/heralding/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/heralding/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/heralding-ftp/",
    quick: "mkdocs/conformance/reports/heralding/ftp/quick/",
    full: "mkdocs/conformance/reports/heralding/ftp/full/",
    quickCard: "mkdocs/conformance/reports/heralding/ftp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/heralding/ftp/full/SCORECARD.txt",
  },
  {
    name: "heralding (SMTP)",
    classLabel: "Low-Interaction · SMTP",
    protocol: "smtp",
    protocolLabel: "SMTP",
    repo: "https://github.com/johnnykv/heralding",
    repoUpdated: "2024-05-21",
    uhqsQuick: 45.07,
    uhqsFull: 45.07,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/heralding/smtp/",
    tutorial: "mkdocs/conformance/reports/heralding/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/heralding/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/heralding-smtp/",
    quick: "mkdocs/conformance/reports/heralding/smtp/quick/",
    full: "mkdocs/conformance/reports/heralding/smtp/full/",
    quickCard: "mkdocs/conformance/reports/heralding/smtp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/heralding/smtp/full/SCORECARD.txt",
  },
  {
    name: "owasp-python-honeypot",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/OWASP/Python-Honeypot",
    repoUpdated: "2026-07-29",
    uhqsQuick: 43.98,
    uhqsFull: 43.98,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/owasp-python-honeypot/http/",
    tutorial: "mkdocs/conformance/reports/owasp-python-honeypot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/owasp-python-honeypot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/owasp-python-honeypot-http/",
    quick: "mkdocs/conformance/reports/owasp-python-honeypot/http/quick/",
    full: "mkdocs/conformance/reports/owasp-python-honeypot/http/full/",
    quickCard: "mkdocs/conformance/reports/owasp-python-honeypot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/owasp-python-honeypot/http/full/SCORECARD.txt",
  },
  {
    name: "owa-honeypot",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/joda32/owa-honeypot",
    repoUpdated: "2026-07-29",
    uhqsQuick: 41.71,
    uhqsFull: 41.71,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/owa-honeypot/http/",
    tutorial: "mkdocs/conformance/reports/owa-honeypot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/owa-honeypot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/owa-honeypot-http/",
    quick: "mkdocs/conformance/reports/owa-honeypot/http/quick/",
    full: "mkdocs/conformance/reports/owa-honeypot/http/full/",
    quickCard: "mkdocs/conformance/reports/owa-honeypot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/owa-honeypot/http/full/SCORECARD.txt",
  },
  {
    name: "honeyup",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/LogoiLab/honeyup",
    repoUpdated: "2026-07-29",
    uhqsQuick: 50.91,
    uhqsFull: 50.91,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/honeyup/http/",
    tutorial: "mkdocs/conformance/reports/honeyup/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/honeyup/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/honeyup-http/",
    quick: "mkdocs/conformance/reports/honeyup/http/quick/",
    full: "mkdocs/conformance/reports/honeyup/http/full/",
    quickCard: "mkdocs/conformance/reports/honeyup/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/honeyup/http/full/SCORECARD.txt",
  },
  {
    name: "modpot",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/referefref/modpot",
    repoUpdated: "2026-07-29",
    uhqsQuick: 50.91,
    uhqsFull: 50.91,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/modpot/http/",
    tutorial: "mkdocs/conformance/reports/modpot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/modpot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/modpot-http/",
    quick: "mkdocs/conformance/reports/modpot/http/quick/",
    full: "mkdocs/conformance/reports/modpot/http/full/",
    quickCard: "mkdocs/conformance/reports/modpot/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/modpot/http/full/SCORECARD.txt",
  },
  {
    name: "Krawl",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/BlessedRebuS/Krawl",
    repoUpdated: "2026-07-29",
    uhqsQuick: 50.91,
    uhqsFull: 50.91,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/Krawl/http/",
    tutorial: "mkdocs/conformance/reports/Krawl/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/Krawl/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/krawl-http/",
    quick: "mkdocs/conformance/reports/Krawl/http/quick/",
    full: "mkdocs/conformance/reports/Krawl/http/full/",
    quickCard: "mkdocs/conformance/reports/Krawl/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/Krawl/http/full/SCORECARD.txt",
  },
  {
    name: "flux",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/andrewmichaelsmith/flux",
    repoUpdated: "2026-07-29",
    uhqsQuick: 50.91,
    uhqsFull: 50.91,
    gradeQuick: "D",
    gradeFull: "D",
    hub: "mkdocs/conformance/reports/flux/http/",
    tutorial: "mkdocs/conformance/reports/flux/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/flux/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/flux-http/",
    quick: "mkdocs/conformance/reports/flux/http/quick/",
    full: "mkdocs/conformance/reports/flux/http/full/",
    quickCard: "mkdocs/conformance/reports/flux/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/flux/http/full/SCORECARD.txt",
  },
  {
    name: "fortigate-vpn-ssl",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/PeterGabaldon/Fortigate.VPN-SSL.Honeypot",
    repoUpdated: "2026-07-29",
    uhqsQuick: 46.78,
    uhqsFull: 46.78,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/fortigate-vpn-ssl/http/",
    tutorial: "mkdocs/conformance/reports/fortigate-vpn-ssl/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/fortigate-vpn-ssl/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/fortigate-vpn-ssl-http/",
    quick: "mkdocs/conformance/reports/fortigate-vpn-ssl/http/quick/",
    full: "mkdocs/conformance/reports/fortigate-vpn-ssl/http/full/",
    quickCard: "mkdocs/conformance/reports/fortigate-vpn-ssl/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/fortigate-vpn-ssl/http/full/SCORECARD.txt",
  },
  {
    name: "honeytrap",
    classLabel: "Low-Interaction · SSH",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/honeytrap/honeytrap",
    repoUpdated: "2026-07-29",
    uhqsQuick: 44.38,
    uhqsFull: 44.38,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/honeytrap/ssh/",
    tutorial: "mkdocs/conformance/reports/honeytrap/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/honeytrap/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/honeytrap-ssh/",
    quick: "mkdocs/conformance/reports/honeytrap/ssh/quick/",
    full: "mkdocs/conformance/reports/honeytrap/ssh/full/",
    quickCard: "mkdocs/conformance/reports/honeytrap/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/honeytrap/ssh/full/SCORECARD.txt",
  },
  {
    name: "portlurker",
    classLabel: "Low-Interaction · generic TCP",
    protocol: "generic",
    protocolLabel: "Generic",
    repo: "https://github.com/bartnv/portlurker",
    repoUpdated: "2026-07-29",
    uhqsQuick: 39.84,
    uhqsFull: 39.84,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/portlurker/generic/",
    tutorial: "mkdocs/conformance/reports/portlurker/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/portlurker/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/portlurker-generic/",
    quick: "mkdocs/conformance/reports/portlurker/generic/quick/",
    full: "mkdocs/conformance/reports/portlurker/generic/full/",
    quickCard: "mkdocs/conformance/reports/portlurker/generic/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/portlurker/generic/full/SCORECARD.txt",
  },
  {
    name: "sticky_elephant",
    classLabel: "Low-Interaction · PostgreSQL",
    protocol: "postgres",
    protocolLabel: "PostgreSQL",
    repo: "https://github.com/betheroot/sticky_elephant",
    repoUpdated: "2026-07-29",
    uhqsQuick: 40.35,
    uhqsFull: 38.06,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/sticky_elephant/postgres/",
    tutorial: "mkdocs/conformance/reports/sticky_elephant/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/sticky_elephant/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/sticky_elephant-postgres/",
    quick: "mkdocs/conformance/reports/sticky_elephant/postgres/quick/",
    full: "mkdocs/conformance/reports/sticky_elephant/postgres/full/",
    quickCard: "mkdocs/conformance/reports/sticky_elephant/postgres/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/sticky_elephant/postgres/full/SCORECARD.txt",
  },
  {
    name: "kippo",
    classLabel: "Low-Interaction · SSH",
    protocol: "ssh",
    protocolLabel: "SSH",
    repo: "https://github.com/desaster/kippo",
    repoUpdated: "2026-07-29",
    uhqsQuick: 35.64,
    uhqsFull: 35.64,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/kippo/ssh/",
    tutorial: "mkdocs/conformance/reports/kippo/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/kippo/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/kippo-ssh/",
    quick: "mkdocs/conformance/reports/kippo/ssh/quick/",
    full: "mkdocs/conformance/reports/kippo/ssh/full/",
    quickCard: "mkdocs/conformance/reports/kippo/ssh/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/kippo/ssh/full/SCORECARD.txt",
  },
  {
    name: "nosqlpot",
    classLabel: "Low-Interaction · Redis",
    protocol: "redis",
    protocolLabel: "Redis",
    repo: "https://github.com/torque59/nosqlpot",
    repoUpdated: "2026-07-29",
    uhqsQuick: 42.37,
    uhqsFull: 40.08,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/nosqlpot/redis/",
    tutorial: "mkdocs/conformance/reports/nosqlpot/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/nosqlpot/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/nosqlpot-redis/",
    quick: "mkdocs/conformance/reports/nosqlpot/redis/quick/",
    full: "mkdocs/conformance/reports/nosqlpot/redis/full/",
    quickCard: "mkdocs/conformance/reports/nosqlpot/redis/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/nosqlpot/redis/full/SCORECARD.txt",
  },
  {
    name: "pyRDP",
    classLabel: "Low-Interaction · RDP",
    protocol: "rdp",
    protocolLabel: "RDP",
    repo: "https://github.com/GoSecure/pyrdp",
    repoUpdated: "2026-07-29",
    uhqsQuick: 33.93,
    uhqsFull: 33.93,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/pyrdp/rdp/",
    tutorial: "mkdocs/conformance/reports/pyrdp/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/pyrdp/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/pyrdp-rdp/",
    quick: "mkdocs/conformance/reports/pyrdp/rdp/quick/",
    full: "mkdocs/conformance/reports/pyrdp/rdp/full/",
    quickCard: "mkdocs/conformance/reports/pyrdp/rdp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/pyrdp/rdp/full/SCORECARD.txt",
  },
  {
    name: "Artillery",
    classLabel: "Low-Interaction · generic TCP",
    protocol: "generic",
    protocolLabel: "Generic",
    repo: "https://github.com/BinaryDefense/artillery",
    repoUpdated: "2026-07-29",
    uhqsQuick: 39.84,
    uhqsFull: 37.55,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/artillery/generic/",
    tutorial: "mkdocs/conformance/reports/artillery/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/artillery/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/artillery-generic/",
    quick: "mkdocs/conformance/reports/artillery/generic/quick/",
    full: "mkdocs/conformance/reports/artillery/generic/full/",
    quickCard: "mkdocs/conformance/reports/artillery/generic/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/artillery/generic/full/SCORECARD.txt",
  },
  {
    name: "honeyhttpd",
    classLabel: "Web-API · HTTP",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/bocajspear1/honeyhttpd",
    repoUpdated: "2024-06-29",
    uhqsQuick: 45.84,
    uhqsFull: 45.73,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/honeyhttpd/http/",
    tutorial: "mkdocs/conformance/reports/honeyhttpd/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/honeyhttpd/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/honeyhttpd-http/",
    quick: "mkdocs/conformance/reports/honeyhttpd/http/quick/",
    full: "mkdocs/conformance/reports/honeyhttpd/http/full/",
    quickCard: "mkdocs/conformance/reports/honeyhttpd/http/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/honeyhttpd/http/full/SCORECARD.txt",
  },
  {
    name: "shiva",
    classLabel: "Low-Interaction · SMTP",
    protocol: "smtp",
    protocolLabel: "SMTP",
    repo: "https://github.com/shiva-spampot/shiva",
    repoUpdated: "2025-03-31",
    uhqsQuick: 45.07,
    uhqsFull: 44.96,
    gradeQuick: "F",
    gradeFull: "F",
    hub: "mkdocs/conformance/reports/shiva/smtp/",
    tutorial: "mkdocs/conformance/reports/shiva/TUTORIAL/",
    methodology: "mkdocs/conformance/reports/shiva/METHODOLOGY/",
    scorecard: "mkdocs/scorecards/shiva-smtp/",
    quick: "mkdocs/conformance/reports/shiva/smtp/quick/",
    full: "mkdocs/conformance/reports/shiva/smtp/full/",
    quickCard: "mkdocs/conformance/reports/shiva/smtp/quick/SCORECARD.txt",
    fullCard: "mkdocs/conformance/reports/shiva/smtp/full/SCORECARD.txt",
  },
];

const Results = () => {
  const [protocolFilter, setProtocolFilter] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState<"cards" | "list">("cards");
  const [page, setPage] = useState(0);
  const [sortKey, setSortKey] = useState<"uhqsQuick" | "uhqsFull" | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");
  const pageSize = viewMode === "cards" ? 3 : 12;

  const filteredLabs = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    let base =
      protocolFilter === "all"
        ? LAB_RESULTS
        : LAB_RESULTS.filter((lab) => lab.protocol === protocolFilter);
    if (q) {
      base = base.filter(
        (lab) =>
          lab.name.toLowerCase().includes(q) ||
          lab.repo.toLowerCase().includes(q) ||
          lab.protocolLabel.toLowerCase().includes(q) ||
          lab.classLabel.toLowerCase().includes(q),
      );
    }
    if (!sortKey) return base;
    return [...base].sort((a, b) => {
      const av = a[sortKey] ?? -1;
      const bv = b[sortKey] ?? -1;
      return sortDir === "asc" ? av - bv : bv - av;
    });
  }, [protocolFilter, searchQuery, sortKey, sortDir]);

  const pageCount = Math.max(1, Math.ceil(filteredLabs.length / pageSize));
  const safePage = Math.min(page, pageCount - 1);
  const pageLabs = filteredLabs.slice(safePage * pageSize, safePage * pageSize + pageSize);

  useEffect(() => {
    if (page !== safePage) setPage(safePage);
  }, [page, safePage]);

  const setFilter = (id: string) => {
    setProtocolFilter(id);
    setPage(0);
  };

  const toggleSort = (key: "uhqsQuick" | "uhqsFull") => {
    if (sortKey !== key) {
      setSortKey(key);
      setSortDir("desc");
    } else if (sortDir === "desc") {
      setSortDir("asc");
    } else {
      setSortKey(null);
      setSortDir("desc");
    }
  };

  const SortIcon = ({ column }: { column: "uhqsQuick" | "uhqsFull" }) => {
    if (sortKey !== column) {
      return <ArrowUpDown className="w-3 h-3 opacity-50" aria-hidden />;
    }
    return sortDir === "desc" ? (
      <ArrowDown className="w-3 h-3 text-primary" aria-hidden />
    ) : (
      <ArrowUp className="w-3 h-3 text-primary" aria-hidden />
    );
  };

  return (
    <section id="results" className="py-24 border-t border-border/50">
      <motion.div
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="mb-8">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4 flex items-center gap-3">
            <Terminal className="text-primary w-8 h-8" />
            Results
          </h2>
          <p className="text-secondary-foreground max-w-3xl">
            Published UHBS-Lab Docker runs — tutorials, quick + full scorecards, and methodology.
            Evaluation proof only (not endorsements). Prefer <span className="text-foreground font-mono text-sm">full/</span> for claim-grade numbers.
          </p>
        </motion.div>

        <motion.div variants={fadeUpVariant} className="mb-6 flex flex-col gap-4">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
          <div>
            <div className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground mb-3">
              Filter by protocol
            </div>
            <div className="flex flex-wrap gap-2" role="group" aria-label="Filter honeypot results by protocol">
              {PROTOCOL_FILTERS.map((opt) => {
                const active = protocolFilter === opt.id;
                const count =
                  opt.id === "all"
                    ? LAB_RESULTS.length
                    : LAB_RESULTS.filter((l) => l.protocol === opt.id).length;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    onClick={() => setFilter(opt.id)}
                    aria-pressed={active}
                    className={
                      active
                        ? "font-mono text-xs px-3 py-1.5 border border-primary bg-primary/15 text-primary"
                        : "font-mono text-xs px-3 py-1.5 border border-border text-secondary-foreground hover:border-primary/50 hover:text-primary transition-colors"
                    }
                  >
                    {opt.label}
                    <span className="ml-1.5 text-muted-foreground">({count})</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <div className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground mb-3">
              View
            </div>
            <div className="inline-flex border border-border" role="group" aria-label="Results view mode">
              <button
                type="button"
                onClick={() => {
                  setViewMode("cards");
                  setPage(0);
                }}
                aria-pressed={viewMode === "cards"}
                className={
                  viewMode === "cards"
                    ? "inline-flex items-center gap-1.5 font-mono text-xs px-3 py-1.5 bg-primary/15 text-primary border-r border-border"
                    : "inline-flex items-center gap-1.5 font-mono text-xs px-3 py-1.5 text-secondary-foreground hover:text-primary border-r border-border"
                }
              >
                <LayoutGrid className="w-3.5 h-3.5" aria-hidden />
                Cards
              </button>
              <button
                type="button"
                onClick={() => {
                  setViewMode("list");
                  setPage(0);
                }}
                aria-pressed={viewMode === "list"}
                className={
                  viewMode === "list"
                    ? "inline-flex items-center gap-1.5 font-mono text-xs px-3 py-1.5 bg-primary/15 text-primary"
                    : "inline-flex items-center gap-1.5 font-mono text-xs px-3 py-1.5 text-secondary-foreground hover:text-primary"
                }
              >
                <List className="w-3.5 h-3.5" aria-hidden />
                List
              </button>
            </div>
          </div>
          </div>

          <label className="relative block max-w-md">
            <span className="sr-only">Search results by name or repository</span>
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" aria-hidden />
            <input
              type="search"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setPage(0);
              }}
              placeholder="Search by name or repo…"
              className="w-full bg-background border border-border pl-9 pr-3 py-2 font-mono text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50"
            />
          </label>
        </motion.div>

        {filteredLabs.length === 0 && (
          <p className="font-mono text-sm text-muted-foreground mb-10">
            No published labs for this protocol filter{searchQuery.trim() ? " / search" : ""}.
          </p>
        )}

        {viewMode === "cards" && filteredLabs.length > 0 && (
          <div className="mb-12">
            <div className="flex items-stretch gap-2 sm:gap-3">
              <button
                type="button"
                onClick={() => setPage((p) => Math.max(0, Math.min(p, pageCount - 1) - 1))}
                disabled={safePage <= 0}
                aria-label="Previous three results"
                className="shrink-0 self-center w-10 h-10 flex items-center justify-center border border-border text-secondary-foreground hover:border-primary/50 hover:text-primary disabled:opacity-25 disabled:hover:border-border disabled:hover:text-secondary-foreground transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 flex-1 min-w-0">
                {pageLabs.map((lab) => (
                  <div
                    key={lab.name}
                    className="bg-card border border-border p-6 terminal-card flex flex-col"
                  >
                    <div className="font-mono text-xs text-primary uppercase tracking-wider mb-2">{lab.classLabel}</div>
                    <h3 className="text-xl font-bold mb-1">
                      <a href={lab.hub} className="hover:text-primary transition-colors">{lab.name}</a>
                    </h3>
                    <a
                      href={lab.repo}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-mono text-xs text-secondary-foreground hover:text-primary transition-colors inline-flex items-center gap-1"
                    >
                      Original project <ArrowRight className="w-3 h-3" />
                    </a>
                    <div className="font-mono text-[10px] text-muted-foreground mb-4 mt-1">
                      GitHub last push {lab.repoUpdated}
                    </div>

                    <div className="grid grid-cols-2 gap-3 mb-6 font-mono text-sm">
                      <div className="border border-border/60 p-3">
                        <div className="text-[10px] uppercase tracking-wider text-muted-foreground mb-1">Quick</div>
                        <div className="text-primary font-bold text-lg">{lab.uhqsQuick == null ? "—" : lab.uhqsQuick.toFixed(2)}</div>
                        <div className="text-xs text-secondary-foreground">Grade {lab.gradeQuick}</div>
                      </div>
                      <div className="border border-primary/30 bg-primary/5 p-3">
                        <div className="text-[10px] uppercase tracking-wider text-muted-foreground mb-1">Full</div>
                        <div className="text-primary font-bold text-lg">{lab.uhqsFull == null ? "—" : lab.uhqsFull.toFixed(2)}</div>
                        <div className="text-xs text-secondary-foreground">Grade {lab.gradeFull}</div>
                      </div>
                    </div>

                    <div className="mt-auto space-y-4 font-mono text-xs">
                      <div>
                        <div className="text-muted-foreground uppercase tracking-wider text-[10px] mb-2">Guides</div>
                        <div className="flex flex-col gap-1.5">
                          <a href={lab.tutorial} className="text-primary hover:underline flex items-center gap-1">
                            Tutorial <ArrowRight className="w-3 h-3" />
                          </a>
                          <a href={lab.methodology} className="text-secondary-foreground hover:text-primary transition-colors flex items-center gap-1">
                            Methodology <ArrowRight className="w-3 h-3" />
                          </a>
                          <a href={lab.hub} className="text-secondary-foreground hover:text-primary transition-colors flex items-center gap-1">
                            Report hub <ArrowRight className="w-3 h-3" />
                          </a>
                        </div>
                      </div>
                      <div>
                        <div className="text-muted-foreground uppercase tracking-wider text-[10px] mb-2">Runs & scorecards</div>
                        <div className="flex flex-col gap-1.5">
                          <a href={lab.scorecard} className="text-primary hover:underline flex items-center gap-1">
                            Published scorecard page <ArrowRight className="w-3 h-3" />
                          </a>
                          <a href={lab.full} className="text-secondary-foreground hover:text-primary transition-colors flex items-center gap-1">
                            Full run artifacts <ArrowRight className="w-3 h-3" />
                          </a>
                          <a href={lab.fullCard} className="text-secondary-foreground hover:text-primary transition-colors flex items-center gap-1">
                            Full SCORECARD.txt <ArrowRight className="w-3 h-3" />
                          </a>
                          <a href={lab.quick} className="text-secondary-foreground hover:text-primary transition-colors flex items-center gap-1">
                            Quick run artifacts <ArrowRight className="w-3 h-3" />
                          </a>
                          <a href={lab.quickCard} className="text-secondary-foreground hover:text-primary transition-colors flex items-center gap-1">
                            Quick SCORECARD.txt <ArrowRight className="w-3 h-3" />
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <button
                type="button"
                onClick={() => setPage((p) => Math.min(pageCount - 1, Math.min(p, pageCount - 1) + 1))}
                disabled={safePage >= pageCount - 1}
                aria-label="Next three results"
                className="shrink-0 self-center w-10 h-10 flex items-center justify-center border border-border text-secondary-foreground hover:border-primary/50 hover:text-primary disabled:opacity-25 disabled:hover:border-border disabled:hover:text-secondary-foreground transition-colors"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>

            {pageCount > 1 && (
              <div className="mt-4 flex items-center justify-center gap-2 font-mono text-[10px] text-muted-foreground tracking-wide">
                <span>
                  {safePage + 1} / {pageCount}
                </span>
                <span className="text-border">·</span>
                <span>
                  {safePage * pageSize + 1}–{Math.min(filteredLabs.length, (safePage + 1) * pageSize)} of {filteredLabs.length}
                </span>
              </div>
            )}
          </div>
        )}

        {viewMode === "list" && filteredLabs.length > 0 && (
          <div className="mb-12">
          <div className="overflow-x-auto border border-border">
            <table className="w-full text-left text-sm font-mono">
              <thead>
                <tr className="border-b border-border bg-card text-muted-foreground text-xs uppercase tracking-wider">
                  <th className="py-3 px-4 font-normal">Target</th>
                  <th className="py-3 px-4 font-normal">Protocol</th>
                  <th className="py-3 px-4 font-normal">Project</th>
                  <th className="py-3 px-4 font-normal">Tutorial</th>
                  <th className="py-3 px-4 font-normal">
                    <button
                      type="button"
                      onClick={() => toggleSort("uhqsQuick")}
                      className="inline-flex items-center gap-1.5 hover:text-primary transition-colors"
                      aria-label={`Sort by Quick UHQS${sortKey === "uhqsQuick" ? `, currently ${sortDir === "desc" ? "high to low" : "low to high"}` : ""}`}
                    >
                      Quick
                      <SortIcon column="uhqsQuick" />
                    </button>
                  </th>
                  <th className="py-3 px-4 font-normal">
                    <button
                      type="button"
                      onClick={() => toggleSort("uhqsFull")}
                      className="inline-flex items-center gap-1.5 hover:text-primary transition-colors"
                      aria-label={`Sort by Full UHQS${sortKey === "uhqsFull" ? `, currently ${sortDir === "desc" ? "high to low" : "low to high"}` : ""}`}
                    >
                      Full
                      <SortIcon column="uhqsFull" />
                    </button>
                  </th>
                  <th className="py-3 px-4 font-normal">Scorecard</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {pageLabs.map((lab) => (
                  <tr key={`row-${lab.name}`} className="hover:bg-card/80">
                    <td className="py-3 px-4 text-foreground font-semibold">
                      <a href={lab.hub} className="hover:text-primary">{lab.name}</a>
                      <div className="text-[10px] text-muted-foreground font-normal mt-0.5">{lab.classLabel}</div>
                    </td>
                    <td className="py-3 px-4 text-secondary-foreground">{lab.protocolLabel}</td>
                    <td className="py-3 px-4">
                      <a href={lab.repo} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">GitHub</a>
                      <div className="text-[10px] text-muted-foreground mt-0.5">Updated {lab.repoUpdated}</div>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.tutorial} className="text-primary hover:underline">Open</a>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.quickCard} className="text-secondary-foreground hover:text-primary">{lab.uhqsQuick == null ? "—" : `${lab.uhqsQuick.toFixed(2)} / ${lab.gradeQuick}`}</a>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.fullCard} className="text-secondary-foreground hover:text-primary">{lab.uhqsFull == null ? "—" : `${lab.uhqsFull.toFixed(2)} / ${lab.gradeFull}`}</a>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.scorecard} className="text-primary hover:underline">Page</a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {pageCount > 1 && (
            <div className="mt-4 flex items-center justify-center gap-3 font-mono text-[10px] text-muted-foreground tracking-wide">
              <button
                type="button"
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={safePage <= 0}
                className="px-2 py-1 border border-border hover:border-primary/50 disabled:opacity-25"
                aria-label="Previous list page"
              >
                Prev
              </button>
              <span>
                {safePage + 1} / {pageCount} · {safePage * pageSize + 1}–{Math.min(filteredLabs.length, (safePage + 1) * pageSize)} of {filteredLabs.length}
              </span>
              <button
                type="button"
                onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))}
                disabled={safePage >= pageCount - 1}
                className="px-2 py-1 border border-border hover:border-primary/50 disabled:opacity-25"
                aria-label="Next list page"
              >
                Next
              </button>
            </div>
          )}
          </div>
        )}

        <motion.div variants={fadeUpVariant} className="flex flex-wrap gap-4 font-mono text-sm">
          <a href="mkdocs/conformance/reports/" className="inline-flex items-center gap-2 border border-border px-4 py-2 hover:border-primary/50 transition-colors">
            All lab reports <ArrowRight className="w-4 h-4 text-primary" />
          </a>
          <a href="mkdocs/scorecards/" className="inline-flex items-center gap-2 border border-border px-4 py-2 hover:border-primary/50 transition-colors">
            All scorecards <ArrowRight className="w-4 h-4 text-primary" />
          </a>
          <a href="mkdocs/tooling/cli/" className="inline-flex items-center gap-2 border border-border px-4 py-2 hover:border-primary/50 transition-colors">
            Docker / CLI guide <ArrowRight className="w-4 h-4 text-primary" />
          </a>
          <a href="mkdocs/tooling/mcp/" className="inline-flex items-center gap-2 border border-border px-4 py-2 hover:border-primary/50 transition-colors">
            MCP for AI hosts <ArrowRight className="w-4 h-4 text-primary" />
          </a>
        </motion.div>
      </motion.div>
    </section>
  );
};

// Section: MCP for AI hosts (AEO / agent tooling)
const McpForAgents = () => {
  return (
    <section id="mcp" className="py-24 border-t border-border/50 bg-[#0f1629]/40">
      <motion.div
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="max-w-3xl mb-10">
          <div className="flex items-center gap-3 mb-4">
            <Terminal className="w-7 h-7 text-primary" />
            <h2 className="text-3xl font-bold font-sans">MCP for AI hosts</h2>
          </div>
          <p className="text-secondary-foreground text-lg font-light leading-relaxed">
            Optional local stdio server so Cursor, Claude Desktop, VS Code, and other
            MCP clients can validate scorecards and recompute UHQS without inventing math.
            Live Docker lab probes stay on the CLI.
          </p>
        </motion.div>

        <motion.div
          variants={fadeUpVariant}
          className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10 font-mono text-sm"
        >
          {[
            { title: "Validate", body: "scorecard · profile · evidence schemas + UHQS integrity" },
            { title: "Score", body: "compute_uhqs / δ_C from uhqs_math — same as uhbs score" },
            { title: "Discover", body: "fixtures, lab report hubs, scoring-formula resource" },
          ].map((card) => (
            <div key={card.title} className="border border-border/60 bg-card/50 p-5">
              <div className="text-primary mb-2">{card.title}</div>
              <div className="text-muted-foreground text-xs leading-relaxed">{card.body}</div>
            </div>
          ))}
        </motion.div>

        <motion.pre
          variants={fadeUpVariant}
          className="bg-background border border-border/60 p-5 overflow-x-auto text-xs font-mono text-secondary-foreground mb-8"
        >{`pip install -e ".[mcp]"
# mcpServers.uhbs → python -m uhbs_mcp  (set UHBS_ROOT to checkout)`}</motion.pre>

        <motion.div variants={fadeUpVariant} className="flex flex-wrap gap-4 font-mono text-sm">
          <a href="mkdocs/tooling/mcp/" className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 hover:opacity-90">
            MCP install guide <ArrowRight className="w-4 h-4" />
          </a>
          <a href="https://github.com/uhbs/uhbs-standard/blob/main/server.json" className="inline-flex items-center gap-2 border border-border px-4 py-2 hover:border-primary/50">
            server.json
          </a>
          <a href="llms.txt" className="inline-flex items-center gap-2 border border-border px-4 py-2 hover:border-primary/50">
            llms.txt
          </a>
        </motion.div>
      </motion.div>
    </section>
  );
};

// Section: Latest experimental changes
const LatestChanges = () => {
  const items = [
    {
      title: "Five-dimension matrix",
      body: "Equal-weight experimental scores with explicit missing dimensions and sensitivity analysis.",
      links: [
        { href: "mkdocs/experimental/", label: "Overview" },
        { href: "mkdocs/experimental/tutorial-matrix-beginner/", label: "Beginner tutorial" },
        { href: "mkdocs/experimental/cli-matrix/", label: "CLI" },
      ],
    },
    {
      title: "GenAI / MCP bench",
      body: "Deterministic replay metrics (CLR, SCR, TTFT). Tarpit-aware timing; not exposed via uhbs-mcp.",
      links: [
        { href: "mkdocs/experimental/tutorial-genai-beginner/", label: "Beginner tutorial" },
        { href: "mkdocs/experimental/cli-genai-bench/", label: "CLI" },
        { href: "mkdocs/architecture/experimental-benchmarks/", label: "Architecture" },
      ],
    },
    {
      title: "Host provenance",
      body: "Collector-neutral summaries with rate limits before hashing. Optional signed envelopes later.",
      links: [
        { href: "mkdocs/experimental/tutorial-provenance-beginner/", label: "Beginner tutorial" },
        { href: "mkdocs/experimental/cli-provenance/", label: "CLI" },
      ],
    },
    {
      title: "OT / ICS verification",
      body: "Hardened Modbus/S7 timeouts and expanding BACnet/MQTT/CoAP plugins (lab).",
      links: [
        { href: "mkdocs/experimental/", label: "Experimental hub" },
        { href: "mkdocs/plugin-authoring/", label: "Plugin authoring" },
        { href: "mkdocs/conformance/reports/conpot/TUTORIAL/", label: "Conpot tutorial" },
      ],
    },
  ];

  return (
    <section id="latest" className="py-24 border-t border-border/50 bg-[#0a0e1a]">
      <motion.div
        className="container mx-auto px-6"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={staggerContainer}
      >
        <motion.div variants={fadeUpVariant} className="mb-4 flex items-center gap-3">
          <div className="h-px w-8 bg-primary"></div>
          <span className="font-mono text-primary uppercase tracking-widest text-xs">
            Latest changes
          </span>
        </motion.div>
        <motion.div variants={fadeUpVariant} className="mb-10 max-w-3xl">
          <h2 className="text-3xl md:text-4xl font-bold font-sans mb-4">
            Experimental additions
          </h2>
          <p className="text-secondary-foreground leading-relaxed mb-3">
            New opt-in surfaces for research and high-assurance labs.{" "}
            <span className="text-foreground font-medium">They do not change UHQS</span>,
            weights, or the Safety Gate δ<sub>C</sub>.
          </p>
          <p className="text-sm font-mono text-muted-foreground">
            Details:{" "}
            <a
              href="https://github.com/uhbs/uhbs-standard/blob/main/CHANGELOG.md"
              className="text-primary hover:underline"
            >
              CHANGELOG
            </a>
            {" · "}
            <a href="mkdocs/rfcs/0002-experimental-benchmark-extensions/" className="text-primary hover:underline">
              RFC 0002
            </a>
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-8">
          {items.map((item) => (
            <motion.div
              key={item.title}
              variants={fadeUpVariant}
              className="border border-border/60 bg-card/40 p-6"
            >
              <div className="flex items-center gap-2 mb-2">
                <h3 className="font-sans text-lg font-semibold">{item.title}</h3>
                <span className="text-[10px] uppercase tracking-wider font-mono text-warning border border-warning/40 px-1.5 py-0.5">
                  Experimental
                </span>
              </div>
              <p className="text-sm text-secondary-foreground leading-relaxed mb-4">{item.body}</p>
              <div className="flex flex-wrap gap-3 font-mono text-xs">
                {item.links.map((link) => (
                  <a
                    key={link.href}
                    href={link.href}
                    className="inline-flex items-center gap-1 text-primary hover:underline"
                  >
                    {link.label} <ArrowRight className="w-3 h-3" aria-hidden="true" />
                  </a>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
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
          Universal Honeypot Benchmarking Standard <span className="text-primary/70">·</span> v4.5.1 <span className="text-primary/70">·</span> 2026
        </div>
        <p className="text-xs text-muted-foreground max-w-lg mx-auto mb-6">
          Open-source beta-status evaluation framework (Apache-2.0). Not a consortium, Steering Committee, or adopted industry standard.
        </p>
        <div className="flex flex-wrap justify-center gap-6 font-mono text-xs text-muted-foreground">
          <a href="mkdocs/" className="hover:text-primary transition-colors">Docs</a>
          <a href="#latest" className="hover:text-primary transition-colors">Latest</a>
          <a href="#results" className="hover:text-primary transition-colors">Results</a>
          <a href="#mcp" className="hover:text-primary transition-colors">MCP</a>
          <a href="https://github.com/uhbs/uhbs-standard/blob/main/CHANGELOG.md" className="hover:text-primary transition-colors">Changelog</a>
          <a href="mkdocs/scorecards/" className="hover:text-primary transition-colors">Scorecards</a>
          <a href="mkdocs/conformance/reports/" className="hover:text-primary transition-colors">Lab reports</a>
          <a href="https://github.com/uhbs/uhbs-standard" className="hover:text-primary transition-colors">GitHub</a>
          <a href="llms.txt" className="hover:text-primary transition-colors">llms.txt</a>
          <a href="llms-full.txt" className="hover:text-primary transition-colors">llms-full.txt</a>
          <a href="sitemap.xml" className="hover:text-primary transition-colors">sitemap</a>
          <a href=".well-known/security.txt" className="hover:text-primary transition-colors">security.txt</a>
          <a href="#scoring" className="hover:text-primary transition-colors">UHQS &gt; 80 beta gate</a>
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
            <a href="#compare" className="hover:text-primary transition-colors">Compare</a>
            <a href="#scoring" className="hover:text-primary transition-colors">Scoring</a>
            <a href="#results" className="hover:text-primary transition-colors text-primary/80">Results</a>
            <a href="#latest" className="hover:text-primary transition-colors">Latest</a>
            <a href="#mcp" className="hover:text-primary transition-colors">MCP</a>
            <a href="mkdocs/" className="hover:text-primary transition-colors border border-border/60 px-2 py-1">Docs</a>
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
        <AdvancedEvidenceProfile />
        <AuditWorkflow />
        <Results />
        <LatestChanges />
        <McpForAgents />
      </main>

      <Footer />
    </div>
  );
}
