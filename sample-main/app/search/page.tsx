'use client';
import React, { useState } from 'react';
import HelpButton from '../helpbutton';
import styles from '../style.module.css';
import { useRouter } from 'next/navigation';
import SearchBar from './searchBar';
import TopBar from './topBar';
import SearchModal from './searchModel';
import FilterSidebar from './FilterSidebar';

export default function SearchPage() {
  const router = useRouter();
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  const handleSearchClick = () => {
    router.push('/');
  };

  const toggleSearchBox = () => {
    setIsSearchOpen(!isSearchOpen);
  };

  const handleCloseClick = () => {
    setIsSearchOpen(false);
  };

  return (
    <>
      <TopBar onSearchClick={toggleSearchBox} onHomeClick={handleSearchClick} />
      
      {isSearchOpen && (
        <SearchModal onClose={handleCloseClick} />
      )}

      <div style={{ padding: '100px 20px' }}>
        <SearchBar />
      </div>

      <FilterSidebar />

      <main className={styles.main}>
        <div style={{
          backgroundImage: `url('/image/search-background.jpeg')`, 
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          width: '100%',
          height: '85vh', 
          position: 'absolute',
          top: '123px', 
          left: 0,
          zIndex: -100, 
        }}></div>
        <HelpButton />
      </main>
    </>
  );
}