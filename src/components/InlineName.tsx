"use client";

/**
 * A name typed straight into the page, like the army's name in the roster card: plain text until you
 * hover or focus it, when a dashed line under it shows it can be edited. Enter or Escape finish.
 *
 * `placeholder` is what shows while it has no name of its own. "default" shows it as ordinary text (a
 * unit's type, a regiment's label and number), so an unnamed row reads as before; "hint" shows it as a
 * quiet prompt ("Add a name") where there's nothing to fall back on.
 */
export function InlineName({
  value,
  placeholder,
  onChange,
  label,
  tone = "default",
  className,
}: {
  value: string | undefined;
  placeholder: string;
  onChange: (name: string | undefined) => void;
  /** What the field names, for screen readers, e.g. "Name for this Guard Musketeer" */
  label: string;
  tone?: "default" | "hint";
  className?: string;
}) {
  const text = value ?? "";
  return (
    <input
      type="text"
      className={["inline-name", className].filter(Boolean).join(" ")}
      data-tone={tone}
      value={text}
      placeholder={placeholder}
      aria-label={label}
      maxLength={60}
      spellCheck={false}
      autoComplete="off"
      // Sized to what it shows, so the rules or type after it sit close by
      size={Math.max((text || placeholder).length, 4) + 1}
      onChange={(e) => onChange(e.currentTarget.value || undefined)}
      onBlur={(e) => {
        const trimmed = e.currentTarget.value.trim();
        if (trimmed !== e.currentTarget.value) onChange(trimmed || undefined);
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === "Escape") e.currentTarget.blur();
      }}
    />
  );
}
