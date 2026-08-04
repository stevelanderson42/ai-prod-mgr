import { Advisor, Household, TransitionEntry, View } from '../types';
import { Breadcrumb } from '../components/Breadcrumb';
import { RiskBand } from '../components/RiskBand';
import { AumBar } from '../components/AumBar';
import { SortableTable, Column } from '../components/SortableTable';
import { colors, formatAum, formatStatus, statusColor, statusTextColor } from '../theme';

const STATUS_ORDER: Record<string, number> = {
  not_started: 0, scheduled: 1, contacted: 2, retained: 3, lost: 4,
};

interface Props {
  advisor: Advisor;
  entries: TransitionEntry[];
  households: Household[];
  allAdvisors: Advisor[];
  onNavigate: (view: View) => void;
}

export function TransitionView({ advisor, entries, households, allAdvisors, onNavigate }: Props) {
  const view: View = { kind: 'transition', advisorId: advisor.advisor_id };

  // Join entries with household AUM
  type Row = TransitionEntry & { aum: number; householdName: string };
  const rows: Row[] = entries.map(e => {
    const hh = households.find(h => h.household_id === e.household_id);
    return {
      ...e,
      aum: hh?.aum ?? 0,
      householdName: hh?.name ?? e.household_id,
    };
  });

  const totalAum = rows.reduce((s, r) => s + r.aum, 0);

  const statusGroups: { label: string; status: string; aum: number }[] = [
    { label: 'Retained', status: 'retained', aum: rows.filter(r => r.status === 'retained').reduce((s, r) => s + r.aum, 0) },
    { label: 'Contacted', status: 'contacted', aum: rows.filter(r => r.status === 'contacted').reduce((s, r) => s + r.aum, 0) },
    { label: 'Scheduled', status: 'scheduled', aum: rows.filter(r => r.status === 'scheduled').reduce((s, r) => s + r.aum, 0) },
    { label: 'Not Started', status: 'not_started', aum: rows.filter(r => r.status === 'not_started').reduce((s, r) => s + r.aum, 0) },
    { label: 'Lost', status: 'lost', aum: rows.filter(r => r.status === 'lost').reduce((s, r) => s + r.aum, 0) },
  ];

  const columns: Column<Row>[] = [
    {
      key: 'name',
      header: 'Household',
      render: r => <span style={{ fontWeight: 500 }}>{r.householdName}</span>,
      sortValue: r => r.householdName,
      width: '15%',
    },
    {
      key: 'aum',
      header: 'AUM',
      render: r => formatAum(r.aum),
      sortValue: r => r.aum,
      width: '10%',
    },
    {
      key: 'status',
      header: 'Status',
      render: r => (
        <span style={{
          display: 'inline-block',
          backgroundColor: statusColor(r.status),
          color: statusTextColor(r.status),
          padding: '2px 10px',
          borderRadius: '9999px',
          fontSize: '11px',
          fontWeight: 600,
        }}>
          {formatStatus(r.status)}
        </span>
      ),
      sortValue: r => STATUS_ORDER[r.status] ?? 5,
      width: '10%',
    },
    {
      key: 'assigned',
      header: 'Assigned To',
      render: r => r.assigned_to,
      sortValue: r => r.assigned_to,
      width: '13%',
    },
    {
      key: 'lastContact',
      header: 'Last Contact',
      render: r => r.last_contact_date ?? '\u2014',
      sortValue: r => r.last_contact_date ?? '',
      width: '10%',
    },
    {
      key: 'nextAction',
      header: 'Next Action',
      render: r => <span style={{ fontSize: '12px' }}>{r.next_action}</span>,
      width: '18%',
    },
    {
      key: 'follow',
      header: 'Follow',
      render: r => <RiskBand band={r.follow_likelihood_band} size="sm" />,
      sortValue: r => ({ High: 0, Moderate: 1, Low: 2 }[r.follow_likelihood_band] ?? 3),
      width: '8%',
    },
    {
      key: 'baseline',
      header: 'Baseline',
      render: r => <RiskBand band={r.baseline_risk_band} size="sm" />,
      sortValue: r => ({ High: 0, Moderate: 1, Low: 2 }[r.baseline_risk_band] ?? 3),
      width: '8%',
    },
  ];

  return (
    <div>
      <Breadcrumb view={view} advisors={allAdvisors} onNavigate={onNavigate} />

      <p style={{
        fontSize: '15px',
        color: colors.textMuted,
        fontStyle: 'italic',
        margin: '0 0 8px 0',
      }}>
        How much of {advisor.name}'s book has been retained, and what remains at risk?
      </p>

      {advisor.departure_date && advisor.score_as_of_date && (
        <p style={{
          fontSize: '12px',
          color: colors.textMuted,
          margin: '0 0 16px 0',
        }}>
          Advisor departed {advisor.departure_date}. Risk scores shown are as of {advisor.score_as_of_date}, 90 days pre-departure.
        </p>
      )}

      <div style={{
        padding: '16px',
        backgroundColor: colors.surface,
        border: `1px solid ${colors.border}`,
        borderRadius: '8px',
        marginBottom: '16px',
      }}>
        <div style={{ fontSize: '13px', fontWeight: 600, marginBottom: '12px' }}>
          AUM Retention Status &mdash; {formatAum(totalAum)} total
        </div>
        <AumBar segments={statusGroups} totalAum={totalAum} />
      </div>

      <SortableTable
        columns={columns}
        data={rows}
        defaultSortKey="status"
        defaultSortDir="asc"
      />
    </div>
  );
}
