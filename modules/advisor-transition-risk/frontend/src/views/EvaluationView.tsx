import { useState } from 'react';
import { EvaluationCase } from '../types';
import { colors, bandColor, bandTextColor } from '../theme';

interface Props {
  cases: EvaluationCase[];
}

export function EvaluationView({ cases }: Props) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const passed = cases.filter(c => c.pass).length;

  const toggle = (id: string) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  return (
    <div>
      <div style={{
        fontSize: '12px',
        color: colors.textMuted,
        marginBottom: '16px',
        padding: '12px 16px',
        backgroundColor: '#f1f5f9',
        borderRadius: '6px',
        lineHeight: 1.6,
      }}>
        This section verifies that the scoring code produces the expected band assignments
        for a set of designed test cases. It confirms the implementation matches its specification.
        It does not validate the model — that would require running the scoring logic against
        historical departure outcomes, which are unavailable in a synthetic demo.
      </div>

      <div style={{
        fontSize: '32px',
        fontWeight: 700,
        marginBottom: '24px',
        color: passed === cases.length ? '#166534' : '#991b1b',
      }}>
        {passed} / {cases.length} passing
      </div>

      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        fontSize: '13px',
      }}>
        <thead>
          <tr>
            {['Case', 'Type', 'Description', 'Expected', 'Actual', 'Result'].map(h => (
              <th key={h} style={{
                textAlign: 'left',
                padding: '10px 12px',
                borderBottom: `2px solid ${colors.border}`,
                color: colors.textMuted,
                fontWeight: 600,
                fontSize: '11px',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {cases.map(c => (
            <>
              <tr
                key={c.case_id}
                onClick={() => toggle(c.case_id)}
                style={{ cursor: 'pointer' }}
                onMouseEnter={e => {
                  (e.currentTarget as HTMLElement).style.backgroundColor = '#f1f5f9';
                }}
                onMouseLeave={e => {
                  (e.currentTarget as HTMLElement).style.backgroundColor = '';
                }}
              >
                <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, fontWeight: 500 }}>
                  {expanded.has(c.case_id) ? '\u25BC' : '\u25B6'} {c.case_id}
                </td>
                <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}` }}>
                  {c.case_type}
                </td>
                <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, maxWidth: '300px' }}>
                  {c.label}
                </td>
                <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}` }}>
                  <span style={{
                    display: 'inline-block',
                    backgroundColor: bandColor(c.expected_band),
                    color: bandTextColor(c.expected_band),
                    padding: '2px 8px',
                    borderRadius: '9999px',
                    fontSize: '11px',
                    fontWeight: 600,
                  }}>
                    {c.expected_band}
                  </span>
                </td>
                <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}` }}>
                  <span style={{
                    display: 'inline-block',
                    backgroundColor: bandColor(c.actual_band),
                    color: bandTextColor(c.actual_band),
                    padding: '2px 8px',
                    borderRadius: '9999px',
                    fontSize: '11px',
                    fontWeight: 600,
                  }}>
                    {c.actual_band}
                    {c.actual_score !== null && ` (${c.actual_score})`}
                  </span>
                </td>
                <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}` }}>
                  <span style={{
                    fontWeight: 700,
                    color: c.pass ? '#166534' : '#991b1b',
                  }}>
                    {c.pass ? 'PASS' : 'FAIL'}
                  </span>
                </td>
              </tr>
              {expanded.has(c.case_id) && (
                <tr key={`${c.case_id}-detail`}>
                  <td colSpan={6} style={{
                    padding: '12px 24px 16px',
                    borderBottom: `1px solid ${colors.border}`,
                    backgroundColor: '#f8fafc',
                  }}>
                    <div style={{ fontSize: '12px', marginBottom: '8px', color: colors.textMuted }}>
                      {c.description}
                    </div>
                    {c.factors.length > 0 && (
                      <div style={{ fontSize: '12px' }}>
                        <div style={{ fontWeight: 600, marginBottom: '4px' }}>Contributing factors:</div>
                        {c.factors.map((f, i) => (
                          <div key={i} style={{ marginLeft: '12px', marginBottom: '2px' }}>
                            <span style={{ fontWeight: 500 }}>{f.signal}:</span>{' '}
                            {f.value} = {f.points} pts
                          </div>
                        ))}
                      </div>
                    )}
                    {c.missing_signals && c.missing_signals.length > 0 && (
                      <div style={{ fontSize: '12px', marginTop: '8px' }}>
                        <div style={{ fontWeight: 600, marginBottom: '4px' }}>Missing / unreliable signals:</div>
                        {c.missing_signals.map((ms, i) => (
                          <div key={i} style={{ marginLeft: '12px', marginBottom: '2px' }}>
                            <span style={{ fontWeight: 500 }}>{ms.signal}:</span>{' '}
                            {ms.reason}
                          </div>
                        ))}
                      </div>
                    )}
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
}
