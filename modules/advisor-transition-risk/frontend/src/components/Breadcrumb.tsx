import { View, Advisor } from '../types';
import { colors } from '../theme';

interface Props {
  view: View;
  advisors: Advisor[];
  onNavigate: (view: View) => void;
}

export function Breadcrumb({ view, advisors, onNavigate }: Props) {
  const crumbs: { label: string; view: View | null }[] = [];

  crumbs.push({ label: 'Advisor List', view: { kind: 'advisor-list' } });

  if (view.kind === 'household' || view.kind === 'transition') {
    const adv = advisors.find(a => a.advisor_id === view.advisorId);
    const name = adv?.name ?? view.advisorId;

    if (view.kind === 'household') {
      crumbs.push({ label: name, view: null });
    } else {
      crumbs.push({
        label: name,
        view: { kind: 'household', advisorId: view.advisorId },
      });
      crumbs.push({ label: 'Transition Plan', view: null });
    }
  }

  return (
    <nav style={{
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      fontSize: '13px',
      color: colors.textMuted,
      padding: '12px 0',
    }}>
      {crumbs.map((c, i) => (
        <span key={i} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {i > 0 && <span style={{ color: colors.textMuted }}>/</span>}
          {c.view ? (
            <button
              onClick={() => onNavigate(c.view!)}
              style={{
                background: 'none',
                border: 'none',
                color: colors.elevated,
                cursor: 'pointer',
                padding: 0,
                fontSize: '13px',
                textDecoration: 'underline',
              }}
            >
              {c.label}
            </button>
          ) : (
            <span style={{ fontWeight: 600, color: colors.text }}>{c.label}</span>
          )}
        </span>
      ))}
    </nav>
  );
}
