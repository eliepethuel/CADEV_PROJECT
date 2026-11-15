"use client";

import { motion, useMotionTemplate, useMotionValue, useSpring, useTransform } from "motion/react";
import type { MouseEvent, ReactNode } from "react";

import { usePrefersReducedMotion } from "./usePrefersReducedMotion";

/** Élément « magnétique » : il suit légèrement le curseur puis revient en place. */
export function Magnetic({ children, strength = 0.35, className }: { children: ReactNode; strength?: number; className?: string }) {
  const reduced = usePrefersReducedMotion();
  const x = useSpring(0, { stiffness: 220, damping: 15 });
  const y = useSpring(0, { stiffness: 220, damping: 15 });

  function onMove(event: MouseEvent<HTMLDivElement>) {
    if (reduced) return;
    const rect = event.currentTarget.getBoundingClientRect();
    x.set((event.clientX - rect.left - rect.width / 2) * strength);
    y.set((event.clientY - rect.top - rect.height / 2) * strength);
  }

  return (
    <motion.div
      className={`inline-block ${className ?? ""}`}
      style={{ x, y }}
      onMouseMove={onMove}
      onMouseLeave={() => {
        x.set(0);
        y.set(0);
      }}
    >
      {children}
    </motion.div>
  );
}

/**
 * Carte « projecteur » : un halo suit le curseur et la carte s'incline légèrement en 3D.
 */
export function SpotlightCard({
  children,
  className = "",
  tilt = true,
  glow = "16 185 129",
}: {
  children: ReactNode;
  className?: string;
  tilt?: boolean;
  glow?: string;
}) {
  const reduced = usePrefersReducedMotion();
  const mouseX = useMotionValue(-400);
  const mouseY = useMotionValue(-400);
  const px = useMotionValue(0.5);
  const py = useMotionValue(0.5);
  const rotateX = useSpring(useTransform(py, [0, 1], [5, -5]), { stiffness: 180, damping: 18 });
  const rotateY = useSpring(useTransform(px, [0, 1], [-6, 6]), { stiffness: 180, damping: 18 });
  const background = useMotionTemplate`radial-gradient(420px circle at ${mouseX}px ${mouseY}px, rgb(${glow} / 0.16), transparent 70%)`;

  function onMove(event: MouseEvent<HTMLDivElement>) {
    const rect = event.currentTarget.getBoundingClientRect();
    mouseX.set(event.clientX - rect.left);
    mouseY.set(event.clientY - rect.top);
    px.set((event.clientX - rect.left) / rect.width);
    py.set((event.clientY - rect.top) / rect.height);
  }

  return (
    <motion.div
      onMouseMove={onMove}
      onMouseLeave={() => {
        px.set(0.5);
        py.set(0.5);
        mouseX.set(-400);
        mouseY.set(-400);
      }}
      style={tilt && !reduced ? { rotateX, rotateY, transformPerspective: 900 } : undefined}
      className={`group relative overflow-hidden rounded-2xl border border-line bg-panel ${className}`}
    >
      <motion.div aria-hidden className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100" style={{ background }} />
      <div className="relative">{children}</div>
    </motion.div>
  );
}

/** Bandeau défilant infini (dupliqué pour une boucle sans couture), en pause au survol. */
export function Marquee({ children, reverse = false, duration = 40 }: { children: ReactNode; reverse?: boolean; duration?: number }) {
  return (
    <div className="group relative flex overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_12%,black_88%,transparent)]">
      <div
        className={`flex shrink-0 gap-3 pr-3 group-hover:[animation-play-state:paused] ${reverse ? "animate-marquee-reverse" : "animate-marquee"}`}
        style={{ ["--marquee-duration" as string]: `${duration}s` }}
      >
        {children}
        <div className="flex shrink-0 gap-3" aria-hidden>
          {children}
        </div>
      </div>
    </div>
  );
}
