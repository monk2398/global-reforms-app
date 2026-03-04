import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { getCategoryNews, getLatestNews } from '../api/api';
import LoadingSkeleton from './LoadingSkeleton';
import NewsCard from './NewsCard';

const feedVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08
    }
  }
};

export default function NewsFeed({ selectedCategory }) {
  const [newsItems, setNewsItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [error, setError] = useState('');
  const [bookmarks, setBookmarks] = useState({});
  const sentinelRef = useRef(null);

  const loadNews = useCallback(async () => {
    try {
      setError('');
      setIsLoading(true);

      const data = selectedCategory === 'all' ? await getLatestNews() : await getCategoryNews(selectedCategory);
      setNewsItems(Array.isArray(data) ? data : []);
    } catch {
      setError('Unable to load news');
    } finally {
      setIsLoading(false);
    }
  }, [selectedCategory]);

  useEffect(() => {
    loadNews();
  }, [loadNews]);

  const loadMoreNews = useCallback(async () => {
    if (isLoadingMore || isLoading || error) return;

    try {
      setIsLoadingMore(true);
      const data = selectedCategory === 'all' ? await getLatestNews() : await getCategoryNews(selectedCategory);

      const normalized = Array.isArray(data) ? data : [];
      if (normalized.length) {
        const appended = normalized.map((item, index) => ({
          ...item,
          id: `${item.id}-${Date.now()}-${index}`
        }));
        setNewsItems((prev) => [...prev, ...appended]);
      }
    } catch {
      // Keep existing items visible; optional silent fail for infinite scrolling.
    } finally {
      setIsLoadingMore(false);
    }
  }, [error, isLoading, isLoadingMore, selectedCategory]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMoreNews();
        }
      },
      { threshold: 0.4 }
    );

    if (sentinelRef.current) observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loadMoreNews]);

  useEffect(() => {
    const onKeyDown = (event) => {
      if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return;

      const cards = document.querySelectorAll('[data-news-card="true"]');
      if (!cards.length) return;

      const offset = event.key === 'ArrowDown' ? 1 : -1;
      const viewportCenter = window.scrollY + window.innerHeight / 2;

      let current = 0;
      cards.forEach((node, index) => {
        const rect = node.getBoundingClientRect();
        const top = rect.top + window.scrollY;
        const bottom = top + rect.height;
        if (viewportCenter >= top && viewportCenter < bottom) {
          current = index;
        }
      });

      const next = Math.min(Math.max(current + offset, 0), cards.length - 1);
      cards[next].scrollIntoView({ behavior: 'smooth', block: 'center' });
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [newsItems]);

  const onToggleBookmark = (id) => {
    setBookmarks((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const renderedItems = useMemo(() => {
    return newsItems.map((news) => (
      <div key={news.id} data-news-card="true" className="snap-start">
        <NewsCard
          news={news}
          bookmarked={Boolean(bookmarks[news.id])}
          onToggleBookmark={() => onToggleBookmark(news.id)}
        />
      </div>
    ));
  }, [bookmarks, newsItems]);

  if (isLoading) return <LoadingSkeleton />;

  if (error) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center px-4 text-center text-gray-200">
        <p className="rounded-2xl border border-red-400/30 bg-red-500/10 px-6 py-4 text-lg">{error}</p>
      </div>
    );
  }

  return (
    <AnimatePresence mode="wait">
      <motion.section
        key={selectedCategory}
        variants={feedVariants}
        initial="hidden"
        animate="show"
        className="snap-y snap-mandatory"
      >
        {renderedItems}
        <div ref={sentinelRef} className="mx-auto h-24 w-full max-w-3xl px-4 pb-6 text-center text-gray-500">
          {isLoadingMore ? 'Loading more...' : 'You are up to date'}
        </div>
      </motion.section>
    </AnimatePresence>
  );
}
