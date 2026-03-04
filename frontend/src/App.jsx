import { useState } from 'react';
import Header from './components/Header';
import NewsFeed from './components/NewsFeed';

const categories = [
  { label: 'Geopolitics', value: 'geopolitics' },
  { label: 'Defense', value: 'defense' },
  { label: 'War', value: 'war' },
  { label: 'Economy', value: 'economy' },
  { label: 'Diplomacy', value: 'diplomacy' }
];

export default function App() {
  const [selectedCategory, setSelectedCategory] = useState('all');

  return (
    <div className="min-h-screen bg-appBg bg-glow text-white">
      <Header
        categories={categories}
        selectedCategory={selectedCategory}
        onSelectCategory={setSelectedCategory}
      />
      <main className="pb-6 pt-2">
        <NewsFeed selectedCategory={selectedCategory} />
      </main>
    </div>
  );
}
