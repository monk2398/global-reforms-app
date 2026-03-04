export default function LoadingSkeleton() {
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-4 pb-6 pt-5">
      {[...Array(3)].map((_, idx) => (
        <div
          key={idx}
          className="h-[76vh] animate-pulse rounded-3xl border border-white/10 bg-cardBg/70 p-4 shadow-glass"
        >
          <div className="h-1/2 rounded-2xl bg-white/10" />
          <div className="mt-4 h-6 w-1/3 rounded-full bg-white/10" />
          <div className="mt-4 h-8 w-11/12 rounded-xl bg-white/10" />
          <div className="mt-3 h-20 w-full rounded-2xl bg-white/10" />
          <div className="mt-4 h-5 w-1/2 rounded-full bg-white/10" />
        </div>
      ))}
    </div>
  );
}
