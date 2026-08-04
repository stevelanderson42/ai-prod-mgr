import { bandColor, bandTextColor } from '../theme';

interface Props {
  band: string;
  size?: 'sm' | 'md';
}

export function RiskBand({ band, size = 'md' }: Props) {
  const padding = size === 'sm' ? '2px 8px' : '4px 12px';
  const fontSize = size === 'sm' ? '11px' : '12px';

  return (
    <span style={{
      display: 'inline-block',
      backgroundColor: bandColor(band),
      color: bandTextColor(band),
      padding,
      borderRadius: '9999px',
      fontSize,
      fontWeight: 600,
      lineHeight: 1.4,
      whiteSpace: 'nowrap',
    }}>
      {band}
    </span>
  );
}
