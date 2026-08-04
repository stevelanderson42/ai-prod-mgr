import { formatAum, statusColor, statusTextColor } from '../theme';

interface Segment {
  label: string;
  status: string;
  aum: number;
}

interface Props {
  segments: Segment[];
  totalAum: number;
}

export function AumBar({ segments, totalAum }: Props) {
  if (totalAum === 0) return null;

  return (
    <div>
      <div style={{
        display: 'flex',
        height: '32px',
        borderRadius: '6px',
        overflow: 'hidden',
        marginBottom: '8px',
      }}>
        {segments.filter(s => s.aum > 0).map((s, i) => (
          <div
            key={i}
            style={{
              width: `${(s.aum / totalAum) * 100}%`,
              backgroundColor: statusColor(s.status),
              color: statusTextColor(s.status),
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '11px',
              fontWeight: 600,
              minWidth: s.aum / totalAum > 0.08 ? 'auto' : '0',
              overflow: 'hidden',
              whiteSpace: 'nowrap',
              padding: '0 4px',
            }}
          >
            {s.aum / totalAum > 0.08 && `${s.label} ${formatAum(s.aum)}`}
          </div>
        ))}
      </div>
      <div style={{
        display: 'flex',
        gap: '16px',
        fontSize: '12px',
        flexWrap: 'wrap',
      }}>
        {segments.map((s, i) => (
          <span key={i} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{
              width: '10px',
              height: '10px',
              borderRadius: '2px',
              backgroundColor: statusColor(s.status),
              display: 'inline-block',
            }} />
            {s.label}: {formatAum(s.aum)} ({totalAum > 0 ? ((s.aum / totalAum) * 100).toFixed(0) : 0}%)
          </span>
        ))}
      </div>
    </div>
  );
}
