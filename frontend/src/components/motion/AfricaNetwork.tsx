"use client";

import { motion } from "motion/react";

import { ARCS, CITIES, DOTS, VIEW_HEIGHT, VIEW_WIDTH } from "./africa";
import { usePrefersReducedMotion } from "./usePrefersReducedMotion";

/**
 * Carte de l'Afrique en matrice de points : des villes pulsent et des arcs lumineux
 * relient les développeurs du continent. Purement décorative (aria-hidden).
 */
export function AfricaNetwork({ className = "" }: { className?: string }) {
  const reduced = usePrefersReducedMotion();

  return (
    <svg viewBox={`-2 -2 ${VIEW_WIDTH + 4} ${VIEW_HEIGHT + 4}`} className={className} aria-hidden role="presentation">
      <defs>
        <linearGradient id="arc-gradient" x1="0" x2="1" y1="0" y2="0">
          <stop offset="0%" stopColor="#34d399" stopOpacity="0" />
          <stop offset="50%" stopColor="#6ee7b7" />
          <stop offset="100%" stopColor="#fbbf24" />
        </linearGradient>
        <radialGradient id="dot-glow">
          <stop offset="0%" stopColor="#fbbf24" stopOpacity="0.9" />
          <stop offset="100%" stopColor="#fbbf24" stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* Continent : les points apparaissent en vague, du nord au sud. */}
      <g>
        {DOTS.map(([x, y], index) => (
          <motion.circle
            key={index}
            cx={x}
            cy={y}
            r={0.58}
            fill="#3fae86"
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 0.55, scale: 1 }}
            transition={{ duration: 0.4, delay: reduced ? 0 : 0.2 + (y / VIEW_HEIGHT) * 1.1 + (x / VIEW_WIDTH) * 0.2 }}
          />
        ))}
      </g>

      {/* Connexions entre développeurs. */}
      <g fill="none" strokeLinecap="round">
        {ARCS.map((arc, index) => (
          <g key={arc.id}>
            <motion.path
              d={arc.d}
              stroke="url(#arc-gradient)"
              strokeWidth={0.45}
              initial={{ pathLength: 0, opacity: 0 }}
              animate={reduced ? { pathLength: 1, opacity: 0.7 } : { pathLength: [0, 1, 1], opacity: [0, 0.9, 0] }}
              transition={
                reduced
                  ? { duration: 0 }
                  : { duration: 3.2, delay: 1.4 + index * 0.45, repeat: Infinity, repeatDelay: ARCS.length * 0.45 - 1.2, ease: "easeInOut" }
              }
            />
            {!reduced && (
              <circle r={0.9} fill="#fde68a">
                <animateMotion dur="3.2s" begin={`${1.4 + index * 0.45}s`} repeatCount="indefinite" path={arc.d} keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines="0.4 0 0.2 1" />
                <animate attributeName="opacity" values="0;1;1;0" dur="3.2s" begin={`${1.4 + index * 0.45}s`} repeatCount="indefinite" />
              </circle>
            )}
          </g>
        ))}
      </g>

      {/* Villes. */}
      <g>
        {CITIES.map((city, index) => (
          <g key={city.name} transform={`translate(${city.at[0]} ${city.at[1]})`}>
            {!reduced && (
              <circle r={1.2} fill="none" stroke="#fbbf24" strokeWidth={0.25} className="origin-center animate-pulse-ring" style={{ animationDelay: `${index * 0.35}s`, transformBox: "fill-box" }} />
            )}
            <circle r={2.4} fill="url(#dot-glow)" opacity={0.6} />
            <motion.circle
              r={0.95}
              fill="#fbbf24"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 300, damping: 14, delay: reduced ? 0 : 1 + index * 0.08 }}
            />
          </g>
        ))}
      </g>
    </svg>
  );
}
