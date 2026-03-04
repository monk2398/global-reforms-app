import CategoryBar from './CategoryBar';

export default function Header({ categories, selectedCategory, onSelectCategory }) {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-appBg/75 px-4 pb-3 pt-4 backdrop-blur-xl">
      <div className="mx-auto flex w-full max-w-3xl items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-gray-400">Geopolitics News</p>
          <h1 className="text-2xl font-semibold text-white">Global Reforms</h1>
        </div>
      </div>
      <CategoryBar
        categories={categories}
        selectedCategory={selectedCategory}
        onSelectCategory={onSelectCategory}
      />
    </header>
  );
}
