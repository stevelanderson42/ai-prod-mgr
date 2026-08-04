import { useState, ReactNode } from 'react';
import { colors } from '../theme';

export interface Column<T> {
  key: string;
  header: string;
  tooltip?: string;
  render: (row: T) => ReactNode;
  sortValue?: (row: T) => number | string;
  width?: string;
}

interface Props<T> {
  columns: Column<T>[];
  data: T[];
  defaultSortKey?: string;
  defaultSortDir?: 'asc' | 'desc';
  onRowClick?: (row: T) => void;
  rowStyle?: (row: T) => React.CSSProperties;
}

export function SortableTable<T>({
  columns,
  data,
  defaultSortKey,
  defaultSortDir = 'desc',
  onRowClick,
  rowStyle,
}: Props<T>) {
  const [sortKey, setSortKey] = useState(defaultSortKey ?? columns[0]?.key);
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>(defaultSortDir);

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('desc');
    }
  };

  const col = columns.find(c => c.key === sortKey);
  const sorted = [...data];
  if (col?.sortValue) {
    const fn = col.sortValue;
    sorted.sort((a, b) => {
      const va = fn(a);
      const vb = fn(b);
      const cmp = typeof va === 'number' && typeof vb === 'number'
        ? va - vb
        : String(va).localeCompare(String(vb));
      return sortDir === 'asc' ? cmp : -cmp;
    });
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        fontSize: '13px',
      }}>
        <thead>
          <tr>
            {columns.map(c => (
              <th
                key={c.key}
                onClick={() => c.sortValue && handleSort(c.key)}
                title={c.tooltip}
                style={{
                  textAlign: 'left',
                  padding: '10px 12px',
                  borderBottom: `2px solid ${colors.border}`,
                  color: colors.textMuted,
                  fontWeight: 600,
                  fontSize: '11px',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  cursor: c.sortValue ? 'pointer' : 'default',
                  userSelect: 'none',
                  whiteSpace: 'nowrap',
                  width: c.width,
                  textDecoration: c.tooltip ? 'underline dotted' : undefined,
                  textUnderlineOffset: c.tooltip ? '3px' : undefined,
                }}
              >
                {c.header}
                {sortKey === c.key && (
                  <span style={{ marginLeft: '4px' }}>
                    {sortDir === 'asc' ? '\u25B2' : '\u25BC'}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, i) => (
            <tr
              key={i}
              onClick={() => onRowClick?.(row)}
              style={{
                cursor: onRowClick ? 'pointer' : 'default',
                ...(rowStyle?.(row) ?? {}),
              }}
              onMouseEnter={e => {
                if (onRowClick) {
                  (e.currentTarget as HTMLElement).style.backgroundColor = '#f1f5f9';
                }
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLElement).style.backgroundColor = '';
              }}
            >
              {columns.map(c => (
                <td
                  key={c.key}
                  style={{
                    padding: '10px 12px',
                    borderBottom: `1px solid ${colors.border}`,
                    verticalAlign: 'top',
                  }}
                >
                  {c.render(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
