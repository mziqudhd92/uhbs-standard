import { useMemo } from "react";
import katex from "katex";

type KatexMathProps = {
  tex: string;
  display?: boolean;
  className?: string;
  /** Accessible plain-language description when TeX is not enough */
  label?: string;
};

/** Render TeX with KaTeX (https://katex.org — MIT). */
export function KatexMath({ tex, display = false, className, label }: KatexMathProps) {
  const html = useMemo(
    () =>
      katex.renderToString(tex, {
        displayMode: display,
        throwOnError: false,
        strict: "ignore",
        output: "html",
      }),
    [tex, display],
  );

  return (
    <span
      className={className}
      role="img"
      aria-label={label ?? tex}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
