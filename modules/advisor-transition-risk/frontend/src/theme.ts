/**
 * Single-hue indigo color system at varying intensity.
 * No red/amber/green.
 */

export const colors = {
  // Risk/likelihood bands
  elevated: '#3730a3', // indigo-800 — dark
  watch: '#6366f1',    // indigo-500 — medium
  stable: '#c7d2fe',   // indigo-200 — light
  insufficient: '#9ca3af', // gray-400

  // Transition statuses
  lost: '#312e81',      // indigo-900
  notStarted: '#4338ca', // indigo-700
  scheduled: '#818cf8',  // indigo-400
  contacted: '#a5b4fc',  // indigo-300
  retained: '#e0e7ff',   // indigo-100

  // UI
  bg: '#f8fafc',
  surface: '#ffffff',
  border: '#e2e8f0',
  text: '#1e293b',
  textMuted: '#64748b',
  banner: '#fef3c7',
  bannerText: '#92400e',
} as const;

export function bandColor(band: string): string {
  switch (band) {
    case 'Elevated':
    case 'High':
      return colors.elevated;
    case 'Watch':
    case 'Moderate':
      return colors.watch;
    case 'Stable':
    case 'Low':
      return colors.stable;
    case 'Insufficient data':
      return colors.insufficient;
    default:
      return colors.insufficient;
  }
}

export function bandTextColor(band: string): string {
  switch (band) {
    case 'Elevated':
    case 'High':
    case 'Watch':
    case 'Moderate':
    case 'Insufficient data':
      return '#ffffff';
    case 'Stable':
    case 'Low':
      return '#3730a3';
    default:
      return '#ffffff';
  }
}

export function statusColor(status: string): string {
  switch (status) {
    case 'lost': return colors.lost;
    case 'not_started': return colors.notStarted;
    case 'scheduled': return colors.scheduled;
    case 'contacted': return colors.contacted;
    case 'retained': return colors.retained;
    default: return colors.insufficient;
  }
}

export function statusTextColor(status: string): string {
  switch (status) {
    case 'retained':
    case 'contacted':
    case 'scheduled':
      return '#312e81';
    default:
      return '#ffffff';
  }
}

export function formatAum(value: number): string {
  if (value >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(1)}B`;
  if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `$${(value / 1_000).toFixed(0)}K`;
  return `$${value}`;
}

export function formatStatus(status: string): string {
  switch (status) {
    case 'not_started': return 'Not Started';
    case 'scheduled': return 'Scheduled';
    case 'contacted': return 'Contacted';
    case 'retained': return 'Retained';
    case 'lost': return 'Lost';
    default: return status;
  }
}
