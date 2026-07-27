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
          <span className="text-muted-foreground font-mono text-4xl md:text-6xl tracking-tighter">(UHBS) v4.0 <span className="text-primary/70">· 2026</span></span>
        </motion.h1>
        
        <motion.p variants={fadeUpVariant} className="text-xl md:text-2xl text-secondary-foreground max-w-3xl mb-8 font-light leading-relaxed">
          An objective, repeatable, quantitative methodology for benchmarking honeypots, decoys, and deception technology — a personal open-source beta (not a consortium standard).
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
          <a href="https://github.com/mziqudhd92/uhbs-standard" className="inline-flex items-center gap-2 bg-card border border-border px-5 py-2.5 font-mono text-sm hover:border-primary/50 transition-colors">
            GitHub
          </a>
        </motion.div>
        
        <motion.div variants={fadeUpVariant} className="flex flex-wrap gap-4 mt-2">
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
                Historically, deception technology has been evaluated subjectively. UHBS introduces a verifiable, deterministic mathematical model designed to expose flaws in protocol state machines, containment boundaries, and behavioral realism.
              </p>
            </div>
            
            <div className="mt-8 bg-primary/5 border-l-4 border-primary/50 p-6">
              <div className="flex items-start gap-4">
                <Shield className="w-6 h-6 text-primary shrink-0 mt-1" />
                <div>
                  <h4 className="text-primary font-semibold font-mono mb-2 uppercase tracking-wide text-sm">Vendor-Neutral Beta Baseline</h4>
                  <p className="text-secondary-foreground text-sm">
                    UHBS v4.0 is a personal open-source beta for comparing and grading honeypots by class and protocol — mathematically reproducible, not a consortium or adopted industry standard.
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
      right: { label: "UHBS v4.0", text: "Target Profile Specification (profile.yaml) adjusts evaluation weights. ICS-SCADA weights protocol fidelity at w_A = 0.35, while POSIX shells emphasize state behavior at w_B = 0.25." },
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
          <motion.div variants={fadeUpVariant} className="lg:col-span-7 bg-card border border-border p-4 md:p-6">
            <div className="flex flex-wrap items-center justify-between gap-3 mb-4 px-2">
              <h3 className="font-mono text-primary text-sm uppercase tracking-wider">The UHQS 4.0 Formula</h3>
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
  uhqsQuick: number;
  uhqsFull: number;
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
  { id: "pjl", label: "PJL" },
  { id: "modbus", label: "Modbus" },
] as const;

const LAB_RESULTS: LabResult[] = [
  {
    name: "ESPot",
    classLabel: "Web-API · HTTP :9200",
    protocol: "http",
    protocolLabel: "HTTP",
    repo: "https://github.com/mycert/ESPot",
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
    name: "Endlessh",
    classLabel: "Low-Interaction · ssh_tarpit :2222",
    protocol: "ssh_tarpit",
    protocolLabel: "SSH tarpit",
    repo: "https://github.com/skeeto/endlessh",
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
    name: "Trapster Community (FTP)",
    classLabel: "Low-Interaction · FTP :2121",
    protocol: "ftp",
    protocolLabel: "FTP",
    repo: "https://github.com/0xBallpoint/trapster-community",
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
];

const Results = () => {
  const [protocolFilter, setProtocolFilter] = useState<string>("all");
  const [viewMode, setViewMode] = useState<"cards" | "list">("cards");
  const [page, setPage] = useState(0);
  const [sortKey, setSortKey] = useState<"uhqsQuick" | "uhqsFull" | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");
  const pageSize = 3;

  const filteredLabs = useMemo(() => {
    const base =
      protocolFilter === "all"
        ? LAB_RESULTS
        : LAB_RESULTS.filter((lab) => lab.protocol === protocolFilter);
    if (!sortKey) return base;
    return [...base].sort((a, b) => {
      const av = a[sortKey];
      const bv = b[sortKey];
      return sortDir === "asc" ? av - bv : bv - av;
    });
  }, [protocolFilter, sortKey, sortDir]);

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

        <motion.div variants={fadeUpVariant} className="mb-6 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
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
                onClick={() => setViewMode("cards")}
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
                onClick={() => setViewMode("list")}
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
        </motion.div>

        {filteredLabs.length === 0 && (
          <p className="font-mono text-sm text-muted-foreground mb-10">
            No published labs for this protocol filter.
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
                      className="font-mono text-xs text-secondary-foreground hover:text-primary transition-colors mb-4 inline-flex items-center gap-1"
                    >
                      Original project <ArrowRight className="w-3 h-3" />
                    </a>

                    <div className="grid grid-cols-2 gap-3 mb-6 font-mono text-sm">
                      <div className="border border-border/60 p-3">
                        <div className="text-[10px] uppercase tracking-wider text-muted-foreground mb-1">Quick</div>
                        <div className="text-primary font-bold text-lg">{lab.uhqsQuick.toFixed(2)}</div>
                        <div className="text-xs text-secondary-foreground">Grade {lab.gradeQuick}</div>
                      </div>
                      <div className="border border-primary/30 bg-primary/5 p-3">
                        <div className="text-[10px] uppercase tracking-wider text-muted-foreground mb-1">Full</div>
                        <div className="text-primary font-bold text-lg">{lab.uhqsFull.toFixed(2)}</div>
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
          <div className="overflow-x-auto border border-border mb-12">
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
                {filteredLabs.map((lab) => (
                  <tr key={`row-${lab.name}`} className="hover:bg-card/80">
                    <td className="py-3 px-4 text-foreground font-semibold">
                      <a href={lab.hub} className="hover:text-primary">{lab.name}</a>
                      <div className="text-[10px] text-muted-foreground font-normal mt-0.5">{lab.classLabel}</div>
                    </td>
                    <td className="py-3 px-4 text-secondary-foreground">{lab.protocolLabel}</td>
                    <td className="py-3 px-4">
                      <a href={lab.repo} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">GitHub</a>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.tutorial} className="text-primary hover:underline">Open</a>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.quickCard} className="text-secondary-foreground hover:text-primary">{lab.uhqsQuick.toFixed(2)} / {lab.gradeQuick}</a>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.fullCard} className="text-secondary-foreground hover:text-primary">{lab.uhqsFull.toFixed(2)} / {lab.gradeFull}</a>
                    </td>
                    <td className="py-3 px-4">
                      <a href={lab.scorecard} className="text-primary hover:underline">Page</a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
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
          <a href="https://github.com/mziqudhd92/uhbs-standard/blob/main/server.json" className="inline-flex items-center gap-2 border border-border px-4 py-2 hover:border-primary/50">
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
          Personal open-source beta evaluation framework (Apache-2.0). Not a consortium, Steering Committee, or adopted industry standard.
        </p>
        <div className="flex flex-wrap justify-center gap-6 font-mono text-xs text-muted-foreground">
          <a href="mkdocs/" className="hover:text-primary transition-colors">Docs</a>
          <a href="#results" className="hover:text-primary transition-colors">Results</a>
          <a href="#mcp" className="hover:text-primary transition-colors">MCP</a>
          <a href="mkdocs/scorecards/" className="hover:text-primary transition-colors">Scorecards</a>
          <a href="mkdocs/conformance/reports/" className="hover:text-primary transition-colors">Lab reports</a>
          <a href="https://github.com/mziqudhd92/uhbs-standard" className="hover:text-primary transition-colors">GitHub</a>
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
        <AuditWorkflow />
        <Results />
        <McpForAgents />
      </main>

      <Footer />
    </div>
  );
}
