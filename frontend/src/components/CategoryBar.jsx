import { motion } from 'framer-motion';

export default function CategoryBar({ categories, selectedCategory, onSelectCategory }) {
  return (
    <div className="mx-auto mt-3 flex w-full max-w-3xl gap-2 overflow-x-auto pb-1">
      {categories.map((category) => {
        const active = selectedCategory === category.value;

        return (
          <motion.button
            whileTap={{ scale: 0.96 }}
            whileHover={{ y: -1 }}
            key={category.value}
            onClick={() => onSelectCategory(category.value)}
            className={`whitespace-nowrap rounded-full border px-4 py-2 text-sm font-medium transition-all ${
              active
                ? 'border-accent bg-accent/20 text-white shadow-lg shadow-accent/20'
                : 'border-white/15 bg-white/5 text-gray-300 hover:border-white/35 hover:bg-white/10'
            }`}
          >
            {category.label}
          </motion.button>
        );
      })}
    </div>
  );
}
