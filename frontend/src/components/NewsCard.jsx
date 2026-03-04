import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { FiBookmark, FiExternalLink, FiShare2 } from 'react-icons/fi';

function formatTime(value) {
  if (!value) return 'Unknown time';

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(date);
}

export default function NewsCard({ news, bookmarked, onToggleBookmark }) {
  const fallbackImage =
    'https://images.unsplash.com/photo-1526778548025-fa2f459cd5ce?auto=format&fit=crop&w=1300&q=80';

  const imageUrl = useMemo(() => news.image_url || fallbackImage, [news.image_url]);

  const handleShare = async () => {
    const payload = {
      title: news.title,
      text: news.summary,
      url: window.location.href
    };

    if (navigator.share) {
      await navigator.share(payload);
      return;
    }

    await navigator.clipboard.writeText(`${news.title}\n${news.summary}`);
  };

  return (
    <motion.article
      initial={{ opacity: 0, y: 20, scale: 0.98 }}
      whileInView={{ opacity: 1, y: 0, scale: 1 }}
      viewport={{ amount: 0.4, once: false }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
      className="mx-auto h-[calc(100vh-8rem)] w-full max-w-3xl snap-center px-4 pb-6"
    >
      <div className="group flex h-full flex-col overflow-hidden rounded-3xl border border-white/10 bg-cardBg/70 shadow-glass backdrop-blur-xl transition-transform duration-300 hover:-translate-y-1">
        <div className="relative h-[44%] overflow-hidden">
          <img
            src={imageUrl}
            alt={news.title}
            className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
          <span className="absolute left-4 top-4 rounded-full border border-accent/50 bg-accent/20 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-blue-100">
            {news.category}
          </span>
          <button
            onClick={onToggleBookmark}
            className="absolute right-4 top-4 rounded-full bg-black/35 p-2 text-white transition hover:bg-black/60"
            aria-label="Toggle bookmark"
          >
            <FiBookmark className={`${bookmarked ? 'fill-white' : ''}`} size={18} />
          </button>
        </div>

        <div className="flex flex-1 flex-col p-5 sm:p-6">
          <h2 className="line-clamp-3 text-2xl font-bold leading-tight text-white sm:text-3xl">{news.title}</h2>
          <p className="mt-4 line-clamp-6 text-base leading-relaxed text-gray-300">{news.summary}</p>

          <div className="mt-auto flex items-center justify-between pt-5">
            <div>
              <p className="text-sm font-medium text-gray-100">{news.source || 'Unknown source'}</p>
              <p className="text-xs text-gray-400">{formatTime(news.published_at)}</p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleShare}
                className="rounded-full border border-white/15 bg-white/5 p-2 text-gray-200 transition hover:bg-white/10"
                aria-label="Share article"
              >
                <FiShare2 size={16} />
              </button>
              <a
                href={news.image_url}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full border border-white/15 bg-white/5 p-2 text-gray-200 transition hover:bg-white/10"
                aria-label="Open media"
              >
                <FiExternalLink size={16} />
              </a>
            </div>
          </div>

          {Array.isArray(news.tags) && news.tags.length > 0 ? (
            <div className="mt-4 flex flex-wrap gap-2">
              {news.tags.slice(0, 4).map((tag) => (
                <span
                  key={`${news.id}-${tag}`}
                  className="rounded-full border border-white/10 bg-white/5 px-2.5 py-1 text-xs text-gray-300"
                >
                  #{tag}
                </span>
              ))}
            </div>
          ) : null}
        </div>
      </div>
    </motion.article>
  );
}
