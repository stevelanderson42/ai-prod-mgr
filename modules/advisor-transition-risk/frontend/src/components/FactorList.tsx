import { Factor, MissingSignal } from '../types';
import { colors } from '../theme';

interface Props {
  factors: Factor[];
  missingSignals?: MissingSignal[];
  showNoteDisclaimer?: boolean;
}

export function FactorList({ factors, missingSignals, showNoteDisclaimer }: Props) {
  if (missingSignals && missingSignals.length > 0 && factors.length === 0) {
    return (
      <div style={{ fontSize: '12px', color: colors.textMuted }}>
        {missingSignals.map((ms, i) => (
          <div key={i} style={{ marginBottom: '2px' }}>
            <span style={{ fontWeight: 500 }}>{ms.signal}:</span>{' '}
            {ms.reason}
          </div>
        ))}
      </div>
    );
  }

  const hasNoteExcerpt = factors.some(f => f.note_excerpt);

  return (
    <div style={{ fontSize: '12px', color: colors.text }}>
      {factors.map((f, i) => (
        <span key={i}>
          {i > 0 && <span style={{ color: colors.textMuted }}> · </span>}
          <span style={{ fontWeight: 500 }}>{f.signal}</span>{' '}
          <span style={{ color: colors.textMuted }}>
            {f.value} ({f.points}pts)
          </span>
        </span>
      ))}
      {hasNoteExcerpt && showNoteDisclaimer && (
        <div style={{
          fontSize: '11px',
          color: colors.textMuted,
          fontStyle: 'italic',
          marginTop: '2px',
        }}>
          In production, manager and HR notes would be access-restricted by role.
        </div>
      )}
    </div>
  );
}
