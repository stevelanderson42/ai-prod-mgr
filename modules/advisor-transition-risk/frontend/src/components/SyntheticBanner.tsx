import { colors } from '../theme';

export function SyntheticBanner() {
  return (
    <div style={{
      backgroundColor: colors.banner,
      color: colors.bannerText,
      padding: '8px 16px',
      fontSize: '13px',
      textAlign: 'center',
      borderBottom: `1px solid ${colors.border}`,
    }}>
      This demo uses synthetic data. No real clients or advisors are represented.
    </div>
  );
}
