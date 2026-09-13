import type { PriceSnapshot } from "@/lib/types";

const W = 640;
const H = 180;
const PAD_X = 16;
const PAD_TOP = 22;
const PAD_BOTTOM = 28;
const MINT = "#3dd68c";
const MUTED = "#8b9cb3";

function fmtPrice(price: number, currency: string): string {
  const sym = currency === "PEN" ? "S/" : currency;
  return `${sym} ${price.toLocaleString("es-PE")}`;
}

function fmtDate(iso: string): string {
  return new Date(iso).toLocaleDateString("es-PE", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

/** Lightweight SVG line chart for a project's price snapshots (time on x, price on y). */
export function PriceChart({ snapshots }: { snapshots: PriceSnapshot[] }) {
  const pts = snapshots.map((s) => ({
    t: new Date(s.recorded_at).getTime(),
    p: s.price,
    c: s.currency,
  }));

  const minP = Math.min(...pts.map((x) => x.p));
  const maxP = Math.max(...pts.map((x) => x.p));
  const minT = pts[0].t;
  const maxT = pts[pts.length - 1].t;
  const spanT = Math.max(maxT - minT, 1);
  const spanP = maxP - minP || Math.max(1, Math.round(maxP * 0.05));

  const x = (t: number) => PAD_X + ((t - minT) / spanT) * (W - 2 * PAD_X);
  const y = (p: number) => PAD_TOP + (1 - (p - minP) / spanP) * (H - PAD_TOP - PAD_BOTTOM);

  const coords = pts.map((pt) => [x(pt.t), y(pt.p)] as const);
  const line = coords.map(([cx, cy], i) => `${i === 0 ? "M" : "L"}${cx.toFixed(1)},${cy.toFixed(1)}`).join(" ");
  const first = coords[0];
  const last = coords[coords.length - 1];
  const area =
    pts.length > 1
      ? `${line} L${last[0].toFixed(1)},${H - PAD_BOTTOM} L${first[0].toFixed(1)},${H - PAD_BOTTOM} Z`
      : "";

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      role="img"
      aria-label="Histórico de precios del proyecto"
      className="h-44 w-full"
    >
      {area && <path d={area} fill={MINT} fillOpacity={0.1} />}
      <path d={line} fill="none" stroke={MINT} strokeWidth={2} />
      {coords.map(([cx, cy], i) => (
        <circle key={i} cx={cx} cy={cy} r={3.5} fill={MINT} />
      ))}
      <text x={first[0]} y={Math.max(first[1] - 8, 12)} fill={MUTED} fontSize={11}>
        {fmtPrice(pts[0].p, pts[0].c)}
      </text>
      <text x={W - PAD_X} y={Math.max(last[1] - 8, 12)} fill={MUTED} fontSize={11} textAnchor="end">
        {fmtPrice(pts[pts.length - 1].p, pts[pts.length - 1].c)}
      </text>
      <text x={first[0]} y={H - 8} fill={MUTED} fontSize={11}>
        {fmtDate(snapshots[0].recorded_at)}
      </text>
      <text x={W - PAD_X} y={H - 8} fill={MUTED} fontSize={11} textAnchor="end">
        {fmtDate(snapshots[snapshots.length - 1].recorded_at)}
      </text>
    </svg>
  );
}
